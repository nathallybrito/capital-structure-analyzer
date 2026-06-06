"""
Módulo de Geração de Relatórios.

Gera relatórios em texto e visualizações gráficas.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np


class ReportGenerator:
    """Gera relatórios de análise de estrutura de capital."""

    def __init__(self, pasta_relatorios='reports'):
        """
        Inicializa o gerador de relatórios.

        Args:
            pasta_relatorios: Pasta onde salvar os relatórios
        """
        self.pasta = pasta_relatorios
        os.makedirs(self.pasta, exist_ok=True)
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 9

    def gerar_relatorio_empresa(self, capital_structure, wacc_calculator, nome_arquivo=None):
        """
        Gera relatório completo de uma empresa.

        Args:
            capital_structure: Objeto CapitalStructure
            wacc_calculator: Objeto WACCCalculator
            nome_arquivo: Nome do arquivo (sem extensão)

        Returns:
            str: Caminho do arquivo gerado
        """
        if not nome_arquivo:
            nome_arquivo = capital_structure.empresa_nome.replace(' ', '_')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(self.pasta, f"{nome_arquivo}_relatorio_{timestamp}.txt")

        conteudo = f"""
{'='*70}
RELATÓRIO DE ANÁLISE DE ESTRUTURA DE CAPITAL
{'='*70}

Empresa: {capital_structure.empresa_nome}
Data: {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}

{capital_structure.relatorio_metricas()}

{wacc_calculator.relatorio_wacc()}

