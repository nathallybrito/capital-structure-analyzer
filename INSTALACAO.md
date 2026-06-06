# Guia de Instalação

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Passos de Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/capital-structure-analyzer.git
cd capital-structure-analyzer
```

### 2. Crie um ambiente virtual (recomendado)

#### No Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## Execução

### Interface Interativa

```bash
python src/main.py
```

Esta será a forma principal de usar a aplicação. Você terá um menu interativo com as seguintes opções:

1. **Inserir nova empresa** - Captura dados financeiros de uma empresa via linha de comando
2. **Listar empresas** - Exibe todas as empresas registradas
3. **Analisar empresa** - Calcula e exibe métricas de estrutura de capital e WACC
4. **Gerar previsões** - Treina modelo de regressão e prevê WACC para diferentes D/E ratios
5. **Otimizar estrutura** - Encontra o D/E ratio que minimiza o WACC
6. **Gerar relatório** - Cria relatórios em texto e gráficos
7. **Relatório comparativo** - Compara múltiplas empresas
8. **Sair** - Encerra o programa

### Script de Teste

Para testar rapidamente a aplicação sem usar o menu interativo:

```bash
python test_aplicacao.py
```

Este script vai:
- Criar uma empresa de teste
- Calcular todas as métricas
- Gerar previsões com modelo de regressão
- Otimizar a estrutura de capital
- Gerar relatórios e gráficos

## Estrutura de Dados

Os dados das empresas são armazenados em CSV em `data/companies_data.csv`:

```csv
empresa,ativos_totais,divida_total,patrimonio,ebitda,taxa_imposto,taxa_juros_mercado
TechCorp,5000000,1500000,3500000,1000000,0.34,0.06
```

## Relatórios Gerados

Os relatórios e gráficos são salvos em `reports/`:

- `{empresa}_relatorio_{timestamp}.txt` - Relatório em texto
- `{empresa}_wacc_vs_de_{timestamp}.png` - Gráfico WACC vs D/E
- `{empresa}_metricas_{timestamp}.png` - Gráfico de métricas
- `relatorio_comparativo_{timestamp}.png` - Comparação entre empresas

## Solução de Problemas

### Erro: "No module named 'pandas'"

Execute:
```bash
pip install pandas --upgrade
```

### Erro ao gerar gráficos

Certifique-se de que matplotlib está instalado:
```bash
pip install matplotlib --upgrade
```

### Erro de ambiente virtual

No Windows, se `venv\Scripts\activate` não funcionar:
```bash
python -m venv venv --clear
```

## Dependências

| Pacote | Versão | Uso |
|--------|--------|-----|
| numpy | >=1.26.0 | Cálculos numéricos |
| pandas | >=2.2.0 | Manipulação de dados e CSV |
| scipy | >=1.12.0 | Otimização numérica |
| scikit-learn | >=1.4.0 | Machine Learning (regressão) |
| matplotlib | >=3.8.0 | Geração de gráficos |
| seaborn | >=0.13.0 | Estilo de gráficos |
| reportlab | >=4.1.0 | Geração de PDF (opcional) |

## Requisitos do Sistema

- **RAM**: Mínimo 2GB
- **Espaço em disco**: ~500MB (incluindo dependências)
- **Processador**: Qualquer processador moderno
- **SO**: Windows, Linux, macOS

## Suporte

Para problemas ou dúvidas, abra uma issue no repositório GitHub.
