# Estrutura do Projeto

## 📁 Organização de Diretórios

```
capital-structure-analyzer/
│
├── src/                          # Código-fonte principal
│   ├── __init__.py              # Inicializador do pacote
│   ├── main.py                  # Interface interativa (menu principal)
│   ├── capital_structure.py     # Cálculos de estrutura de capital
│   ├── wacc_calculator.py       # Cálculo do WACC (Weighted Average Cost of Capital)
│   ├── prediction.py            # Algoritmo de previsão (Regressão Polinomial)
│   ├── optimization.py          # Otimização de estrutura de capital
│   ├── data_capture.py          # Captura e carregamento de dados
│   └── report_generator.py      # Geração de relatórios e gráficos
│
├── data/                         # Dados das empresas
│   └── companies_data.csv       # Base de dados em CSV (criada automaticamente)
│
├── reports/                      # Relatórios gerados (criado em tempo de execução)
│   ├── *.txt                    # Relatórios em texto
│   └── *.png                    # Gráficos em PNG
│
├── test_aplicacao.py            # Script de teste rápido
├── requirements.txt             # Dependências Python
├── .gitignore                   # Arquivo git (ignore)
├── README.md                    # Documentação principal
├── INSTALACAO.md                # Guia de instalação
├── ESTRUTURA.md                 # Este arquivo (organização do projeto)
└── LICENSE                      # Licença do projeto
```

## 📝 Descrição dos Módulos

### `src/capital_structure.py`
**Classe: CapitalStructure**

Responsável pelos cálculos fundamentais de estrutura de capital:

- **Métodos principais:**
  - `leverage_ratio()` → D/A ratio
  - `debt_to_equity()` → D/E ratio
  - `equity_ratio()` → E/A ratio
  - `custo_divida_implicito()` → Taxa de custo da dívida
  - `interest_coverage()` → Índice de cobertura de juros
  - `roi()` → Retorno sobre investimento
  - `roe()` → Retorno sobre patrimônio

**Fórmulas implementadas:**
```
D/A = Dívida / Ativo Total
D/E = Dívida / Patrimônio
Interest Coverage = EBITDA / Despesa com Juros
ROE = Lucro Líquido / Patrimônio
```

### `src/wacc_calculator.py`
**Classe: WACCCalculator**

Calcula o WACC (Weighted Average Cost of Capital):

- **Método principal:**
  - `calcular_wacc()` → Custo médio ponderado de capital

**Fórmula:**
```
WACC = (E/V) * Re + (D/V) * Rd * (1 - Tc)

Onde:
- E = Valor do Patrimônio
- D = Valor da Dívida  
- V = Valor Total (E + D)
- Re = Custo do Patrimônio (calculado via CAPM)
- Rd = Custo da Dívida
- Tc = Taxa de Impostos
```

- **Análises adicionais:**
  - Análise de sensibilidade de beta
  - Impacto da alavancagem no WACC
  - Cenários de mudança de D/E ratio

### `src/prediction.py`
**Classe: PredictorWACC** ⭐ *Algoritmo de Previsão*

Implementa modelo de **regressão polinomial** para prever WACC:

- **Características:**
  - Treina com dados históricos de múltiplas empresas
  - Gera previsões de WACC para diferentes D/E ratios
  - Calcula intervalos de confiança (95%)
  - Encontra D/E ratio que minimiza WACC

- **Métodos principais:**
  - `gerar_dados_treino()` → Simula dados de estruturas de capital
  - `treinar()` → Treina modelo com Regressão Polinomial
  - `prever()` → Prevê WACC para dado D/E ratio
  - `intervalo_confianca()` → Calcula IC 95%
  - `encontrar_minimo_wacc()` → D/E que minimiza WACC

**Modelo:**
```
WACC = β₀ + β₁*(D/E) + β₂*(D/E)² + ε
```

- Grau do polinômio: 2 (parabólico)
- Métrica de ajuste: R² Score e RMSE

### `src/optimization.py`
**Classe: CapitalStructureOptimizer**

Otimiza estrutura de capital usando algoritmos numéricos:

- **Métodos de otimização:**
  - SLSQP (Sequential Least Squares Programming)
  - Diferential Evolution (busca global)