{'='*70}
FIM DO RELATÓRIO
{'='*70}
        """

        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print(f"✓ Relatório salvo em: {caminho}")
        return caminho

    def gerar_grafico_wacc_vs_de(self, wacc_calculator, nome_arquivo=None):
        """
        Gera gráfico WACC vs D/E ratio.

        Args:
            wacc_calculator: Objeto WACCCalculator
            nome_arquivo: Nome do arquivo (sem extensão)

        Returns:
            str: Caminho do arquivo gerado
        """
        if not nome_arquivo:
            nome_arquivo = wacc_calculator.cs.empresa_nome.replace(' ', '_')

        # Gera dados
        d_e_valores = np.linspace(0.1, 3.0, 50)
        wacc_valores = []

        for d_e in d_e_valores:
            novo_d = d_e * wacc_calculator.cs.patrimonio
            novo_v = novo_d + wacc_calculator.cs.patrimonio

            peso_e = wacc_calculator.cs.patrimonio / novo_v
            peso_d = novo_d / novo_v

            beta_ajustado = 1.2 * (1 + (1 - wacc_calculator.cs.taxa_imposto) * d_e)
            re = 0.045 + beta_ajustado * 0.07
            rd = wacc_calculator.cs.taxa_juros_mercado + min(0.03 * d_e, 0.12)

            wacc = (peso_e * re) + (peso_d * rd * (1 - wacc_calculator.cs.taxa_imposto))
            wacc_valores.append(wacc)

        # Cria figura
        fig, ax = plt.subplots(figsize=(12, 7))

        ax.plot(d_e_valores, np.array(wacc_valores) * 100, 'b-', linewidth=2.5, label='WACC')
        ax.axvline(wacc_calculator.cs.debt_to_equity(), color='green', linestyle='--',
                   linewidth=2, label=f"D/E Atual: {wacc_calculator.cs.debt_to_equity():.3f}")

        wacc_atual = wacc_calculator.calcular_wacc()
        ax.plot(wacc_calculator.cs.debt_to_equity(), wacc_atual * 100, 'go', markersize=10)

        ax.set_xlabel('Debt-to-Equity (D/E) Ratio', fontsize=12, fontweight='bold')
        ax.set_ylabel('WACC (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Análise de WACC vs D/E Ratio - {wacc_calculator.cs.empresa_nome}',
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        ax.set_ylim(bottom=0)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(self.pasta, f"{nome_arquivo}_wacc_vs_de_{timestamp}.png")
        plt.tight_layout()
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Gráfico salvo em: {caminho}")
        return caminho

    def gerar_grafico_metricas(self, capital_structure, nome_arquivo=None):
        """
        Gera gráfico com principais métricas.

        Args:
            capital_structure: Objeto CapitalStructure
            nome_arquivo: Nome do arquivo (sem extensão)

        Returns:
            str: Caminho do arquivo gerado
        """
        if not nome_arquivo:
            nome_arquivo = capital_structure.empresa_nome.replace(' ', '_')

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # Gráfico 1: Estrutura de Capital
        ax1 = axes[0, 0]
        estrutura = [capital_structure.divida_total, capital_structure.patrimonio]
        cores = ['#ff9999', '#99ccff']
        wedges, texts, autotexts = ax1.pie(estrutura, labels=['Dívida', 'Patrimônio'],
                                            autopct='%1.1f%%', colors=cores, startangle=90)
        ax1.set_title('Estrutura de Capital\n(D/E: {:.3f})'.format(capital_structure.debt_to_equity()),
                      fontweight='bold')

        # Gráfico 2: Índices Financeiros
        ax2 = axes[0, 1]
        indices = {
            'D/A': capital_structure.leverage_ratio(),
            'E/A': capital_structure.equity_ratio(),
            'ROI': capital_structure.roi(),
            'ROE': capital_structure.roe()
        }
        ax2.bar(indices.keys(), indices.values(), color=['#ff9999', '#99ccff', '#99ff99', '#ffcc99'])
        ax2.set_title('Índices Financeiros', fontweight='bold')
        ax2.set_ylabel('Valor')
        ax2.grid(axis='y', alpha=0.3)

        # Gráfico 3: Composição de Ativos
        ax3 = axes[1, 0]
        ativos_info = {
            'Total': capital_structure.ativos_totais,
            'Financiado por\nDívida': capital_structure.divida_total,
            'Financiado por\nPatrimônio': capital_structure.patrimonio
        }
        ax3.bar(ativos_info.keys(), [v/1e6 for v in ativos_info.values()],
                color=['#999999', '#ff9999', '#99ccff'])
        ax3.set_title('Composição de Ativos (em milhões)', fontweight='bold')
        ax3.set_ylabel('Valor (R$ Milhões)')
        ax3.grid(axis='y', alpha=0.3)

        # Gráfico 4: Indicadores de Risco
        ax4 = axes[1, 1]
        indicadores = {
            'Interest\nCoverage': min(capital_structure.interest_coverage(), 10),
            'Alavancagem\nFinanceira': min(capital_structure.alavancagem_financeira(), 10)
        }
        cores_risco = ['green' if v > 2.5 else 'orange' if v > 1.5 else 'red'
                       for v in indicadores.values()]
        ax4.bar(indicadores.keys(), indicadores.values(), color=cores_risco)
        ax4.axhline(y=2.5, color='green', linestyle='--', label='Zona Saudável')
        ax4.axhline(y=1.5, color='orange', linestyle='--', label='Zona de Atenção')
        ax4.set_title('Indicadores de Risco', fontweight='bold')
        ax4.set_ylabel('Valor')
        ax4.legend(fontsize=8)
        ax4.grid(axis='y', alpha=0.3)

        plt.suptitle(f'Análise Completa - {capital_structure.empresa_nome}',
                     fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(self.pasta, f"{nome_arquivo}_metricas_{timestamp}.png")
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Gráfico salvo em: {caminho}")
        return caminho

    def gerar_relatorio_comparativo(self, empresas_lista, wacc_calculator_list, nome_arquivo=None):
        """
        Gera relatório comparativo entre múltiplas empresas.

        Args:
            empresas_lista: Lista de objetos CapitalStructure
            wacc_calculator_list: Lista de objetos WACCCalculator
            nome_arquivo: Nome do arquivo (sem extensão)

        Returns:
            str: Caminho do arquivo gerado
        """
        if not nome_arquivo:
            nome_arquivo = "relatorio_comparativo"

        # Prepara dados
        dados = []
        for cs, wacc_calc in zip(empresas_lista, wacc_calculator_list):
            dados.append({
                'Empresa': cs.empresa_nome,
                'D/E Ratio': cs.debt_to_equity(),
                'D/A Ratio': cs.leverage_ratio(),
                'WACC': wacc_calc.calcular_wacc(),
                'ROE': cs.roe(),
                'Interest Coverage': cs.interest_coverage()
            })

        df = pd.DataFrame(dados)

        # Cria figura com tabela
        fig, ax = plt.subplots(figsize=(14, len(empresas_lista) * 0.6 + 2))
        ax.axis('tight')
        ax.axis('off')

        # Formata dados para exibição
        df_display = df.copy()
        for col in ['D/E Ratio', 'D/A Ratio', 'WACC', 'ROE']:
            df_display[col] = df_display[col].apply(lambda x: f'{x:.4f}')
        df_display['Interest Coverage'] = df_display['Interest Coverage'].apply(lambda x: f'{x:.2f}x')

        table = ax.table(cellText=df_display.values, colLabels=df_display.columns,
                        cellLoc='center', loc='center', bbox=[0, 0, 1, 1])

        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)

        # Estilo do header
        for i in range(len(df_display.columns)):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Cores alternadas
        for i in range(1, len(df_display) + 1):
            for j in range(len(df_display.columns)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
                else:
                    table[(i, j)].set_facecolor('#ffffff')

        plt.title('Relatório Comparativo de Estrutura de Capital', fontsize=14, fontweight='bold', pad=20)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(self.pasta, f"{nome_arquivo}_{timestamp}.png")
        plt.tight_layout()
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ Relatório comparativo salvo em: {caminho}")
        return caminho

    def salvar_csv_resultados(self, dados_list, nome_arquivo="resultados"):
        """
        Salva resultados em arquivo CSV.

        Args:
            dados_list: Lista de dicionários com dados
            nome_arquivo: Nome do arquivo (sem extensão)

        Returns:
            str: Caminho do arquivo gerado
        """
        df = pd.DataFrame(dados_list)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(self.pasta, f"{nome_arquivo}_{timestamp}.csv")

        df.to_csv(caminho, index=False, encoding='utf-8')
        print(f"✓ Dados salvos em: {caminho}")
        return caminho
