from os import environ
import traceback
import logging
import requests
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

file_path = "data.json"


def accessDataFile():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado. Criando um novo arquivo.")
        data = []
    return data


def includeNewData(data, new_entry):
    already_exists = False
    remove_entry = False
    for entry in data:
        if entry.get("id") == new_entry.get("id"):
            if entry.get("publicKey") == new_entry.get("publicKey"):
                remove_entry = True
            already_exists = True
    data = [entry for entry in data if entry.get("id") != new_entry.get("id")]
    if not remove_entry:
        data.append(new_entry)
    return data, already_exists, remove_entry


def modifyDataFile(data):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            print(f"Arquivo {file_path} atualizado com o novo conteúdo.")
    except IOError as e:
        print(f"Erro ao salvar o arquivo: {e}")


def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")


def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()


def verify_signature(public_key_pem, message, signature):
    try:
        # Carregar a chave pública
        public_key = RSA.import_key(public_key_pem)

        # Calcular o hash da mensagem
        h = SHA256.new(message.encode())

        # Verificar a assinatura
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False


def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        input = hex2str(data["payload"])
        logger.info(f"Received input: {input}")

        dicionario = json.loads(input)

        # Atribui cada valor a uma variável
        id = dicionario["id"]
        publicKey = dicionario["publicKey"]
        publicKey = publicKey.replace("\\n", "\n").encode()
        signature = bytes.fromhex(dicionario["signature"])
        message = publicKey.decode()

        resultado = verify_signature(publicKey, message, signature)

        if resultado:
            json_data = accessDataFile()
            json_data, already_exists, remove_entry = includeNewData(
                json_data, dicionario
            )
            modifyDataFile(json_data)
            logger.info(
                "\nA assinatura foi verificada com sucesso. O certificado é válido."
            )
            # Emits notice with result of calculation
            if remove_entry:
                logger.info(f"Removing certificate from {id}")
            elif already_exists:
                logger.info(f"Replacing certificate from {id}")
            else:
                logger.info(f"Adding certificate from {id}")
            response = requests.post(
                rollup_server + "/notice", json={"payload": str2hex(str(json_data))}
            )
            logger.info(
                f"Received notice status {response.status_code} body {response.content}"
            )
        else:
            logger.info("\nFalha na verificação. O certificado pode não ser válido.")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(
            rollup_server + "/report", json={"payload": str2hex(msg)}
        )
        logger.info(
            f"Received report status {response.status_code} body {response.content}"
        )

    return status


def searchCert(data, id):
    for item in data:
        if item.get("id") == id:
            return item
    return None


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    id = hex2str(data["payload"])
    json_data = accessDataFile()
    item = searchCert(json_data, id)
    if item is not None:
        logger.info(f"Certificado do {id} encontrado: {item}")
    else:
        logger.info("Certificado não encontrado")
    # logger.info("Adding report")
    # response = requests.post(
    #     rollup_server + "/report", json={"payload": data["payload"]}
    # )
    # logger.info(f"Received report status {response.status_code}")
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]

        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
