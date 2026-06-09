"""
Programa Principal - Analisador de Estrutura de Capital.

Interface interativa para análise e otimização de estrutura de capital.
Trabalho 2 - Administração Financeira (CAD 167) - UFMG - 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from capital_structure import CapitalStructure
from wacc_calculator import WACCCalculator
from prediction import PredictorWACC
from optimization import CapitalStructureOptimizer
from data_capture import DataCapture
from report_generator import ReportGenerator


class MenuPrincipal:
    """Gerencia a interface interativa do programa."""

    def __init__(self):
        """Inicializa o menu e componentes do programa."""
        self.data_capture = DataCapture()
        self.report_gen = ReportGenerator()
        self.predictor = PredictorWACC(grau_polinomio=2)

        # Cria dados de exemplo se não existirem
        if not self.data_capture.empresas:
            self.data_capture.criar_dados_exemplo()

    def exibir_cabecalho(self):
        """Exibe o cabeçalho do programa."""
        print("\n" + "="*70)
        print("ANALISADOR DE ESTRUTURA DE CAPITAL".center(70))
        print("Administração Financeira - CAD 167 - UFMG - 2026".center(70))
        print("="*70)

    def menu_principal(self):
        """Menu principal da aplicação."""
        while True:
            self.exibir_cabecalho()
            print("\n[1] Inserir nova empresa")
            print("[2] Listar empresas registradas")
            print("[3] Analisar empresa específica")
            print("[4] Gerar previsões (Modelo de Regressão)")
            print("[5] Otimizar estrutura de capital")
            print("[6] Gerar relatório de empresa")
            print("[7] Relatório comparativo entre empresas")
            print("[8] Sair")

            opcao = input("\nEscolha uma opção (1-8): ").strip()

            if opcao == '1':
                self.inserir_empresa()
            elif opcao == '2':
                self.data_capture.listar_empresas()
            elif opcao == '3':
                self.analisar_empresa()
            elif opcao == '4':
                self.gerar_previsoes()
            elif opcao == '5':
                self.otimizar_empresa()
            elif opcao == '6':
                self.gerar_relatorio()
            elif opcao == '7':
                self.relatorio_comparativo()
            elif opcao == '8':
                print("\n✓ Até logo!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")

            input("\nPressione ENTER para continuar...")

    def inserir_empresa(self):
        """Menu para inserir nova empresa."""
        empresa = self.data_capture.capturar_empresa_manual()
        if empresa:
            # Treina novamente o modelo de previsão com a nova empresa
            if len(self.data_capture.empresas) >= 2:
                self.predictor.gerar_dados_treino(self.data_capture.empresas, WACCCalculator)
                self.predictor.treinar(self.predictor.X_treino, self.predictor.y_treino)

    def analisar_empresa(self):
        """Menu para analisar uma empresa específica."""
        self.data_capture.listar_empresas()

        if not self.data_capture.empresas:
            return

        try:
            indice = int(input("\nDigite o número da empresa (0 para primeira): "))
            empresa = self.data_capture.empresas[indice]
        except (ValueError, IndexError):
            print("❌ Índice inválido.")
            return

        print(empresa.relatorio_metricas())

        # Calcula WACC
        wacc_calc = WACCCalculator(empresa)
        print(wacc_calc.relatorio_wacc())

        # Oferece opções adicionais
        print("\nOpções adicionais:")
        print("[1] Gerar gráficos")
        print("[2] Retornar ao menu")

        opcao = input("Escolha: ").strip()
        if opcao == '1':
            self.report_gen.gerar_grafico_wacc_vs_de(wacc_calc)
            self.report_gen.gerar_grafico_metricas(empresa)

    def gerar_previsoes(self):
        """Menu para gerar previsões com modelo de regressão."""
        if len(self.data_capture.empresas) < 2:
            print("❌ Necessário pelo menos 2 empresas para gerar previsões.")
            print(f"   Empresas registradas: {len(self.data_capture.empresas)}")
            return

        print("\n📊 Treinando modelo de previsão...")

        # Treina modelo
        self.predictor.gerar_dados_treino(self.data_capture.empresas, WACCCalculator)
        self.predictor.treinar(self.predictor.X_treino, self.predictor.y_treino)

        print(self.predictor.relatorio_previsao())

        # Oferece previsão para D/E específico
        while True:
            try:
                d_e_input = input("\nDigite um D/E ratio para previsão (ou 'sair'): ").strip()
                if d_e_input.lower() == 'sair':
                    break

                d_e = float(d_e_input)
                wacc_pred, ic_lower, ic_upper = self.predictor.intervalo_confianca(d_e)

                print(f"\n{'─'*50}")
                print(f"D/E Ratio: {d_e:.4f}")
                print(f"WACC Previsto: {wacc_pred*100:.2f}%")
                print(f"Intervalo de Confiança (95%): [{ic_lower*100:.2f}%, {ic_upper*100:.2f}%]")
                print(f"Margem de Erro: ±{(ic_upper - wacc_pred)*100:.2f}%")
                print(f"{'─'*50}")

            except ValueError:
                print("❌ Valor inválido. Digite um número.")

    def otimizar_empresa(self):
        """Menu para otimizar estrutura de capital de uma empresa."""
        self.data_capture.listar_empresas()

        if not self.data_capture.empresas:
            return

        try:
            indice = int(input("\nDigite o número da empresa para otimizar [0 - n]: "))
            empresa = self.data_capture.empresas[indice]
        except (ValueError, IndexError):
            print("❌ Índice inválido.")
            return

        print(f"\n🔄 Otimizando estrutura de capital para {empresa.empresa_nome}...")

        wacc_calc = WACCCalculator(empresa)
        optimizer = CapitalStructureOptimizer(wacc_calc)

        # Executa otimização
        resultado = optimizer.otimizar(metodo='SLSQP')

        print(optimizer.relatorio_otimizacao())

        # Gera gráfico
        print("\n📊 Gerando gráfico de sensibilidade...")
        sensibilidade = optimizer.analise_sensibilidade()

        import matplotlib.pyplot as plt
        import numpy as np
        from datetime import datetime

        d_e_vals = [s[0] for s in sensibilidade]
        wacc_vals = [s[1] * 100 for s in sensibilidade]

        fig, ax = plt.subplots(figsize=(12, 7))
        ax.plot(d_e_vals, wacc_vals, 'b-', linewidth=2.5, label='Curva WACC')
        ax.axvline(resultado['d_e_otimo'], color='red', linestyle='--', linewidth=2,
                  label=f"D/E Ótimo: {resultado['d_e_otimo']:.3f}")
        ax.plot(resultado['d_e_otimo'], resultado['wacc_minimo']*100, 'r*', markersize=20,
               label=f"Ponto Ótimo: {resultado['wacc_minimo']*100:.2f}%")

        ax.set_xlabel('Debt-to-Equity Ratio', fontsize=12, fontweight='bold')
        ax.set_ylabel('WACC (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Otimização de Estrutura de Capital - {empresa.empresa_nome}',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = f"reports/{empresa.empresa_nome.replace(' ', '_')}_otimizacao_{timestamp}.png"
        os.makedirs('reports', exist_ok=True)
        plt.tight_layout()
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Gráfico salvo em: {caminho}")

    def gerar_relatorio(self):
        """Menu para gerar relatório de uma empresa."""
        self.data_capture.listar_empresas()

        if not self.data_capture.empresas:
            return

        try:
            indice = int(input("\nDigite o número da empresa [0 - n]: "))
            empresa = self.data_capture.empresas[indice]
        except (ValueError, IndexError):
            print("❌ Índice inválido.")
            return

        print(f"\n📄 Gerando relatórios para {empresa.empresa_nome}...")

        wacc_calc = WACCCalculator(empresa)

        # Gera relatório em texto
        self.report_gen.gerar_relatorio_empresa(empresa, wacc_calc)

        # Gera gráficos
        self.report_gen.gerar_grafico_wacc_vs_de(wacc_calc)
        self.report_gen.gerar_grafico_metricas(empresa)

        print("✓ Todos os relatórios foram gerados com sucesso!")

    def relatorio_comparativo(self):
        """Menu para gerar relatório comparativo."""
        if len(self.data_capture.empresas) < 2:
            print("❌ Necessário pelo menos 2 empresas para comparação.")
            return

        print("\n📊 Gerando relatório comparativo...")

        wacc_calcs = [WACCCalculator(empresa) for empresa in self.data_capture.empresas]
        self.report_gen.gerar_relatorio_comparativo(self.data_capture.empresas, wacc_calcs)

        print("✓ Relatório comparativo gerado com sucesso!")


def main():
    """Função principal do programa."""
    try:
        menu = MenuPrincipal()
        menu.menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
