import sys
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


# Função para verificar a assinatura
def verify_signature(public_key_pem, message, signature):
    try:
        # Carregar a chave pública
        public_key_pem = public_key_pem.replace("\\n", "\n").encode()
        public_key = RSA.import_key(public_key_pem)

        # Calcular o hash da mensagem
        h = SHA256.new(message.encode())

        # Verificar a assinatura
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
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