- **Funcionalidade:**
  - Encontra D/E ratio ótimo que minimiza WACC
  - Análise de sensibilidade
  - Recomendações de restruturação

### `src/data_capture.py`
**Classe: DataCapture**

Gerencia captura e armazenamento de dados:

- **Funcionalidades:**
  - Captura dados via linha de comando
  - Carrega/salva em CSV
  - Validação de dados
  - Criação automática de dados de exemplo

### `src/report_generator.py`
**Classe: ReportGenerator**

Gera relatórios e visualizações:

- **Relatórios gerados:**
  - Texto: Análise completa da empresa
  - Gráficos PNG: WACC vs D/E, Métricas, Comparativo

- **Gráficos:**
  - Estrutura de Capital (pie chart)
  - Índices Financeiros (bar chart)
  - Composição de Ativos
  - Indicadores de Risco
  - Curva de otimização

### `src/main.py`
**Classe: MenuPrincipal**

Interface interativa com menu de 8 opções:

1. Inserir nova empresa
2. Listar empresas registradas
3. Analisar empresa específica
4. Gerar previsões com modelo
5. Otimizar estrutura de capital
6. Gerar relatório de empresa
7. Relatório comparativo
8. Sair

## 🔄 Fluxo de Dados

```
[Entrada: Captura Manual ou CSV]
           ↓
[DataCapture: Validação e Armazenamento]
           ↓
[CapitalStructure: Cálculos de Métricas]
           ↓
[WACCCalculator: Cálculo do WACC]
           ↓
[PredictorWACC: Treinamento e Previsão] ⭐
           ↓
[CapitalStructureOptimizer: Otimização]
           ↓
[ReportGenerator: Relatórios e Gráficos]
           ↓
[Saída: CSV, Texto, PNG]
```

## 📊 Dados de Entrada

Arquivo `data/companies_data.csv`:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| empresa | Nome da empresa | TechCorp |
| ativos_totais | Ativo total (R$) | 5000000 |
| divida_total | Dívida total (R$) | 1500000 |
| patrimonio | Patrimônio líquido (R$) | 3500000 |
| ebitda | EBITDA (R$) | 1000000 |
| taxa_imposto | Taxa de imposto (%) | 0.34 |
| taxa_juros_mercado | Taxa de juros mercado (%) | 0.06 |

## 📤 Dados de Saída

### 1. Arquivos Texto
`reports/*_relatorio_*.txt`
- Análise completa da empresa
- Todas as métricas calculadas
- WACC e cenários

### 2. Gráficos PNG
- `*_wacc_vs_de_*.png` → WACC vs D/E ratio
- `*_metricas_*.png` → Dashboard de métricas
- `relatorio_comparativo_*.png` → Comparação entre empresas
- `*_otimizacao_*.png` → Curva de otimização

### 3. Arquivo CSV
`reports/resultados_*.csv`
- Tabela de previsões
- D/E ratios e WACC previsto
- Intervalos de confiança

## 🎯 Requisitos Atendidos

✅ **Captura de dados**: Menu interativo ou CSV  
✅ **Algoritmo de previsão**: Regressão Polinomial com ML  
✅ **Código comentado**: Todos os módulos bem documentados  
✅ **Tema**: Estrutura de Capital (D/E ratio, WACC, otimização)  
✅ **Geração de relatórios**: Texto, gráficos e CSV  
✅ **Execução**: Menu interativo e script de teste  

## 🚀 Como Expandir

1. **Novos modelos de previsão:**
   - Adicione em `prediction.py`
   - Use sklearn para diferentes algoritmos

2. **Novos indicadores:**
   - Expanda `capital_structure.py` com mais métricas

3. **Mais otimizadores:**
   - Adicione em `optimization.py` (ex: algoritmos genéticos)

4. **Exportação PDF:**
   - Use `reportlab` (já nos requirements)

## 📚 Referências Acadêmicas

- **WACC**: Brealey, Myers & Allen (Corporate Finance)
- **Capital Structure**: Modigliani & Miller Theory
- **CAPM**: Sharpe (Capital Asset Pricing Model)
- **Otimização**: Boyd & Vandenberghe (Convex Optimization)
