"""
ARTIGO 19 - Coleta REAL via Refinitiv Eikon Data API
"""
import os
import sys
import pandas as pd
import eikon as ek

APP_KEY = "7d2c324b20fd439fa46ebefeb82dcbf5e837b5e5"
ek.set_app_key(APP_KEY)

RICS_B3 = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "PSSA3.SA", "ALSO3.SA",
    "LJQQ3.SA", "SQIA3.SA", "BBDC4.SA", "ITSA4.SA",
]

START = "2020-01-01"
END = "2024-12-31"


def main():
    os.chdir(r"C:\Users\Renato\Documents\Doutorado\Artigos\19-GovTechs-Valor-Mercado-Goveranca-Algoritmica")
    print("[1/3] Coletando retornos diarios...")
    try:
        df = ek.get_timeseries(
            rics=RICS_B3,
            fields=["CLOSE", "VOLUME"],
            start_date=START,
            end_date=END,
            interval="daily",
        )
        df.to_csv("Raw_Data/retornos_diarios.csv")
        print(f"  -> Salvo: {len(df)} linhas")
    except Exception as e:
        print(f"  ERRO: {e}")
        return

    print("[2/3] Coletando fundamentalistas...")
    try:
        campos = [
            "TR.PriceClose", "TR.MarketCap", "TR.CompanyMarketCap",
            "TR.TotalDebt", "TR.TotalEquity", "TR.EBITDA",
            "TR.ReturnonAssets", "TR.ReturnonEquity",
        ]
        df2, err = ek.get_data(RICS_B3, campos, {"Period": "FY0"})
        df2.to_csv("Raw_Data/fundamentalistas.csv", index=False)
        print(f"  -> Salvo: {len(df2)} empresas")
    except Exception as e:
        print(f"  ERRO: {e}")

    print("[3/3] Template de eventos criado")
    template = pd.DataFrame(columns=[
        "data_evento", "ticker", "tipo_evento",
        "descricao", "valor_investimento_brl", "fonte",
    ])
    template.to_csv("Raw_Data/eventos_certificacao_template.csv", index=False)
    print("\nConcluido")


if __name__ == "__main__":
    main()
