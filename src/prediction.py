"""
Módulo de Previsão de WACC.

Utiliza regressão polinomial para prever como o WACC varia
com a estrutura de capital (D/E ratio).
"""

import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error


class PredictorWACC:
    """Prediz WACC baseado em estrutura de capital usando ML."""

    def __init__(self, grau_polinomio=2):
        """
        Inicializa o preditor.

        Args:
            grau_polinomio: Grau do polinômio para regressão (default: 2)
        """
        self.grau = grau_polinomio
        self.modelo = None
        self.poly_features = None
        self.X_treino = None
        self.y_treino = None
        self.r2 = None
        self.rmse = None

    def gerar_dados_treino(self, empresas_lista, wacc_calculator_class):
        """
        Gera dados de treino a partir de uma lista de empresas.
        Simula diferentes D/E ratios para cada empresa.

        Args:
            empresas_lista: Lista de objetos CapitalStructure
            wacc_calculator_class: Classe WACCCalculator para cálculos

        Returns:
            tuple: (X_dados, y_dados) para treino
        """
        x_dados = []
        y_dados = []

        for empresa in empresas_lista:
            # Gera pontos de dados simulando diferentes estruturas de capital
            d_e_base = empresa.debt_to_equity()

            # Varia o D/E ratio de 0 até 3x o valor atual
            for multiplicador in np.linspace(0.1, 3.0, 30):
                novo_d_e = d_e_base * multiplicador
                novo_d = novo_d_e * empresa.patrimonio
                novo_v = novo_d + empresa.patrimonio

                if novo_v > 0:
                    # Calcula WACC para este D/E ratio
                    peso_e = empresa.patrimonio / novo_v
                    peso_d = novo_d / novo_v

                    rd = empresa.taxa_juros_mercado + min(0.03 * novo_d_e, 0.12)
                    beta_ajustado = 1.2 * (1 + (1 - empresa.taxa_imposto) * novo_d_e)
                    re = 0.045 + beta_ajustado * 0.07

                    wacc_simulado = (peso_e * re) + (peso_d * rd * (1 - empresa.taxa_imposto))

                    x_dados.append([novo_d_e])
                    y_dados.append(wacc_simulado)

        self.X_treino = np.array(x_dados)
        self.y_treino = np.array(y_dados)

        return self.X_treino, self.y_treino

    def treinar(self, X_treino, y_treino):
        """
        Treina o modelo de regressão polinomial.

        Args:
            X_treino: Features (D/E ratio) - array (n, 1)
            y_treino: Target (WACC) - array (n,)
        """
        # Transforma em polinômio
        self.poly_features = PolynomialFeatures(degree=self.grau)
        X_poly = self.poly_features.fit_transform(X_treino)

        # Treina modelo linear no espaço polinomial
        self.modelo = LinearRegression()
        self.modelo.fit(X_poly, y_treino)

        # Calcula métricas
        y_pred = self.modelo.predict(X_poly)
        self.r2 = r2_score(y_treino, y_pred)
        self.rmse = np.sqrt(mean_squared_error(y_treino, y_pred))

    def prever(self, d_e_ratio):
        """
        Prevê o WACC para um determinado D/E ratio.

        Args:
            d_e_ratio: D/E ratio (float ou array)

        Returns:
            float ou array: WACC previsto
        """
        if self.modelo is None:
            raise ValueError("Modelo não treinado. Execute treinar() primeiro.")

        if isinstance(d_e_ratio, (int, float)):
            x = np.array([[d_e_ratio]])
        else:
            x = np.array(d_e_ratio).reshape(-1, 1)

        x_poly = self.poly_features.transform(x)
        predicoes = self.modelo.predict(x_poly)

        return predicoes[0] if len(predicoes) == 1 else predicoes

    def intervalo_confianca(self, d_e_ratio, confianca=0.95):
        """
        Calcula intervalo de confiança para a previsão.

        Args:
            d_e_ratio: D/E ratio
            confianca: Nível de confiança (default: 95%)

        Returns:
            tuple: (wacc_pred, limite_inferior, limite_superior)
        """
        wacc_pred = self.prever(d_e_ratio)

        # Usa RMSE para estimar intervalo de confiança
        # Intervalo ≈ previsão ± (z * RMSE)
        z = 1.96 if confianca == 0.95 else 2.576  # Para 99%

        margem_erro = z * self.rmse
        limite_inferior = max(0, wacc_pred - margem_erro)
        limite_superior = wacc_pred + margem_erro

        return wacc_pred, limite_inferior, limite_superior

    def encontrar_minimo_wacc(self, d_e_min=0.0, d_e_max=3.0):
        """
        Encontra o D/E ratio que minimiza o WACC previsto.

        Args:
            d_e_min: D/E mínimo a considerar
            d_e_max: D/E máximo a considerar

        Returns:
            tuple: (d_e_otimo, wacc_minimo)
        """
        if self.modelo is None:
            raise ValueError("Modelo não treinado.")

        # Testa múltiplos pontos para encontrar o mínimo
        d_e_valores = np.linspace(d_e_min, d_e_max, 100)
        wacc_valores = self.prever(d_e_valores)

        idx_minimo = np.argmin(wacc_valores)
        d_e_otimo = d_e_valores[idx_minimo]
        wacc_minimo = wacc_valores[idx_minimo]

        return d_e_otimo, wacc_minimo

    def tabela_previsoes(self, d_e_inicio=0.0, d_e_fim=3.0, passos=11):
        """
        Gera tabela de previsões de WACC para vários D/E ratios.

        Args:
            d_e_inicio: D/E inicial
            d_e_fim: D/E final
            passos: Número de pontos

        Returns:
            list: Lista de dicts com previsões
        """
        previsoes = []
        d_e_valores = np.linspace(d_e_inicio, d_e_fim, passos)

        for d_e in d_e_valores:
            wacc_pred, ic_lower, ic_upper = self.intervalo_confianca(d_e)
            previsoes.append({
                'd_e_ratio': d_e,
                'wacc': wacc_pred,
                'ic_lower': ic_lower,
                'ic_upper': ic_upper,
                'margem_erro': ic_upper - wacc_pred
            })

        return previsoes

    def relatorio_previsao(self):
        """
        Gera relatório das previsões e análises.

        Returns:
            str: String com o relatório
        """
        if self.modelo is None:
            return "Modelo não treinado ainda."

        d_e_otimo, wacc_otimo = self.encontrar_minimo_wacc()
        previsoes = self.tabela_previsoes()

        relatorio = f"""
═══════════════════════════════════════════════════════════
ANÁLISE DE PREVISÃO - MODELO DE REGRESSÃO POLINOMIAL
═══════════════════════════════════════════════════════════

DESEMPENHO DO MODELO:
  Grau do Polinômio:               {self.grau}
  R² Score:                        {self.r2:.4f}
  RMSE:                            {self.rmse:.6f}
  {'✓ Bom ajuste' if self.r2 > 0.80 else '⚠️ Ajuste moderado' if self.r2 > 0.60 else '❌ Ajuste fraco'}

ESTRUTURA DE CAPITAL ÓTIMA:
  D/E Ratio Ótimo:                 {d_e_otimo:.4f}
  WACC Mínimo Previsto:            {wacc_otimo*100:.2f}%

PREVISÕES DE WACC:
  D/E Ratio  │ WACC Previsto │ IC Inferior │ IC Superior │ Margem
  ─────────────────────────────────────────────────────────────
"""

        for pred in previsoes:
            relatorio += f"  {pred['d_e_ratio']:7.2f}   │ {pred['wacc']*100:11.2f}% │ {pred['ic_lower']*100:10.2f}% │ {pred['ic_upper']*100:10.2f}% │ ±{pred['margem_erro']*100:5.2f}%\n"

        relatorio += f"""
═══════════════════════════════════════════════════════════

INTERPRETAÇÃO:
O modelo de regressão polinomial de grau {self.grau} foi treinado com dados
simulados de múltiplas empresas. As previsões indicam como o WACC varia
com a estrutura de capital (D/E ratio).

O intervalo de confiança (95%) mostra a incerteza na previsão.
D/E ratios menores indicam estrutura mais conservadora (menos risco).
D/E ratios maiores indicam estrutura agressiva (mais risco).

═══════════════════════════════════════════════════════════
        """
        return relatorio
