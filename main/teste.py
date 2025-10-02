import json

# Carregando o JSON (você poderia carregar de um arquivo externo também)
data = {
  "pessoas": [
    {
      "campo": "transporte",
      "pergunta": "Você utiliza carro particular diariamente? (Sim ou Não): ",
      "tipo": "sim_nao"
    },
    {
      "campo": "km_carro",
      "pergunta": "Quantos km você dirige por semana em média?: ",
      "tipo": "numero",
      "unidade": "km"
    },
    {
      "campo": "tipo_combustivel",
      "pergunta": "Qual o tipo de combustível do carro (gasolina, etanol, diesel, eletrico)?: ",
      "tipo": "texto"
    },
    {
      "campo": "energia_residencial",
      "pergunta": "Qual o consumo mensal de eletricidade da sua casa?: ",
      "tipo": "numero",
      "unidade": "kWh"
    },
    {
      "campo": "viagens_aereas",
      "pergunta": "Quantos voos domésticos você fez no último ano?: ",
      "tipo": "numero",
      "unidade": "voos"
    },
    {
      "campo": "alimentacao",
      "pergunta": "Com que frequência você consome carne vermelha por semana?: ",
      "tipo": "numero",
      "unidade": "vezes/semana"
    }
  ],
  "empresas": [
    {
      "campo": "eletricidade",
      "pergunta": "Qual foi o consumo anual de eletricidade da empresa?: ",
      "tipo": "numero",
      "unidade": "kWh"
    },
    {
      "campo": "diesel",
      "pergunta": "Quantos litros de diesel a empresa consumiu no ano?: ",
      "tipo": "numero",
      "unidade": "litros"
    },
    {
      "campo": "gasolina",
      "pergunta": "Quantos litros de gasolina foram consumidos no ano?: ",
      "tipo": "numero",
      "unidade": "litros"
    },
    {
      "campo": "gas_natural",
      "pergunta": "Quantos metros cúbicos de gás natural foram consumidos?: ",
      "tipo": "numero",
      "unidade": "m³"
    },
    {
      "campo": "residuos",
      "pergunta": "Quantos quilos de resíduos sólidos a empresa gerou?: ",
      "tipo": "numero",
      "unidade": "kg"
    },
    {
      "campo": "viagens_corporativas",
      "pergunta": "Quantas viagens aéreas corporativas foram realizadas no ano?: ",
      "tipo": "numero",
      "unidade": "voos"
    }
  ]
}

def perguntar_e_calcular(lista_perguntas):
    total_co2 = 0
    respostas = {}

    for item in lista_perguntas:
        if item["tipo"] == "sim_nao":
            resposta = input(item["pergunta"]).strip().lower()
            respostas[item["campo"]] = resposta
            if resposta == "sim":
                quantidade = float(input(f"Informe a quantidade de CO₂ emitida ({item.get('unidade','kg')}): "))
                total_co2 += quantidade
        elif item["tipo"] == "numero":
            valor = float(input(item["pergunta"]))
            respostas[item["campo"]] = valor
            total_co2 += valor  # Aqui você poderia aplicar uma fórmula real de CO₂ por unidade
        elif item["tipo"] == "texto":
            valor = input(item["pergunta"]).strip()
            respostas[item["campo"]] = valor

    return total_co2, respostas

# Escolher tipo de questionário
tipo = input("Você quer calcular CO₂ de uma pessoa ou empresa? (pessoa/empresa): ").strip().lower()

if tipo == "pessoa":
    total, respostas = perguntar_e_calcular(data["pessoas"])
elif tipo == "empresa":
    total, respostas = perguntar_e_calcular(data["empresas"])
else:
    print("Tipo inválido.")
    total = 0
    respostas = {}

print("\nRespostas coletadas:")
for k, v in respostas.items():
    print(f"{k}: {v}")

print(f"\nTotal estimado de CO₂: {total} kg")
