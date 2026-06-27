"""
ARTIGO 22 - Coleta de dados via Refinitiv Eikon (Worldscope)
Estrutura de Capital e Oligopolio nas Compras Publicas de TI

Coleta:
1. Indicadores financeiros de empresas B3 (2015-2024)
   - Endividamento, Patrimonio Liquido, Ativo Total
   - Receita, EBITDA, ROA, Cobertura de Juros
2. Cruzamento com dados de contratos do PNCP

Saida:
- Raw_Data/balanço_patrimonial.csv
- Raw_Data/dre.csv
- Raw_Data/indicadores_anuais.csv
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

RICS = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "ITSA4.SA", "BBSE3.SA",
    "PSSA3.SA", "ALSO3.SA", "LJQQ3.SA", "SQIA3.SA",
]

START = "2015-01-01"
END = "2024-12-31"


def coletar_balanco():
    print(f"[1/3] Coletando dados de balanco patrimonial ({START} a {END})...")
    campos = [
        "TR.TotalAssets", "TR.TotalLiabilities", "TR.TotalEquity",
        "TR.TotalDebt", "TR.LongTermDebt", "TR.ShortTermDebt",
    ]
    df, err = ek.get_data(RICS, campos, {"SDate": START, "EDate": END, "Frq": "FY"})
    df.to_csv("Raw_Data/balanco_patrimonial.csv", index=False)
    print(f"  -> Salvo em Raw_Data/balanco_patrimonial.csv ({len(df)} linhas)")


def coletar_dre():
    print("[2/3] Coletando DRE (Demonstracao do Resultado)...")
    campos = [
        "TR.Revenue", "TR.GrossProfit", "TR.OperatingIncome",
        "TR.EBITDA", "TR.NetIncome", "TR.InterestExpense",
    ]
    df, err = ek.get_data(RICS, campos, {"SDate": START, "EDate": END, "Frq": "FY"})
    df.to_csv("Raw_Data/dre.csv", index=False)
    print(f"  -> Salvo em Raw_Data/dre.csv ({len(df)} linhas)")


def coletar_indicadores():
    print("[3/3] Calculando indicadores derivados (deve rodar apos balanco + DRE)...")
    balanco = pd.read_csv("Raw_Data/balanco_patrimonial.csv")
    dre = pd.read_csv("Raw_Data/dre.csv")
    df = balanco.merge(dre, on=["Instrument", "Date"], how="outer")
    df["endividamento_total"] = df["TR.TotalDebt"] / df["TR.TotalAssets"]
    df["cobertura_juros"] = df["TR.EBITDA"] / df["TR.InterestExpense"].replace(0, 1)
    df["ROA"] = df["TR.NetIncome"] / df["TR.TotalAssets"].replace(0, 1)
    df.to_csv("Raw_Data/indicadores_anuais.csv", index=False)
    print(f"  -> Salvo em Raw_Data/indicadores_anuais.csv ({len(df)} linhas)")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    coletar_balanco()
    coletar_dre()
    coletar_indicadores()
    print("\nConcluido. Proximos passos:")
    print("1. Calcular HHI por subsetor a partir de dados do PNCP")
    print("2. Rodar regressao em painel com efeitos fixos")
