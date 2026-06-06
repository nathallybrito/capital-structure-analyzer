# Como Usar a Aplicação

## 🚀 Quick Start (Início Rápido)

### 1. Instalação Rápida
```bash
cd capital-structure-analyzer
pip install -r requirements.txt
```

### 2. Executar a Aplicação
```bash
python src/main.py
```

### 3. Ou rodar o teste automático
```bash
python test_aplicacao.py
```

## 📖 Guia Passo-a-Passo

### **Cenário 1: Inserir uma Nova Empresa**

1. Execute `python src/main.py`
2. Escolha opção **[1] Inserir nova empresa**
3. Preencha os dados solicitados:
   - Nome da empresa
   - Ativo total (R$)
   - Dívida total (R$)
   - Patrimônio líquido (R$)
   - EBITDA (R$)
   - Taxa de imposto (default: 0.34)
   - Taxa de juros de mercado (default: 0.06)

**Exemplo:**
```
Nome da empresa: Empresa XYZ
Ativo total: 10000000
Dívida total: 3000000
Patrimônio: 7000000
EBITDA: 2000000
Taxa de imposto: 0.34
Taxa de juros: 0.06
```

### **Cenário 2: Analisar Estrutura de Capital**

1. No menu, escolha **[3] Analisar empresa específica**
2. Selecione a empresa por índice (0, 1, 2, etc.)
3. A aplicação exibirá:
   - Índices de estrutura de capital (D/A, D/E, E/A)
   - Custos e retornos (ROI, ROE, custo da dívida)
   - Indicadores de risco (Interest Coverage)
   - WACC detalhado com análise de cenários

### **Cenário 3: Prever WACC com Machine Learning**

1. Escolha **[4] Gerar previsões (Modelo de Regressão)**
2. O modelo será treinado automaticamente com:
   - Dados das empresas registradas
   - Simulação de 30 variações de D/E ratio por empresa
   - Regressão polinomial de grau 2

3. Resultados exibidos:
   - Desempenho do modelo (R², RMSE)
   - **D/E ratio ótimo que minimiza WACC**
   - **Tabela de previsões** com intervalos de confiança

4. Digite um D/E ratio específico para prever seu WACC:
   ```
   Digite um D/E ratio para previsão: 0.5
   
   D/E Ratio: 0.5000
   WACC Previsto: 8.75%
   Intervalo de Confiança (95%): [8.52%, 8.98%]
   ```

### **Cenário 4: Otimizar Estrutura de Capital**

1. Escolha **[5] Otimizar estrutura de capital**
2. Selecione a empresa
3. A otimização encontrará:
   - **D/E ratio ótimo** que minimiza WACC
   - Economia de WACC possível
   - Mudança percentual necessária em dívida
   - Recomendações práticas
   - Gráfico de sensibilidade

**Exemplo de resultado:**
```
D/E Ratio Ótimo: 0.45
WACC Mínimo: 8.20%

Economia de WACC: 1.35%

RECOMENDAÇÃO:
⬇️ REDUZIR DÍVIDA: Reduzir o D/E ratio pode reduzir o WACC em 1.35%.
   Diminua a alavancagem de 0.625 para 0.450.
```

### **Cenário 5: Gerar Relatório Completo**

1. Escolha **[6] Gerar relatório de empresa**
2. Selecione a empresa
3. Serão gerados 3 arquivos em `reports/`:
   - **Relatório em texto** (.txt)
   - **Gráfico WACC vs D/E** (.png)
   - **Dashboard de métricas** (.png)

### **Cenário 6: Comparar Múltiplas Empresas**

1. Escolha **[7] Relatório comparativo entre empresas**
2. Será gerado um gráfico comparativo mostrando:
   - D/E ratio de cada empresa
   - WACC de cada empresa
   - ROE e Interest Coverage
   - Comparação lado-a-lado

## 💡 Exemplos Práticos

### Exemplo: Análise de TechCorp

```bash
$ python src/main.py
[3]
0
```

