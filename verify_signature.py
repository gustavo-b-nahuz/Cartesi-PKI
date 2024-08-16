import sys
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


# Função para verificar a assinatura
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


# Ler a chave pública a partir do arquivo
with open("public_key.pem", "rb") as f:
    public_key_pem = f.read()

# Ler a assinatura a partir do arquivo
with open("signature.hex", "r") as f:
    signature = bytes.fromhex(f.read())

# Usar a chave pública como a mensagem
message = public_key_pem.decode()

# Verificação
if verify_signature(public_key_pem, message, signature):
    print("Assinatura verificada com sucesso.")
else:
    print("Falha na verificação da assinatura.")
