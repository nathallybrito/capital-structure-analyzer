"""
Módulo de cálculo do WACC (Weighted Average Cost of Capital).

O WACC é o custo médio ponderado de capital, considerando debt e equity.
"""

class WACCCalculator:
    """Calcula o WACC de uma empresa."""

    def __init__(self, capital_structure, taxa_livre_risco=0.045, premio_risco_mercado=0.07):
        """
        Inicializa o calculador de WACC.

        Args:
            capital_structure: Objeto CapitalStructure com os dados da empresa
            taxa_livre_risco: Taxa livre de risco (Tesouro, default: 4.5%)
            premio_risco_mercado: Prêmio de risco do mercado (default: 7%)
        """
        self.cs = capital_structure
        self.taxa_livre_risco = taxa_livre_risco
        self.premio_risco_mercado = premio_risco_mercado

    def custo_patrimonio_capm(self, beta=1.2):
        """
        Calcula o custo do patrimônio usando o modelo CAPM.
        Re = Rf + β * (Rm - Rf)

        Args:
            beta: Beta da empresa (risco sistemático, default: 1.2)

        Returns:
            float: Custo do patrimônio (Re)
        """
        # Ajusta beta com base no D/E ratio (mais dívida = mais risco)
        d_e = self.cs.debt_to_equity()
        beta_ajustado = beta * (1 + (1 - self.cs.taxa_imposto) * d_e)

        custo_patrimonio = (self.taxa_livre_risco +
                           beta_ajustado * self.premio_risco_mercado)

        return custo_patrimonio

    def custo_divida(self):
        """
        Retorna o custo implícito da dívida já calculado.

        Returns:
            float: Custo da dívida (Rd)
        """
        return self.cs.custo_divida_implicito()

    def pesos_capital(self):
        """
        Calcula os pesos do patrimônio (E) e dívida (D) no capital total.

        Returns:
            tuple: (peso_patrimonio, peso_divida)
        """
        valor_total = self.cs.ativos_totais
        peso_patrimonio = self.cs.patrimonio / valor_total if valor_total > 0 else 0
        peso_divida = self.cs.divida_total / valor_total if valor_total > 0 else 0

        return peso_patrimonio, peso_divida

    def calcular_wacc(self, beta=1.2):
        """
        Calcula o WACC da empresa.
        WACC = (E/V) * Re + (D/V) * Rd * (1 - Tc)

        Args:
            beta: Beta da empresa para cálculo do CAPM

        Returns:
            float: WACC
        """
        re = self.custo_patrimonio_capm(beta)
        rd = self.custo_divida()
        peso_e, peso_d = self.pesos_capital()

        # WACC = (E/V)*Re + (D/V)*Rd*(1-Tc)
        wacc = (peso_e * re) + (peso_d * rd * (1 - self.cs.taxa_imposto))

        return wacc

    def analise_sensibilidade_wacc(self, beta_range=(0.8, 1.6)):
        """
        Calcula WACC para diferentes valores de beta (análise de sensibilidade).

        Args:
            beta_range: Tupla (beta_min, beta_max)

        Returns:
            list: Lista de tuplas (beta, wacc)
        """
        beta_min, beta_max = beta_range
        wacc_por_beta = []

        for beta in [round(beta_min + i * 0.1, 1) for i in range(int((beta_max - beta_min) * 10) + 1)]:
            wacc = self.calcular_wacc(beta)
            wacc_por_beta.append((beta, wacc))

        return wacc_por_beta

    def impacto_alavancagem(self):
        """
        Analisa como a alavancagem (D/E ratio) afeta o WACC.

        Returns:
            dict: Dicionário com análise do impacto
        """
        d_e_atual = self.cs.debt_to_equity()
        wacc_atual = self.calcular_wacc()

        # Simula redução de D/E em 50%
        d_e_reduzido = d_e_atual * 0.5
        wacc_reduzido = self._wacc_para_de_ratio(d_e_reduzido)

        # Simula aumento de D/E em 50%
        d_e_aumentado = d_e_atual * 1.5
        wacc_aumentado = self._wacc_para_de_ratio(d_e_aumentado)

        return {
            'wacc_atual': wacc_atual,
            'wacc_reducao_50': wacc_reduzido,
            'wacc_aumento_50': wacc_aumentado,
            'd_e_atual': d_e_atual,
            'd_e_reduzido': d_e_reduzido,
            'd_e_aumentado': d_e_aumentado,
            'impacto_percentual': ((wacc_reduzido - wacc_atual) / wacc_atual * 100,
                                  (wacc_aumentado - wacc_atual) / wacc_atual * 100)
        }

    def _wacc_para_de_ratio(self, novo_d_e):
        """
        Calcula o WACC para um determinado D/E ratio.
        Método auxiliar para análises de cenários.

        Args:
            novo_d_e: Novo D/E ratio desejado

        Returns:
            float: WACC para o novo D/E ratio
        """
        # Ajusta valores de dívida e patrimônio mantendo ativos totais constantes
        novo_d = (novo_d_e * self.cs.patrimonio)
        novo_e = self.cs.patrimonio
        novo_v = novo_d + novo_e

        peso_e = novo_e / novo_v if novo_v > 0 else 0
        peso_d = novo_d / novo_v if novo_v > 0 else 0

        # Recalcula custos com novo D/E
        beta_ajustado = 1.2 * (1 + (1 - self.cs.taxa_imposto) * novo_d_e)
        re = (self.taxa_livre_risco +
              beta_ajustado * self.premio_risco_mercado)

        # Custo de dívida aumenta com leverage
        rd = self.cs.taxa_juros_mercado + min(0.03 * novo_d_e, 0.12)

        return (peso_e * re) + (peso_d * rd * (1 - self.cs.taxa_imposto))

    def relatorio_wacc(self):
        """
        Gera relatório formatado do WACC e análises.

        Returns:
            str: String com o relatório
        """
        wacc = self.calcular_wacc()
        re = self.custo_patrimonio_capm()
        rd = self.custo_divida()
        peso_e, peso_d = self.pesos_capital()
        impacto = self.impacto_alavancagem()

        relatorio = f"""
═══════════════════════════════════════════════════════════
ANÁLISE DO WACC - {self.cs.empresa_nome.upper()}
═══════════════════════════════════════════════════════════

CUSTOS COMPONENTES:
  Custo do Patrimônio (Re/CAPM):  {re:.4f} ({re*100:.2f}%)
  Custo da Dívida (Rd):            {rd:.4f} ({rd*100:.2f}%)
  Taxa de Imposto:                 {self.cs.taxa_imposto:.2%}

PESOS NO CAPITAL:
  Peso Patrimônio (E/V):           {peso_e:.4f} ({peso_e*100:.2f}%)
  Peso Dívida (D/V):               {peso_d:.4f} ({peso_d*100:.2f}%)

WACC ATUAL:
  ► WACC:                          {wacc:.4f} ({wacc*100:.2f}%) ◄

ANÁLISE DE CENÁRIOS (D/E Ratio):
  D/E Atual:                       {impacto['d_e_atual']:.4f}
  WACC Atual:                      {impacto['wacc_atual']*100:.2f}%

  D/E Reduzido (-50%):             {impacto['d_e_reduzido']:.4f}
  WACC Reduzido:                   {impacto['wacc_reducao_50']*100:.2f}%
  Impacto:                         {impacto['impacto_percentual'][0]:+.2f}%

  D/E Aumentado (+50%):            {impacto['d_e_aumentado']:.4f}
  WACC Aumentado:                  {impacto['wacc_aumento_50']*100:.2f}%
  Impacto:                         {impacto['impacto_percentual'][1]:+.2f}%

═══════════════════════════════════════════════════════════
        """
        return relatorio
