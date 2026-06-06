# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.0.0] - 2026-06-06

### ✨ Adicionado
- **Análise de Estrutura de Capital**: Cálculos completos de D/A, D/E, E/A ratios
- **Cálculo de WACC**: Weighted Average Cost of Capital com CAPM
- **Modelo de Previsão**: Regressão Polinomial para prever WACC
- **Otimização**: Encontra D/E ratio ótimo que minimiza WACC
- **Captura de Dados**: Menu interativo e carregamento CSV
- **Geração de Relatórios**: Texto, gráficos PNG e CSV
- **Interface Interativa**: Menu principal com 8 opções
- **Análise Comparativa**: Compara múltiplas empresas
- **Dados de Exemplo**: 5 empresas pré-carregadas

### 📚 Documentação
- README.md com documentação completa
- INSTALACAO.md com guia passo-a-passo
- COMO_USAR.md com 6 cenários práticos
- ESTRUTURA.md com documentação técnica
- SUMARIO_ENTREGA.md com checklist de requisitos
- CHANGELOG.md (este arquivo)

### 🔧 Componentes Técnicos

#### Módulos Python (7)
1. `capital_structure.py` - Classe CapitalStructure (9 métodos)
2. `wacc_calculator.py` - Classe WACCCalculator (7 métodos)
3. `prediction.py` - Classe PredictorWACC com ML (7 métodos)
4. `optimization.py` - Classe CapitalStructureOptimizer (5 métodos)
5. `data_capture.py` - Classe DataCapture (6 métodos)
6. `report_generator.py` - Classe ReportGenerator (5 métodos)
7. `main.py` - Classe MenuPrincipal com interface

#### Dependências (6)
- numpy: Cálculos numéricos
- pandas: Manipulação de dados
- scipy: Otimização numérica
- scikit-learn: Machine Learning
- matplotlib: Visualizações
- seaborn: Estilo de gráficos

### 📊 Funcionalidades

#### Cálculos
- [x] D/A Ratio (Alavancagem)
- [x] D/E Ratio (Estrutura de Capital)
- [x] E/A Ratio (Índice de Patrimônio)
- [x] WACC (Custo Médio de Capital)
- [x] ROE (Retorno sobre Patrimônio)
- [x] ROI (Retorno sobre Investimento)
- [x] Interest Coverage (Cobertura de Juros)

#### Análises
- [x] Sensibilidade de beta
- [x] Impacto de alavancagem
- [x] Simulação de cenários
- [x] Previsão com ML
- [x] Otimização numérica

#### Relatórios
- [x] Relatório textual formatado
- [x] Gráfico WACC vs D/E
- [x] Dashboard de métricas (2x2)
- [x] Gráfico de otimização
- [x] Relatório comparativo
- [x] Tabela de previsões CSV

### 🎓 Conceitos Implementados
- [x] Estrutura de Capital (Modigliani-Miller)
- [x] CAPM (Capital Asset Pricing Model)
- [x] Regressão Polinomial
- [x] Otimização numérica (SLSQP)
- [x] Intervalos de confiança

---

## Notas de Versão

### v1.0.0 - Release Inicial
- Implementação completa do projeto Trabalho 2 (CAD 167)
- Todos os requisitos acadêmicos atendidos
- Documentação extensiva (1500+ linhas)
- Pronto para apresentação e GitHub

### Requisitos Atendidos ✅
- [x] Execução da aplicação
- [x] Captura de dados
- [x] Descrição em comentários do código
- [x] Geração de relatórios
- [x] Algoritmo de previsão
- [x] Tema: Estrutura de Capital

---

## Roadmap Futuro (Opcional)

### v1.1.0
- [ ] Exportação em PDF
- [ ] Dashboard web com Flask/Django
- [ ] Análise de série temporal
- [ ] Conexão com API de dados reais

### v1.2.0
- [ ] Suporte a múltiplas moedas
- [ ] Análise de risco de crédito
- [ ] Simulação de Monte Carlo
- [ ] Alertas de limite de solvência

### v2.0.0
- [ ] Interface gráfica (GUI)
- [ ] Base de dados (SQLite/PostgreSQL)
- [ ] API REST
- [ ] Análise de cenários avançada

---

## Contribuições

Este projeto foi desenvolvido como trabalho acadêmico.

**Desenvolvido para:**
- Disciplina: Administração Financeira (CAD 167)
- Curso: Sistemas de Informação
- Universidade: UFMG
- Período: 1º Semestre de 2026

---

## Licença

MIT License - Veja LICENSE para detalhes.

---

Última atualização: 2026-06-06
