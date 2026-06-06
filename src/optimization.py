"""
Módulo de Otimização de Estrutura de Capital.

Encontra a estrutura de capital (D/E ratio) que minimiza o WACC
usando otimização numérica.
"""

from scipy.optimize import minimize, differential_evolution
import numpy as np


class CapitalStructureOptimizer:
    """Otimiza a estrutura de capital para minimizar o WACC."""

    def __init__(self, wacc_calculator, restricoes=None):
        """
        Inicializa o otimizador.

        Args:
            wacc_calculator: Objeto WACCCalculator
            restricoes: Dict com limites de D/E (min, max)
        """
        self.wacc_calc = wacc_calculator
        self.restricoes = restricoes or {'min': 0.0, 'max': 3.0}
        self.resultado_otimizacao = None

    def _funcao_objetivo(self, d_e_ratio):
        """
        Função objetivo a minimizar: calcula WACC para dado D/E ratio.

        Args:
            d_e_ratio: D/E ratio

        Returns:
            float: WACC para este D/E ratio
        """
        cs = self.wacc_calc.cs
        novo_d = d_e_ratio * cs.patrimonio
        novo_v = novo_d + cs.patrimonio

        if novo_v <= 0 or d_e_ratio < 0:
            return float('inf')

        peso_e = cs.patrimonio / novo_v
        peso_d = novo_d / novo_v

        # Recalcula custos com novo D/E
        beta_ajustado = 1.2 * (1 + (1 - cs.taxa_imposto) * d_e_ratio)
        re = 0.045 + beta_ajustado * 0.07

        rd = cs.taxa_juros_mercado + min(0.03 * d_e_ratio, 0.12)

        wacc = (peso_e * re) + (peso_d * rd * (1 - cs.taxa_imposto))
        return wacc

    def otimizar(self, metodo='SLSQP'):
        """
        Encontra o D/E ratio ótimo que minimiza o WACC.

        Args:
            metodo: Método de otimização ('SLSQP', 'Nelder-Mead', 'differential_evolution')

        Returns:
            dict: Resultado da otimização com x_otimo, wacc_minimo, etc.
        """
        d_e_inicial = self.wacc_calc.cs.debt_to_equity()

        if metodo == 'differential_evolution':
            # Usa algoritmo evolutivo para busca global
            bounds = [(self.restricoes['min'], self.restricoes['max'])]
            resultado = differential_evolution(
                self._funcao_objetivo,
                bounds,
                seed=42,
                maxiter=1000
            )
        else:
            # Usa métodos clássicos de otimização
            bounds = [(self.restricoes['min'], self.restricoes['max'])]
            resultado = minimize(
                self._funcao_objetivo,
                x0=d_e_inicial,
                bounds=bounds,
                method=metodo
            )

        self.resultado_otimizacao = {
            'metodo': metodo,
            'd_e_otimo': resultado.x[0] if hasattr(resultado.x, '__len__') else resultado.x,
            'wacc_minimo': resultado.fun,
            'sucesso': resultado.success,
            'mensagem': resultado.message if hasattr(resultado, 'message') else str(resultado.success)
        }

        return self.resultado_otimizacao

    def analise_sensibilidade(self, d_e_min=None, d_e_max=None, pontos=100):
        """
        Realiza análise de sensibilidade: WACC para vários D/E ratios.

        Args:
            d_e_min: D/E mínimo (default: usa restricoes)
            d_e_max: D/E máximo (default: usa restricoes)
            pontos: Número de pontos para análise

        Returns:
            list: Lista de (d_e, wacc) para cada ponto
        """
        d_e_min = d_e_min or self.restricoes['min']
        d_e_max = d_e_max or self.restricoes['max']

        d_e_valores = np.linspace(d_e_min, d_e_max, pontos)
        sensibilidade = []

        for d_e in d_e_valores:
            wacc = self._funcao_objetivo(d_e)
            sensibilidade.append((d_e, wacc))

        return sensibilidade

    def recomendacoes(self):
        """
        Gera recomendações baseadas na otimização.

        Returns:
            str: Texto com recomendações
        """
        if not self.resultado_otimizacao:
            return "Execute otimizar() primeiro."

        cs = self.wacc_calc.cs
        d_e_atual = cs.debt_to_equity()
        d_e_otimo = self.resultado_otimizacao['d_e_otimo']
        wacc_otimo = self.resultado_otimizacao['wacc_minimo']
        wacc_atual = self.wacc_calc.calcular_wacc()

        mudanca_percentual = ((d_e_otimo - d_e_atual) / d_e_atual * 100) if d_e_atual > 0 else 0
        economia_wacc = ((wacc_atual - wacc_otimo) / wacc_atual * 100) if wacc_atual > 0 else 0

        if abs(mudanca_percentual) < 5:
            recomendacao = "✓ MANTER ESTRUTURA: A estrutura atual está próxima do ótimo."
        elif mudanca_percentual > 0:
            recomendacao = (f"⬆️ AUMENTAR DÍVIDA: Aumentar o D/E ratio pode reduzir o WACC em {economia_wacc:.2f}%.\n"
                           f"   Aumente a alavancagem de {d_e_atual:.3f} para {d_e_otimo:.3f}.")
        else:
            recomendacao = (f"⬇️ REDUZIR DÍVIDA: Reduzir o D/E ratio pode reduzir o WACC em {economia_wacc:.2f}%.\n"
                           f"   Diminua a alavancagem de {d_e_atual:.3f} para {d_e_otimo:.3f}.")

        riscos = ""
        if d_e_otimo > 2.0:
            riscos = "\n   ⚠️ ALERTA: D/E otimizado muito alto. Implica alto risco de crédito."
        elif d_e_otimo > 1.5:
            riscos = "\n   ⚠️ AVISO: D/E otimizado moderadamente alto. Monitore indicadores de solvência."

        return recomendacao + riscos

    def relatorio_otimizacao(self):
        """
        Gera relatório completo da otimização.

        Returns:
            str: String com o relatório
        """
        if not self.resultado_otimizacao:
            return "Modelo não otimizado ainda."

        otim = self.resultado_otimizacao
        cs = self.wacc_calc.cs
        d_e_atual = cs.debt_to_equity()
        wacc_atual = self.wacc_calc.calcular_wacc()

        mudanca_de = ((otim['d_e_otimo'] - d_e_atual) / d_e_atual * 100) if d_e_atual > 0 else 0
        economia = ((wacc_atual - otim['wacc_minimo']) / wacc_atual * 100) if wacc_atual > 0 else 0

        relatorio = f"""
═══════════════════════════════════════════════════════════
OTIMIZAÇÃO DE ESTRUTURA DE CAPITAL - {cs.empresa_nome.upper()}
═══════════════════════════════════════════════════════════

SITUAÇÃO ATUAL:
  D/E Ratio Atual:                 {d_e_atual:.4f}
  WACC Atual:                      {wacc_atual*100:.2f}%

RESULTADO DA OTIMIZAÇÃO:
  Método:                          {otim['metodo']}
  D/E Ratio Ótimo:                 {otim['d_e_otimo']:.4f}
  WACC Mínimo:                     {otim['wacc_minimo']*100:.2f}%
  Sucesso:                         {'✓ Sim' if otim['sucesso'] else '✗ Não'}

COMPARATIVO:
  Mudança em D/E:                  {mudanca_de:+.2f}%
  Economia de WACC:                {economia:.2f}%
  Redução Absoluta de WACC:        {(wacc_atual - otim['wacc_minimo'])*100:+.2f}%

RECOMENDAÇÕES:
{self.recomendacoes()}

RESTRIÇÕES APLICADAS:
  D/E Mínimo:                      {self.restricoes['min']:.4f}
  D/E Máximo:                      {self.restricoes['max']:.4f}

═══════════════════════════════════════════════════════════
        """
        return relatorio
