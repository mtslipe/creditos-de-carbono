# Calculadora de Carbono

Uma ferramenta para estimar emissões de gases do efeito estufa (GEE).

## Sobre o Projeto

A Calculadora de Carbono é uma aplicação desenvolvida em Python que permite aos usuários:
- Calcular suas emissões de CO₂
- Determinar a quantidade de créditos de carbono necessários para compensação
- Avaliar custos de compensação através de diferentes projetos
- Manter um histórico de cálculos e compensações

## Funcionalidades

- **Cálculo de Emissões**: Suporte para cálculos individuais e empresariais
- **Projetos de Compensação**:
  - Reflorestamento
  - Energias Renováveis
  - Captura de Metano
  - Conservação Florestal
- **Histórico de Cálculos**: Registro completo de todas as estimativas e compensações
- **Interface Gráfica**: Design intuitivo e responsivo usando CustomTkinter

## Bibliotecas

- Python 3
- CustomTkinter
- JSON 
- DateTime 
- OS 

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/mtslipe/creditos-de-carbono.git
```

2. Instale as dependências:
```bash
pip install customtkinter
```

3. Execute o aplicativo:
```bash
python app.py
```

## Como Usar

1. **Login**: Digite seu nome para começar
2. **Escolha o Tipo**: Selecione entre cálculo para pessoas ou empresas
3. **Responda as Perguntas**: Forneça informações sobre consumo e atividades
4. **Visualize Resultados**: Veja suas emissões totais e opções de compensação
5. **Compense**: Escolha um projeto e registre sua compensação
6. **Histórico**: Acesse seus cálculos e compensações anteriores

## Projetos de Compensação

- **Reflorestamento**: R$ 90,00/tCO₂
- **Energias Renováveis**: R$ 85,00/tCO₂
- **Captura de Metano**: R$ 110,00/tCO₂
- **Conservação Florestal**: R$ 75,00/tCO₂

## Estrutura do Projeto

```
creditos-de-carbono/
│
├── app.py           # Aplicativo principal
├── perguntas.json  # Banco de perguntas
├── historico.json  # Registro de cálculos
└── README.md       # Documentação
```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.
