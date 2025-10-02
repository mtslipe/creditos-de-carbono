import json

with open('main\perguntas.json', 'r', encoding='utf-8') as arq:
    vListaPerguntas = json.load(arq)

def calcularCO2():
    vQuantidadeTotal = 0
    for pergunta in vListaPerguntas["pessoas"]:
        resposta = input(pergunta["pergunta"]).strip().lower()
        if resposta == "sim":
            vValor = int(input(pergunta["contra_pergunta"]))
            vQuantidadeTotal += vValor * pergunta["calculo_co2"]
    
    return vQuantidadeTotal

print(f"Total de CO₂ informado: {calcularCO2()} kg")