import json

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


def modifyData(data, id, new_entry):
    for item in data:
        if item["nome"] == id:
            item.update(new_entry)
            return True
    return False


def excludeData(data, id):
    for item in data:
        if item["nome"] == id:
            data.remove(item)
            return True
    return False


dicionario = {
    "id": "Miguel",
    "signature": "91fd286e69dc900b7dd49a6637fa05b5ac53d7771d383f42c1eae6651f63fa8d75e43b37905d05c699d683499fa9ca41dc3df259913aa5b455912334530c9302aa73732914569bb6f053a5ded5c716e355c5adb0a253c0b15a920d510a716436f05f5054cc1ba331ae9c3afe7fb3ba348d18df30af6fa66dc78422b238d23e6a7990568cab34264e783b927ee007a9077cc431e08e2c57f1a7c180ae1e72b6fa0efd71c66bd556318a497b8bebba7901149ea96884e673bf466018b0509639d1dffdca1dc726fd4cc6888f2269f6a41df3c991e5bb98eb411e5e74e101896a0724a93f2afa29814ef332139d082bc205569eccdc6797b5f27e4a3f7721de7a2d",
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyc4ONrDVbGji5mGEvZhj\nEFWIPnziRBFBfQsFgAFNHaez0HSnVr/e0XJLey3Yawi+FkX1McAxgJl2A6o8461t\n6G5cp92+9h6iOCEFNVmcnY+mYAiOoKyR9o8+/xUV6zByzwBAT/ZWY+5VEyjVMvVq\neLKAMg+Iaw1oBBfyELAcbR0v3s4L1oG0T+13pil2MCZpMMdV5WBIh8kX3775ilta\n+RgI2ZEyrbRY0QlLiDNQ4LbQMbnlrt3CRhlMuaw+xYlVDl5fGPmTXAHa2M+rTxMy\n6CSNUbAISbdGHfG8VVKrgzR8sGOusxoBG/NvrxCf3cZsz8IKextP3fL8LE2wfsHQ\n8QIDAQAB\n-----END PUBLIC KEY-----",
}
dicionario2 = {
    "id": "Gustavo",
    "signature": "88a1c8840c6d26e3a9901c127b7c2a495940dde2de0208b5d3561f6d52061799191a3915163cba63eb2480d99da473424a0bfa5c22f60105aa743b817a6a834b68463ec3403418b238793886303142bf668d07a36cded95b648d68d7c33a7339e4b1792a2a0eeaaa18ca719ea0228e4e8c68163c2479d7c54c01b6237a8259f07c0060f6d4ccdc61e38351756fa5d7ac84e3132695be480b169faf2694cdbf6cbad46eab1cc3acb51313ada403cca5b92c35d33d6dc8457132f3d91111839b99825a472c1f23ac26d3a2256005398df27b069a3cc28355ec1ed680f0594ec20c441d9903b1849a80535c4f549f0fc536df4b1d9129e0592a2972d20b7d72bfe5",
    "publicKey": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm1dvUFAk1KYxQBwpuzZ2\nz6Mr0eTU7jtKNIVQR2Hwbzr7yxI4RC73exwDu8/KD8+/hJoroMibHNRXdaXOGJid\n7cegfrq4HSpBdIjB+IZu6nJoBd9yt5GVVws3BG3AlZx8rTdZb06VqzLMPowo1ZzK\nKdg4vL7+COYj8SFuusiQd0qXORCiP1ve+iY5ffLvcR9R9T0kzHvhVSASrNvwjFJP\n/yQ1iinqaSI+yUMFRbB6wnK70wFntGeir0dOtZfqayGMvBZubqXQboam50JmOVdW\nDQKH0YzpIHzqTHJc5CqtOa7qFijc8I7SXRUsFji9XAqFxCvRE9b5JQdPJx9FkgY2\nowIDAQAB\n-----END PUBLIC KEY-----",
}

# Obter dados do arquivo
data = accessDataFile()
# Incluir item
data, already_exists, remove_entry = includeNewData(data, dicionario)
print(data)

modifyDataFile(data)

data = accessDataFile()
data, already_exists, remove_entry = includeNewData(data, dicionario2)
print(data)
modifyDataFile(data)
# Alterar item
# modifyData(data,"Miguel",new)

# Excluir item
# excludeData(data,"Miguel")

# Salvar dados atualizados no arquivo
