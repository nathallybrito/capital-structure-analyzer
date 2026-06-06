"""
Script de teste para demonstrar o funcionamento da aplicação.
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from capital_structure import CapitalStructure
from wacc_calculator import WACCCalculator
from prediction import PredictorWACC
from optimization import CapitalStructureOptimizer
from report_generator import ReportGenerator


def teste_completo():
    """Executa teste completo da aplicação."""
    print("="*70)
    print("TESTE COMPLETO DA APLICAÇÃO".center(70))
    print("="*70)

    # 1. Criar empresa de teste
    print("\n[1] CRIANDO EMPRESA DE TESTE...")
    empresa = CapitalStructure(
        empresa_nome="TechCorp Brasil",
        ativos_totais=5000000,
        divida_total=1500000,
        patrimonio=3500000,
        ebitda=1000000,
        taxa_imposto=0.34,
        taxa_juros_mercado=0.06
    )
    print("✓ Empresa criada com sucesso!")

    # 2. Calcular métricas de estrutura de capital
    print("\n[2] CALCULANDO MÉTRICAS DE ESTRUTURA DE CAPITAL...")
    print(empresa.relatorio_metricas())

    # 3. Calcular WACC
    print("\n[3] CALCULANDO WACC...")
    wacc_calc = WACCCalculator(empresa)
    print(wacc_calc.relatorio_wacc())

    # 4. Gerar previsões
    print("\n[4] GERANDO PREVISÕES COM MODELO DE REGRESSÃO...")

    # Cria mais empresas para treino
    empresas_treino = [
        empresa,
        CapitalStructure(
            empresa_nome="RetailCo",
            ativos_totais=10000000,
            divida_total=4000000,
            patrimonio=6000000,
            ebitda=1500000
        ),
        CapitalStructure(
            empresa_nome="ManufExcel",
            ativos_totais=8000000,
            divida_total=2500000,
            patrimonio=5500000,
            ebitda=1200000
        )
    ]

    predictor = PredictorWACC(grau_polinomio=2)
    predictor.gerar_dados_treino(empresas_treino, WACCCalculator)
    predictor.treinar(predictor.X_treino, predictor.y_treino)

    print(predictor.relatorio_previsao())

    # 5. Otimizar estrutura de capital
    print("\n[5] OTIMIZANDO ESTRUTURA DE CAPITAL...")
    optimizer = CapitalStructureOptimizer(wacc_calc)
    resultado = optimizer.otimizar(metodo='SLSQP')
    print(optimizer.relatorio_otimizacao())

    # 6. Gerar relatórios
    print("\n[6] GERANDO RELATÓRIOS E GRÁFICOS...")
    report_gen = ReportGenerator()
    report_gen.gerar_relatorio_empresa(empresa, wacc_calc)
    report_gen.gerar_grafico_wacc_vs_de(wacc_calc)
    report_gen.gerar_grafico_metricas(empresa)
    report_gen.gerar_relatorio_comparativo(empresas_treino, [WACCCalculator(e) for e in empresas_treino])

    print("\n" + "="*70)
    print("✓ TESTE CONCLUÍDO COM SUCESSO!".center(70))
    print("="*70)
    print("\nPróximos passos:")
    print("1. Execute 'python src/main.py' para usar a interface interativa")
    print("2. Verifique os relatórios em 'reports/'")
    print("3. Submeta o projeto no GitHub")


if __name__ == "__main__":
    try:
        teste_completo()
    except Exception as e:
        print(f"\n❌ ERRO DURANTE O TESTE: {e}")
        import traceback
        traceback.print_exc()
