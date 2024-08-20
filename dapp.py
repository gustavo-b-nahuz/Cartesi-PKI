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

# Acessa o arquivo JSON (banco de dados local) e retorna um array com seus dados (ou em branco caso não exista o arquivo)
def accessDataFile():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado. Criando um novo arquivo.")
        data = []
    return data

# Atualiza o array
def updateData(data, new_entry):
    already_exists = False
    remove_entry = False
    # Itera sobre os certificados existentes
    for entry in data:
        # Caso o ID do inserido já existia, marca a flag already_exists como true
        if entry.get("id") == new_entry.get("id"):
            # Caso o certificado seja igual, quer dizer que devemos removê-lo, então marca remove_entry como true
            # Se não for igual, iremos apenas alterá-lo
            if entry.get("publicKey") == new_entry.get("publicKey"):
                remove_entry = True
            already_exists = True
    # Remove um certificado antigo caso tenha o mesmo ID do novo
    data = [entry for entry in data if entry.get("id") != new_entry.get("id")]
    # Só inclui o novo se o ID não existia antes
    if not remove_entry:
        data.append(new_entry)
    return data, already_exists, remove_entry

# Modifica o arquivo JSON com o array atualizado 
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

# Verifica se a mensagem foi assinada pela mesma chave privada que gerou a chave publica
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
        # A mensagem utilizada para gerar a assinatura foi o proprio certificado com chave publica
        message = publicKey.decode()

        resultado = verify_signature(publicKey, message, signature)

        # Se a assinatura e valida
        if resultado:
            # O json (BD) e acessado e um array com as informacoes criado
            json_data = accessDataFile()
            
            # O array e atualizado com as informacoes atuais
            json_data, already_exists, remove_entry = updateData(json_data, dicionario)
            
            # O arquivo json e modificado com as novas informacoes
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
            logger.info("\nFalha na verificação. A assinatura não é válida.")

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

# Busca no array as informacoes do id
def searchCert(data, id):
    for item in data:
        if item.get("id") == id:
            return item
    return None


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    
    # Recebe da solicitacao de inspect o id a ser buscado
    id = hex2str(data["payload"])

    # O json (BD) e acessado e um array com as informacoes criado
    json_data = accessDataFile()

    # Busca no array o id solicitado no inspect
    item = searchCert(json_data, id)
    if item is not None:
        logger.info(f"Certificado do {id} encontrado:\n{item['publicKey']}")
    else:
        logger.info("Certificado não encontrado")

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