**Saída:**
```
═══════════════════════════════════════════════════════════
ANÁLISE DE ESTRUTURA DE CAPITAL - TECHCORP
═══════════════════════════════════════════════════════════

DADOS FINANCEIROS:
  Ativo Total:                    R$ 5,000,000.00
  Dívida Total:                   R$ 1,500,000.00
  Patrimônio Líquido:             R$ 3,500,000.00
  EBITDA:                         R$ 1,000,000.00

ÍNDICES DE ESTRUTURA DE CAPITAL:
  Leverage Ratio (D/A):           0.3000 (30.00%)
  Debt-to-Equity (D/E):           0.4286
  Equity Ratio (E/A):             0.7000 (70.00%)
  Alavancagem Financeira:         1.4286x

CUSTOS E RETORNOS:
  Custo da Dívida (Rd):           0.0606 (6.06%)
  ROI (Retorno s/ Investimento):  0.2000 (20.00%)
  ROE (Retorno s/ Patrimônio):    0.4023 (40.23%)

INDICADORES DE RISCO:
  Interest Coverage:              7.75x
  ✓ Saudável
```

### Exemplo: Previsão de WACC

```bash
[4]

Modelo treinado com R² = 0.9234

D/E Ratio Ótimo:                 0.5234
WACC Mínimo Previsto:            8.15%

Digite um D/E ratio para previsão: 0.5
D/E Ratio: 0.5000
WACC Previsto: 8.18%
Intervalo de Confiança (95%): [8.05%, 8.31%]
Margem de Erro: ±0.13%
```

## 📊 Interpretando os Resultados

### D/E Ratio (Dívida/Patrimônio)
- **< 0.5**: Estrutura conservadora (baixo risco, menor retorno)
- **0.5 - 1.0**: Estrutura equilibrada (recomendado para maioria)
- **1.0 - 2.0**: Estrutura agressiva (maior risco e retorno)
- **> 2.0**: Estrutura muito agressiva (alto risco de insolvência)

### WACC (Weighted Average Cost of Capital)
- Quanto menor, melhor (reduz custo de capital)
- Tipicamente entre 6% - 12% para empresas saudáveis
- A otimização busca minimizar este valor

### Interest Coverage (Cobertura de Juros)
- **> 2.5x**: ✓ Saudável (pode cobrir juros 2.5 vezes)
- **1.5 - 2.5x**: ⚠️ Atenção (algum risco)
- **< 1.5x**: ❌ Crítico (dificuldade em pagar juros)

## 🔍 Validação de Dados

A aplicação valida automaticamente:

✅ Valores positivos  
✅ Consistência entre Ativo, Dívida e Patrimônio  
✅ EBITDA realista (entre 5% e 30% do ativo)  
✅ Índices de solvência adequados  

## 📁 Arquivos Gerados

```
reports/
├── TechCorp_relatorio_20260606_143025.txt
├── TechCorp_wacc_vs_de_20260606_143025.png
├── TechCorp_metricas_20260606_143025.png
└── relatorio_comparativo_20260606_143030.png

data/
└── companies_data.csv (atualizado automaticamente)
```

## ⚙️ Configurações Avançadas

### Ajustar Beta (Risco Sistemático)

Em `src/wacc_calculator.py`, linha ~40:
```python
wacc = wacc_calc.calcular_wacc(beta=1.2)  # Altere para seu beta
```

### Mudar Grau do Polinômio de Previsão

Em `src/main.py`, linha ~20:
```python
self.predictor = PredictorWACC(grau_polinomio=3)  # Grau 2, 3, ou 4
```

### Ajustar Limites de Otimização

Em `src/main.py`, função `otimizar_empresa()`:
```python
restricoes={'min': 0.1, 'max': 2.5}  # Altere os limites de D/E
```

## 🆘 Troubleshooting

### Erro: "No module named 'pandas'"
```bash
pip install --upgrade pandas
```

### Erro ao gerar gráficos
```bash
pip install --upgrade matplotlib seaborn
```

### Erro de arquivo não encontrado
```bash
python src/main.py  # Execute da raiz do projeto
```

## 📞 Suporte

Para dúvidas sobre:
- **Estrutura do código**: Veja `ESTRUTURA.md`
- **Instalação**: Veja `INSTALACAO.md`
- **Algoritmos**: Veja comentários no código (bem documentados)

---

**Desenvolvido para:** Trabalho 2 - Administração Financeira (CAD 167)  
**Disciplina:** Administração Financeira  
**UFMG** - Faculdade de Ciências Econômicas - 2026
