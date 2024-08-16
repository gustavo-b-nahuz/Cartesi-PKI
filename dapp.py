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
        signature_file = dicionario["signature_file"]
        public_key_file = dicionario["public_key_file"]

        # Ler a chave pública a partir do arquivo
        with open(public_key_file, "rb") as f:
            public_key_pem = f.read()

        # Ler a assinatura a partir do arquivo
        with open(signature_file, "r") as f:
            signature = bytes.fromhex(f.read())

        message = public_key_pem.decode()

        resultado = verify_signature(public_key_pem, message, signature)

        if resultado:
            logger.info(
                "\nA assinatura foi verificada com sucesso. O certificado é válido."
            )
            # Emits notice with result of calculation
            logger.info(f"Adding notice with payload from {id}")
            response = requests.post(
                rollup_server + "/notice", json={"payload": str2hex(dicionario)}
            )
            logger.info(
                f"Received notice status {response.status_code} body {response.content}"
            )
        else:
            logger.info("\nFalha na verificação. O certificado pode não ser válido.")
        # Evaluates expression
        # parser = Parser()
        # output = parser.parse(input).evaluate({})

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


def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    response = requests.post(
        rollup_server + "/report", json={"payload": data["payload"]}
    )
    logger.info(f"Received report status {response.status_code}")
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
