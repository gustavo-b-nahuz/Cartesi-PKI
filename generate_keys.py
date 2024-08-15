from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Gerar par de chaves
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Salvar as chaves em arquivos
with open("private_key.pem", "wb") as f:
    f.write(private_key)

with open("public_key.pem", "wb") as f:
    f.write(public_key)

print("Chaves geradas e salvas em 'private_key.pem' e 'public_key.pem'.")

# Assinar a mensagem e salvar a assinatura em hexadecimal
message = b"Mensagem original"
h = SHA256.new(message)
signature = pkcs1_15.new(key).sign(h)

with open("signature.hex", "w") as f:
    f.write(signature.hex())

print("Mensagem assinada e assinatura salva em 'signature.hex'.")
