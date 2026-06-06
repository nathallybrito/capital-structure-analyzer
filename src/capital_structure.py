"""
Módulo de cálculos de Estrutura de Capital.

Realiza cálculos de índices e métricas relacionadas à estrutura de capital.
"""

class CapitalStructure:
    """Calcula métricas de estrutura de capital de uma empresa."""

    def __init__(self, empresa_nome, ativos_totais, divida_total, patrimonio,
                 ebitda, taxa_imposto=0.34, taxa_juros_mercado=0.06):
        """
        Inicializa os dados da empresa.

        Args:
            empresa_nome: Nome da empresa
            ativos_totais: Ativo total em reais
            divida_total: Dívida total em reais
            patrimonio: Patrimônio líquido em reais
            ebitda: EBITDA em reais
            taxa_imposto: Taxa de imposto sobre renda (default: 34%)
            taxa_juros_mercado: Taxa de juros de mercado (default: 6%)
        """
        self.empresa_nome = empresa_nome
        self.ativos_totais = ativos_totais
        self.divida_total = divida_total
        self.patrimonio = patrimonio
        self.ebitda = ebitda
        self.taxa_imposto = taxa_imposto
        self.taxa_juros_mercado = taxa_juros_mercado

        self.validar_dados()

    def validar_dados(self):
        """Valida se os dados estão consistentes."""
        # Patrimônio = Ativos - Dívidas (aproximadamente)
        diferenca = abs((self.ativos_totais - self.divida_total) - self.patrimonio)
        if diferenca > self.ativos_totais * 0.01:  # Tolerância de 1%
            print(f"⚠️ Aviso: Inconsistência nos dados de {self.empresa_nome}")
            print(f"  Ativos - Dívida = {self.ativos_totais - self.divida_total}")
            print(f"  Patrimônio informado = {self.patrimonio}")

    def leverage_ratio(self):
        """
        Calcula o Leverage Ratio (D/A).
        Indica a proporção de dívida em relação aos ativos totais.

        Returns:
            float: Razão D/A (entre 0 e 1)
        """
        return self.divida_total / self.ativos_totais if self.ativos_totais > 0 else 0

    def debt_to_equity(self):
        """
        Calcula a Razão Dívida/Patrimônio (D/E).
        Indica quantos reais de dívida para cada real de patrimônio.

        Returns:
            float: Razão D/E
        """
        return self.divida_total / self.patrimonio if self.patrimonio > 0 else 0

    def equity_ratio(self):
        """
        Calcula a Razão Patrimônio/Ativo (E/A).
        Indica a proporção de patrimônio em relação aos ativos.

        Returns:
            float: Razão E/A (entre 0 e 1)
        """
        return self.patrimonio / self.ativos_totais if self.ativos_totais > 0 else 0

    def alavancagem_financeira(self):
        """
        Calcula o grau de alavancagem financeira.
        Mostra quantas vezes o patrimônio é maior/menor que os ativos.

        Returns:
            float: Alavancagem financeira
        """
        e_a = self.equity_ratio()
        return 1 / e_a if e_a > 0 else 0

    def custo_divida_implicito(self):
        """
        Estima o custo implícito da dívida.
        Calcula a taxa de juros que a empresa paga sobre sua dívida.

        Returns:
            float: Taxa de custo da dívida (entre 0 e 1)
        """
        # Custo da dívida = (Taxa de juros mercado + Prêmio de risco de crédito)
        d_e = self.debt_to_equity()

        # Prêmio de risco aumenta com o D/E (mais dívida = mais risco)
        premio_risco = min(0.03 * d_e, 0.12)  # Máximo de 12% adicional

        custo_divida = self.taxa_juros_mercado + premio_risco
        return min(custo_divida, 0.20)  # Máximo de 20%

    def roi(self):
        """
        Calcula o Retorno sobre Investimento (ROI).
        ROI = EBITDA / Ativo Total

        Returns:
            float: ROI em percentual decimal
        """
        return self.ebitda / self.ativos_totais if self.ativos_totais > 0 else 0

    def interest_coverage(self):
        """
        Calcula o Índice de Cobertura de Juros.
        Indica quantas vezes o EBITDA cobre as despesas com juros.

        Returns:
            float: Índice de cobertura
        """
        despesa_juros = self.divida_total * self.custo_divida_implicito()
        return self.ebitda / despesa_juros if despesa_juros > 0 else float('inf')

    def roe(self):
        """
        Calcula o Retorno sobre Patrimônio (ROE).
        ROE = Lucro / Patrimônio
        Usa EBITDA como proxy para lucro (antes de juros e impostos).

        Returns:
            float: ROE em percentual decimal
        """
        lucro_operacional = self.ebitda - (self.divida_total * self.custo_divida_implicito())
        lucro_liquido = lucro_operacional * (1 - self.taxa_imposto)
        return lucro_liquido / self.patrimonio if self.patrimonio > 0 else 0

    def valor_empresa(self, taxa_desconto=0.10):
        """
        Estima o valor da empresa usando perpetuidade simples.
        Valor = EBITDA / Taxa de desconto

        Args:
            taxa_desconto: Taxa de desconto a utilizar (default: 10%)

        Returns:
            float: Valor estimado da empresa
        """
        return self.ebitda / taxa_desconto if taxa_desconto > 0 else 0

    def relatorio_metricas(self):
        """
        Gera um relatório formatado com todas as métricas.

        Returns:
            str: String com o relatório
        """
        d_e = self.debt_to_equity()

        relatorio = f"""
═══════════════════════════════════════════════════════════
ANÁLISE DE ESTRUTURA DE CAPITAL - {self.empresa_nome.upper()}
═══════════════════════════════════════════════════════════

DADOS FINANCEIROS:
  Ativo Total:                    R$ {self.ativos_totais:,.2f}
  Dívida Total:                   R$ {self.divida_total:,.2f}
  Patrimônio Líquido:             R$ {self.patrimonio:,.2f}
  EBITDA:                         R$ {self.ebitda:,.2f}

ÍNDICES DE ESTRUTURA DE CAPITAL:
  Leverage Ratio (D/A):           {self.leverage_ratio():.4f} ({self.leverage_ratio()*100:.2f}%)
  Debt-to-Equity (D/E):           {d_e:.4f}
  Equity Ratio (E/A):             {self.equity_ratio():.4f} ({self.equity_ratio()*100:.2f}%)
  Alavancagem Financeira:         {self.alavancagem_financeira():.4f}x

CUSTOS E RETORNOS:
  Custo da Dívida (Rd):           {self.custo_divida_implicito():.4f} ({self.custo_divida_implicito()*100:.2f}%)
  ROI (Retorno s/ Investimento):  {self.roi():.4f} ({self.roi()*100:.2f}%)
  ROE (Retorno s/ Patrimônio):    {self.roe():.4f} ({self.roe()*100:.2f}%)

INDICADORES DE RISCO:
  Interest Coverage:              {self.interest_coverage():.2f}x
  {'✓ Saudável' if self.interest_coverage() > 2.5 else '⚠️ Atenção' if self.interest_coverage() > 1.5 else '❌ Crítico'}

═══════════════════════════════════════════════════════════
        """
        return relatorio
