import json

file_path = 'data.json'

def accessDataFile():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f'Arquivo {file_path} não encontrado. Criando um novo arquivo.')
        data = []
    return data

def modifyDataFile(data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print(f'Arquivo {file_path} atualizado com o novo conteúdo.')
    except IOError as e:
        print(f'Erro ao salvar o arquivo: {e}')

def includeNewData(data,new_entry):
    data.append(new_entry)

def modifyData(data,id,new_entry):
    for item in data:
        if item['nome'] == id:
            item.update(new_entry)
            return True
    return False

def excludeData(data,id):
    for item in data:
        if item['nome'] == id:
            data.remove(item)
            return True
    return False

# Obter dados do arquivo
#data = accessDataFile()

# Incluir item
#includeNewData(data,new)

# Alterar item
#modifyData(data,"Miguel",new)

# Excluir item
#excludeData(data,"Miguel")

# Salvar dados atualizados no arquivo
#modifyDataFile(data)  
