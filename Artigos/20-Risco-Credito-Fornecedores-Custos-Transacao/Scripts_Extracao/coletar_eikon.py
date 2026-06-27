"""
ARTIGO 20 - Coleta de dados via Refinitiv Eikon (Credit Risk)
Score de Risco de Credito de Fornecedores Publicos

Coleta:
1. Ratings de credito corporativo em escala longo prazo
2. Probabilidade de inadimplencia (PD) 1 ano
3. Indicadores financeiros (leverage, cobertura de juros, ROA)
4. Cruzamento com CNPJs do PNCP

Saida:
- Raw_Data/credit_ratings.csv
- Raw_Data/credit_pd.csv
- Raw_Data/indicadores_financeiros.csv
"""
import os
import sys
import pandas as pd
import eikon as ek

APP_KEY = os.environ.get("EIKON_APP_KEY")
if not APP_KEY:
    print("ERRO: defina EIKON_APP_KEY no ambiente.")
    sys.exit(1)
ek.set_app_key(APP_KEY)

# RICs candidatos - empresas com contratos publicos relevantes
# Necessario cruzar com lista de CNPJs do PNCP para verificar fornecedores efetivos
RICS = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "ITSA4.SA", "BBSE3.SA",
    "PSSA3.SA", "ALSO3.SA", "LJQQ3.SA", "SQIA3.SA",
]

START = "2017-01-01"
END = "2024-12-31"


def coletar_ratings():
    print(f"[1/3] Coletando ratings de longo prazo ({START} a {END})...")
    df = ek.get_timeseries(
        rics=RICS,
        fields=["S&P LT Issuer Rating (Foreign)", "Moodys LT Issuer Rating"],
        start_date=START,
        end_date=END,
    )
    df.to_csv("Raw_Data/credit_ratings.csv")
    print(f"  -> Salvo em Raw_Data/credit_ratings.csv")


def coletar_pd():
    print("[2/3] Coletando probabilidade de inadimplencia (PD 1 ano)...")
    df = ek.get_data(
        RICS,
        ["TR.PDMean1Y", "TR.PDMean5Y", "TR.CreditRatingAgency"],
        {"SDate": START, "EDate": END, "Frq": "FY"},
    )
    df.to_csv("Raw_Data/credit_pd.csv", index=False)
    print("  -> Salvo em Raw_Data/credit_pd.csv")


def coletar_indicadores():
    print("[3/3] Coletando indicadores financeiros...")
    campos = [
        "TR.TotalDebt", "TR.TotalEquity", "TR.InterestCoverage",
        "TR.ReturnonAssets", "TR.OperatingMargin", "TR.CurrentRatio",
    ]
    df, err = ek.get_data(RICS, campos, {"SDate": START, "EDate": END, "Frq": "FY"})
    df.to_csv("Raw_Data/indicadores_financeiros.csv", index=False)
    print("  -> Salvo em Raw_Data/indicadores_financeiros.csv")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    coletar_ratings()
    coletar_pd()
    coletar_indicadores()
    print("\nConcluido. Proximos passos:")
    print("1. Carregar lista de CNPJs do PNCP (Base_de_Dados_e_APIs/Raw_Data/Artigos_Quanti/...)")
    print("2. Cruzar CNPJ <-> RIC para identificar fornecedores publicos efetivos")
    print("3. Extrair dados de aditivos/rescisoes dos contratos no PNCP")
