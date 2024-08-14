# from Crypto.PublicKey import RSA
# from Crypto.Signature import pkcs1_15
# from Crypto.Hash import SHA256
# import json
# from binascii import unhexlify
#
# # Função para gerar par de chaves (pública e privada)
# def gerar_chaves():
#     chave = RSA.generate(2048)
#     chave_privada = chave.export_key()
#     chave_publica = chave.publickey().export_key()
#     return chave_privada, chave_publica
#
# # Função para assinar um certificado com a chave privada
# def assinar_certificado(certificado, chave_privada):
#     chave_privada_rsa = RSA.import_key(chave_privada)
#     h = SHA256.new(certificado)
#     assinatura = pkcs1_15.new(chave_privada_rsa).sign(h)
#     return assinatura
#
# # Função para verificar a assinatura usando a chave pública
# def verificar_assinatura(certificado, assinatura, chave_publica):
#     chave_publica_rsa = RSA.import_key(chave_publica)
#     h = SHA256.new(certificado)
#     try:
#         pkcs1_15.new(chave_publica_rsa).verify(h, assinatura)
#         return True
#     except (ValueError, TypeError):
#         return False
#
# # Simulação do processo
# # Usuário 1 gera as chaves
# chave_privada, chave_publica = gerar_chaves()
#
# # Usuário 1 cria um certificado (neste exemplo, é apenas uma mensagem)
# certificado = 'Este é um certificado de exemplo.'.encode('utf-8')
#
# # Imprime o certificado
# # print("Certificado:")
# # print(certificado.decode('utf-8'))
#
# # Usuário 1 assina o certificado
# assinatura = assinar_certificado(certificado, chave_privada)
#
# # Imprime a assinatura
# # print("\nAssinatura:")
# # print(assinatura.hex())
#
# # Imprime a chave pública
# # print("\nChave Pública:")
# # print(chave_publica.decode('utf-8'))
#
# # Verificando se o certificado foi realmente assinado pelo dono da chave pública
# resultado = verificar_assinatura(certificado, assinatura, chave_publica)
#
# ########### teste do dapp
# dicionario = json.loads('{"nome":"Gustavo", "certificado":"Certificado teste", "assinatura":"46fc55ea11660935dde516bd8c10493402528af8132d5d6dccd00b8462c922082e9285d909a06fbd39e93e826707350567e1af48c23788e73257d2cc9bf94876afdab04097e0349a50f6236fdb24ade19f268173198f6acc2f4fadb39715eb418b450b650b2fee0fffa8780ac79a20b13112d2ce8f8a7f08bc4deeb3158d8d300125638c5c6fa8fac0061d1ec3a0347c83e610d08de57ebe3d27d54da9748e160f41a87ba1ed7455795b8ee1916a818b6155d6fe9cf71944a613adff6761176208d8c39287855daf2a189b52f7343b26b052a1a923788c2592c58485825d238dd7c35559006de404a0b088e6e5cceb5348af7e27207beedcefe9fd476745dfe1", "publicKey":"-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvHdlEdv8TdbWzy/2ejzn\\n4zb2KyOX6PCyoZzJpsBTA03WFloL/Q6UsPjjjpUQ8ZpaOjNeMZnuZqMfhYdYOsH/\\nU7v22j6Iw2XBEnnpZQA53tE4YQmZHk/HbiymfKhtfM9qtzwds7f/Wml46tRchqOk\\nApaGomCj+DAQXVHY1i5YybMTmd6X9aYynVj+/JExCIdvRGMruFGE7UnfIsfDTCWK\\nVptyPOBElhN5nSN73btEzbua4oxcZs5nj+9nuHM3xXDuOn+geZbQUEwHKLGnPk2b\\nSpu6L6LmdvOIR8JcYz46KdzMNijTqCzA4mZO6EBR9GQ+KGGTdauMu1KB3GTTjQ7E\\n+wIDAQAB\\n-----END PUBLIC KEY-----"}')
#
# # Atribui cada valor a uma variável
# nome = dicionario["nome"]
# certificado = dicionario["certificado"]
# certificado = certificado.encode('utf-8')
# assinatura = (dicionario["assinatura"])
# publicKey = dicionario["publicKey"]
#
# print("Nome:", nome)
# print("Certificado:", certificado)
# print("Assinatura:", assinatura)
# print("Chave Pública:", publicKey)
# resultado = verificar_assinatura(certificado, assinatura, publicKey)
# ########### teste do dapp
#
# if resultado:
#     print("A assinatura foi verificada com sucesso. O certificado é válido.")
# else:
#     print("Falha na verificação. O certificado pode não ser válido.")

# Aqui comeca codigo que gera as chaves e salva no arquivo pem
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Gerar par de chaves
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Exportar a chave pública
public_key = private_key.public_key()
pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Exportar a chave privada
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Salvar as chaves em arquivos
with open('private_key.pem', 'wb') as f:
    f.write(pem_private_key)

with open('public_key.pem', 'wb') as f:
    f.write(pem_public_key)

print("Chaves geradas e salvas em 'private_key.pem' e 'public_key.pem'.")

# Aqui comeca codigo que assina a mensagem e salva no arquivo hex
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Carregar a chave privada
with open('private_key.pem', 'rb') as f:
    pem_private_key = f.read()

private_key = load_pem_private_key(pem_private_key, password=None)

# Mensagem a ser assinada
message = b"Mensagem original"

# Assinar a mensagem
signature = private_key.sign(
    message,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Salvar a assinatura em formato hexadecimal
with open('signature.hex', 'w') as f:
    f.write(signature.hex())

print("Mensagem assinada e assinatura salva em 'signature.hex'.")

# Aqui comeca codigo que verifica se assinatura eh valida
import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

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


if len(sys.argv) != 4:
    print("Uso: python script.py <public_key_pem> <message> <signature>")
    sys.exit(1)

public_key_pem = sys.argv[1]
message = sys.argv[2]
signature = bytes.fromhex(sys.argv[3])

# Verificação
if verify_signature(public_key_pem, message, signature):
    print("Assinatura verificada com sucesso.")
else:
    print("Falha na verificação da assinatura.")