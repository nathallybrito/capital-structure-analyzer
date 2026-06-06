# Analisador de Estrutura de Capital

Aplicação desenvolvida para a disciplina de Administração Financeira (CAD 167) - UFMG

## Descrição

Este projeto implementa um sistema completo para análise e otimização de **Estrutura de Capital** de empresas. A aplicação captura dados financeiros, calcula métricas essenciais, utiliza algoritmos de previsão para estimar custos de capital e recomenda uma estrutura de capital ótima que minimiza o WACC (Weighted Average Cost of Capital).

## Tema: Estrutura de Capital

A Estrutura de Capital refere-se à forma como uma empresa financia seus ativos, através de uma combinação de dívida (debt) e patrimônio (equity). Decisões sobre essa estrutura afetam:
- O custo de capital da empresa
- O risco financeiro
- O valor da empresa
- As políticas de dividendos

## Funcionalidades

1. **Captura de Dados**: Interface para inserir dados financeiros de empresas
2. **Cálculo de Métricas**: Indices de alavancagem, D/E ratio, ROE, ROA, etc.
3. **Previsão de WACC**: Algoritmo de regressão para prever custo de capital
4. **Otimização**: Encontra a estrutura de capital ótima usando otimização numérica
5. **Geração de Relatórios**: Relatórios em PDF e CSV com gráficos e análises

## Estrutura do Projeto

```
capital-structure-analyzer/
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências Python
├── data/
│   └── companies_data.csv    # Dados das empresas (exemplo)
├── src/
│   ├── __init__.py
│   ├── main.py              # Entrada principal
│   ├── data_capture.py      # Captura de dados
│   ├── capital_structure.py # Cálculos de estrutura de capital
│   ├── wacc_calculator.py   # Cálculo do WACC
│   ├── prediction.py        # Algoritmo de previsão (regressão)
│   ├── optimization.py      # Otimização da estrutura de capital
│   └── report_generator.py  # Geração de relatórios
└── reports/                 # Relatórios gerados
```

## Algoritmos Implementados

### 1. Cálculo de WACC
```
WACC = (E/V) * Re + (D/V) * Rd * (1 - Tc)

Onde:
- E = Valor do Patrimônio
- D = Valor da Dívida
- V = E + D (Valor Total)
- Re = Custo do Patrimônio (CAPM)
- Rd = Custo da Dívida
- Tc = Taxa de Impostos
```

### 2. Modelo de Previsão
Utiliza **Regressão Polinomial** para prever WACC em função do Debt/Equity Ratio:
- Treina um modelo com dados históricos
- Gera previsões para diferentes estruturas de capital
- Calcula intervalo de confiança

### 3. Otimização
Encontra a estrutura de capital que **minimiza o WACC** usando:
- Algoritmo de otimização numérica (Scipy)
- Restrições de limite mínimo e máximo de alavancagem
- Análise de sensibilidade

## Como Executar

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

```bash
git clone https://github.com/seu-usuario/capital-structure-analyzer.git
cd capital-structure-analyzer
pip install -r requirements.txt
```

### Execução

```bash
python src/main.py
```

## Uso

A aplicação oferece um menu interativo:

1. **Inserir Nova Empresa**: Captura dados de uma nova empresa
2. **Listar Empresas**: Exibe todas as empresas registradas
3. **Analisar Empresa**: Calcula métricas e estrutura de capital
4. **Gerar Previsões**: Prevê WACC para diferentes D/E ratios
5. **Otimizar Estrutura**: Encontra a estrutura de capital ótima
6. **Gerar Relatório**: Cria relatório em PDF
7. **Sair**: Encerra a aplicação

## Exemplo de Dados Entrada

```csv
empresa,ativos_totais,dívida_total,patrimônio,ebitda,taxa_imposto
Empresa A,1000000,300000,700000,200000,0.34
Empresa B,2000000,800000,1200000,400000,0.34
```

## Métricas Calculadas

- **Leverage Ratio (D/A)**: Dívida / Ativo Total
- **Debt-to-Equity (D/E)**: Dívida / Patrimônio
- **Interest Coverage**: EBITDA / Despesas com Juros
- **Custo do Patrimônio (Re)**: Calculado via CAPM
- **Custo da Dívida (Rd)**: Taxa de juros implícita
- **WACC**: Custo médio ponderado de capital

## Relatórios Gerados

- Análise detalhada por empresa
- Gráficos de estrutura de capital vs. WACC
- Curva de otimização com ponto ótimo
- Recomendações de restruturação

## Autores

Trabalho 2 - Administração Financeira (CAD 167)
Disciplina: Administração Financeira
Professor: Bruno Pérez Ferreira
UFMG - Faculdade de Ciências Econômicas - 2026
