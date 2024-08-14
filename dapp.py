from os import environ
import traceback
import logging
import requests
from py_expression_eval import Parser
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

def verificar_assinatura(certificado, assinatura, chave_publica):
    chave_publica_rsa = RSA.import_key(chave_publica)
    h = SHA256.new(certificado)
    try:
        pkcs1_15.new(chave_publica_rsa).verify(h, assinatura)
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
        nome = dicionario["nome"]
        certificado = dicionario["certificado"]
        assinatura = dicionario["assinatura"]
        publicKey = dicionario["publicKey"]

        # Exibe os valores das variáveis
        print("Nome:", nome)
        print("Certificado:", certificado)
        print("Assinatura:", assinatura)
        print("Chave Pública:", publicKey)

        resultado = verificar_assinatura(certificado, assinatura, publicKey)

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