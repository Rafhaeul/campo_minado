import json


def registrar(nome, pontos, dia):

    dados = {
        nome:{
        "Pontos": pontos,
        "Data": dia
    }}


    try:
        with open("registro.json", 'r') as arquivo:
            dados_arquivo = json.load(arquivo)

    except FileNotFoundError:
        with open("registro.json", 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
    else:
        dados_arquivo.update(dados)
        with open("registro.json", 'w') as arquivo:
            json.dump(dados_arquivo, arquivo, indent=4)
    finally:
        with open("registro.json") as arquivo:
            todos = json.load(arquivo)
            maior = 0
            for key, value in todos.items():
                if maior < todos[key]['Pontos']:
                    maior = todos[key]['Pontos']
                    recordista = key

    return recordista, maior


