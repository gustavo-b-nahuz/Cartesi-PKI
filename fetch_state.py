import requests


def hex2str(hex_str):
    # Remove o prefixo "0x" se estiver presente
    clean_hex = hex_str[2:] if hex_str.startswith("0x") else hex_str

    # Converte a string hexadecimal para uma sequência de bytes
    bytes_data = bytes.fromhex(clean_hex)

    # Decodifica os bytes para uma string UTF-8
    return bytes_data.decode("utf-8")


def fetch_graphql_data():
    try:
        response = requests.post(
            "http://localhost:8080/graphql",
            json={"query": "{ notices { edges { node { payload } } } }"},
            headers={"Content-Type": "application/json"},
        )

        result = response.json()

        for edge in result["data"]["notices"]["edges"]:
            payload = edge["node"]["payload"]
            print(hex2str(payload))
    except Exception as error:
        print("Erro ao buscar dados do GraphQL:", error)


fetch_graphql_data()
