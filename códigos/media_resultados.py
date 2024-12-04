import json

# Carregar o arquivo JSON
with open('avaliacao_2.json', 'r') as file:
    dados = json.load(file)

i = 0
precisao = 0
recall = 0
f1 = 0
for user, lista in dados.items():
    precisao += lista[0]
    recall += lista[1]
    f1 += lista[2]
    i += 1
p = ((precisao/i),(recall/i),(f1/i)) 
print(p)