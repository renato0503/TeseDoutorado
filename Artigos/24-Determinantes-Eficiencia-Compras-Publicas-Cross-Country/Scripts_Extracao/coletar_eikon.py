"""
ARTIGO 24 - Coleta de dados via Refinitiv Datastream (cross-country)
Determinantes da Eficiencia em Compras Publicas

Coleta:
1. Indicadores macroeconomicos de paises (PIBpc, inflacao, abertura comercial)
2. Indicadores institucionais do World Bank Worldwide Governance Indicators
3. Indicadores de infraestrutura digital (e-Government Index - ITU/UN)

Saida:
- Raw_Data/macro_datastream.csv
- Raw_Data/wgi_worldbank.csv
- Raw_Data/egov_index_un.csv
- Raw_Data/governanca_algoritmica_dummy.csv
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

# Lista de paises com codigos ISO3
PAISES = [
    "ARG", "AUS", "AUT", "BEL", "BOL", "BRA", "CAN", "CHL", "CHN", "COL",
    "CRI", "CZE", "DNK", "ECU", "EGY", "ESP", "FIN", "FRA", "GBR", "GRC",
    "HUN", "IDN", "IND", "IRL", "ISL", "ISR", "ITA", "JPN", "KOR", "MEX",
    "NLD", "NOR", "NZL", "PAN", "PER", "PHL", "POL", "PRT", "RUS", "SGP",
    "SWE", "THA", "TUR", "TWN", "URY", "USA", "VEN", "VNM", "ZAF",
]

START = "2015-01-01"
END = "2024-12-31"


def coletar_macro():
    print(f"[1/4] Coletando indicadores macroeconomicos ({START} a {END})...")
    codigos_datastream = [(p, p + "GDPPC") for p in PAISES]
    # Datastream requer codigos especificos; abaixo exemplo generico
    rics = [f"{p}=XETR" for p in ["USD", "EUR"]]  # placeholder FX
    df = ek.get_data(rics, ["TR.PriceClose"], {"SDate": START, "EDate": END})
    df[0].to_csv("Raw_Data/macro_datastream.csv", index=False)
    print("  -> Salvo em Raw_Data/macro_datastream.csv (exemplo FX). Ampliar com codigos Datastream reais.")


def coletar_wgi():
    print("[2/4] Coletando Worldwide Governance Indicators (manual)...")
    instrucoes = (
        "World Bank WGI nao tem API publica robusta.\n"
        "1. Acesse: https://info.worldbank.org/governance/wgi/\n"
        "2. Baixe o dataset completo (formato Excel ou CSV)\n"
        "3. Salve como Raw_Data/wgi_raw.xlsx ou wgi_raw.csv\n"
        "4. Execute este script novamente para processar"
    )
    print(instrucoes)
    for f in ["Raw_Data/wgi_raw.xlsx", "Raw_Data/wgi_raw.csv"]:
        if os.path.exists(f):
            try:
                if f.endswith(".xlsx"):
                    df = pd.read_excel(f)
                else:
                    df = pd.read_csv(f)
                cols = ["countrycode", "year", "estimate"]
                df_pivot = df[cols].pivot_table(
                    index=["countrycode", "year"], columns=None, values="estimate"
                )
                df_pivot.to_csv("Raw_Data/wgi_worldbank.csv")
                print("  -> Processado: Raw_Data/wgi_worldbank.csv")
            except Exception as e:
                print(f"  Erro processando {f}: {e}")
            break


def coletar_egov():
    print("[3/4] Coletando UN E-Government Index (manual)...")
    instrucoes = (
        "1. Acesse: https://publicadministration.un.org/en/intergovernmental-support/egdi\n"
        "2. Baixe o dataset do EGDI 2015-2024\n"
        "3. Salve como Raw_Data/egov_un.csv\n"
        "4. Execute novamente para processar"
    )
    print(instrucoes)
    f = "Raw_Data/egov_un.csv"
    if os.path.exists(f):
        try:
            df = pd.read_csv(f)
            df.to_csv("Raw_Data/egov_index_un.csv", index=False)
            print("  -> Processado: Raw_Data/egov_index_un.csv")
        except Exception as e:
            print(f"  Erro: {e}")


def criar_template_gov_alg():
    print("[4/4] Criando template para dummy de governanca algoritmica...")
    template = pd.DataFrame({
        "countrycode": PAISES,
        "tem_compras_eletronicas": [None] * len(PAISES),
        "tem_auditoria_continua": [None] * len(PAISES),
        "tem_xai_contratacao": [None] * len(PAISES),
        "fonte": [None] * len(PAISES),
    })
    template.to_csv("Raw_Data/governanca_algoritmica_dummy.csv", index=False)
    print("  -> Template salvo. Preencher manualmente com base em pesquisa documental.")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    criar_template_gov_alg()
    coletar_macro()
    coletar_wgi()
    coletar_egov()
    print("\nConcluido. Proximos passos:")
    print("1. Preencher governanca_algoritmica_dummy.csv e arquivos manuais")
    print("2. Rodar regressao em painel com efeitos fixos de pais e ano")
