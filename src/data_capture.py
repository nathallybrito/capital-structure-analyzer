"""
Módulo de Captura de Dados.

Permite capturar dados de empresas via linha de comando ou arquivo CSV.
"""

import pandas as pd
import os
from capital_structure import CapitalStructure


class DataCapture:
    """Gerencia captura e carregamento de dados de empresas."""

    def __init__(self, arquivo_dados='data/companies_data.csv'):
        """
        Inicializa o capturador de dados.

        Args:
            arquivo_dados: Caminho do arquivo CSV com os dados
        """
        self.arquivo_dados = arquivo_dados
        self.empresas = []
        self.carregar_dados_existentes()

    def carregar_dados_existentes(self):
        """Carrega dados do arquivo CSV se existir."""
        if os.path.exists(self.arquivo_dados):
            try:
                df = pd.read_csv(self.arquivo_dados)
                for _, row in df.iterrows():
                    empresa = CapitalStructure(
                        empresa_nome=row['empresa'],
                        ativos_totais=float(row['ativos_totais']),
                        divida_total=float(row['divida_total']),
                        patrimonio=float(row['patrimonio']),
                        ebitda=float(row['ebitda']),
                        taxa_imposto=float(row.get('taxa_imposto', 0.34)),
                        taxa_juros_mercado=float(row.get('taxa_juros_mercado', 0.06))
                    )
                    self.empresas.append(empresa)
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")

    def capturar_empresa_manual(self):
        """
        Captura dados de uma empresa via entrada do usuário.

        Returns:
            CapitalStructure: Objeto com os dados da empresa
        """
        print("\n" + "="*60)
        print("CAPTURA DE DADOS - NOVA EMPRESA")
        print("="*60)

        try:
            nome = input("\nNome da empresa: ").strip()
            if not nome:
                print("❌ Nome não pode estar vazio.")
                return None

            ativos = float(input("Ativo total (R$): "))
            divida = float(input("Dívida total (R$): "))
            patrimonio = float(input("Patrimônio líquido (R$): "))
            ebitda = float(input("EBITDA (R$): "))

            taxa_imposto = float(input("Taxa de imposto (padrão 0.34): ") or "0.34")
            taxa_juros = float(input("Taxa de juros de mercado (padrão 0.06): ") or "0.06")

            if ativos <= 0 or patrimonio <= 0 or ebitda <= 0:
                print("❌ Valores devem ser positivos.")
                return None

            empresa = CapitalStructure(
                empresa_nome=nome,
                ativos_totais=ativos,
                divida_total=divida,
                patrimonio=patrimonio,
                ebitda=ebitda,
                taxa_imposto=taxa_imposto,
                taxa_juros_mercado=taxa_juros
            )

            self.empresas.append(empresa)
            self.salvar_dados()

            print(f"✓ Empresa {nome} adicionada com sucesso!")
            return empresa

        except ValueError as e:
            print(f"❌ Erro ao processar entrada: {e}")
            return None

    def salvar_dados(self):
        """Salva os dados das empresas no arquivo CSV."""
        os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)

        dados = []
        for empresa in self.empresas:
            dados.append({
                'empresa': empresa.empresa_nome,
                'ativos_totais': empresa.ativos_totais,
                'divida_total': empresa.divida_total,
                'patrimonio': empresa.patrimonio,
                'ebitda': empresa.ebitda,
                'taxa_imposto': empresa.taxa_imposto,
                'taxa_juros_mercado': empresa.taxa_juros_mercado
            })

        df = pd.DataFrame(dados)
        df.to_csv(self.arquivo_dados, index=False)
        print(f"✓ Dados salvos em {self.arquivo_dados}")

    def listar_empresas(self):
        """Lista todas as empresas registradas."""
        if not self.empresas:
            print("\n❌ Nenhuma empresa registrada.")
            return

        print("\n" + "="*100)
        print("EMPRESAS REGISTRADAS")
        print("="*100)
        print(f"{'Nome':<20} {'Ativos':<15} {'Dívida':<15} {'Patrimônio':<15} {'D/E Ratio':<10}")
        print("-"*100)

        for empresa in self.empresas:
            print(f"{empresa.empresa_nome:<20} "
                  f"R$ {empresa.ativos_totais:>13,.0f} "
                  f"R$ {empresa.divida_total:>13,.0f} "
                  f"R$ {empresa.patrimonio:>13,.0f} "
                  f"{empresa.debt_to_equity():>9.4f}")

        print("="*100)

    def obter_empresa(self, indice_ou_nome):
        """
        Obtém uma empresa por índice ou nome.

        Args:
            indice_ou_nome: Índice (int) ou nome (str) da empresa

        Returns:
            CapitalStructure: Objeto da empresa ou None
        """
        if isinstance(indice_ou_nome, int):
            if 0 <= indice_ou_nome < len(self.empresas):
                return self.empresas[indice_ou_nome]
        else:
            for empresa in self.empresas:
                if empresa.empresa_nome.lower() == indice_ou_nome.lower():
                    return empresa

        return None

    def criar_dados_exemplo(self):
        """Cria dados de exemplo se o arquivo não existir."""
        if os.path.exists(self.arquivo_dados):
            return

        print("Criando dados de exemplo...")

        dados_exemplo = [
            {
                'empresa': 'TechCorp',
                'ativos_totais': 5000000,
                'divida_total': 1500000,
                'patrimonio': 3500000,
                'ebitda': 1000000,
                'taxa_imposto': 0.34,
                'taxa_juros_mercado': 0.06
            },
            {
                'empresa': 'RetailCo',
                'ativos_totais': 10000000,
                'divida_total': 4000000,
                'patrimonio': 6000000,
                'ebitda': 1500000,
                'taxa_imposto': 0.34,
                'taxa_juros_mercado': 0.06
            },
            {
                'empresa': 'ManufExcel',
                'ativos_totais': 8000000,
                'divida_total': 2500000,
                'patrimonio': 5500000,
                'ebitda': 1200000,
                'taxa_imposto': 0.34,
                'taxa_juros_mercado': 0.06
            },
            {
                'empresa': 'FinanceGroup',
                'ativos_totais': 12000000,
                'divida_total': 6000000,
                'patrimonio': 6000000,
                'ebitda': 2000000,
                'taxa_imposto': 0.34,
                'taxa_juros_mercado': 0.06
            },
            {
                'empresa': 'ServicePro',
                'ativos_totais': 3000000,
                'divida_total': 600000,
                'patrimonio': 2400000,
                'ebitda': 800000,
                'taxa_imposto': 0.34,
                'taxa_juros_mercado': 0.06
            }
        ]

        df = pd.DataFrame(dados_exemplo)
        os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)
        df.to_csv(self.arquivo_dados, index=False)

        self.empresas = []
        self.carregar_dados_existentes()

        print(f"✓ {len(self.empresas)} empresas de exemplo criadas em {self.arquivo_dados}")
