from os import environ
import traceback
import logging
import requests
from py_expression_eval import Parser
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

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
        # Remover espaços em branco desnecessários e novas linhas
        public_key_pem = public_key_pem.replace("\\n", "\n").encode()

        # Carregar a chave pública do formato PEM
        public_key = load_pem_public_key(public_key_pem)

        # Verificar a assinatura
        public_key.verify(
            signature,
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except ValueError as e:
        print(f"Erro ao carregar a chave pública: {e}")
        return False

def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    status = "accept"
    try:
        input = hex2str(data["payload"])
        logger.info(f"Received input: {input}")

        dicionario = json.loads(input)

        # Atribui cada valor a uma variável
        nome = dicionario["nome"]
        mensagem = dicionario["certificado"]
        assinatura = dicionario["assinatura"]
        publicKey = dicionario["publicKey"]

        # Exibe os valores das variáveis
        print("Nome:", nome)
        print("Mensagem:", mensagem)
        print("Assinatura:", assinatura)
        print("Chave Pública:", publicKey)

        resultado = verify_signature(publicKey, mensagem, assinatura)

        if resultado:
            print("\nA assinatura foi verificada com sucesso. O certificado é válido.")
        else:
            print("\nFalha na verificação. O certificado pode não ser válido.")
        # Evaluates expression
        # parser = Parser()
        # output = parser.parse(input).evaluate({})

        # Emits notice with result of calculation
        # logger.info(f"Adding notice with payload: '{output}'")
        response = requests.post(rollup_server + "/notice", json={"payload": str2hex(str("Sucesso"))})
        logger.info(f"Received notice status {response.status_code} body {response.content}")

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {data}\n{traceback.format_exc()}"
        logger.error(msg)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(msg)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return status

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json={"payload": data["payload"]})
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