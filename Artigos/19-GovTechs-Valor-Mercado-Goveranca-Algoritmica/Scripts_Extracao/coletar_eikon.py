"""
ARTIGO 19 - Coleta de dados via Refinitiv Eikon
O Valor de Mercado das GovTechs e a Governanca Algoritmica

Coleta:
1. Retornos diarios de acoes (RICs B3) - 2018-01-01 a 2025-12-31
2. Indicadores fundamentalistas (WACC proxy, leverage, ROA, market cap)
3. Identificacao de eventos de certificacao (preencher manualmente apos busca)

Saida:
- Raw_Data/retornos_diarios.csv
- Raw_Data/fundamentalistas.csv
- Raw_Data/eventos_certificacao_template.csv
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

# Lista de RICs candidatos a GovTechs/fornecedoras de TI ao setor publico
# Ajustar apos screening inicial com base em receita publica > 5%
RICS_B3 = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "BBDC4.SA", "ITSA4.SA",
    "PETR4.SA", "VALE3.SA", "BBSE3.SA", "B3SA3.SA",
]

START = "2018-01-01"
END = "2025-12-31"


def coletar_retornos():
    print(f"[1/3] Coletando retornos diarios de {len(RICS_B3)} ativos ({START} a {END})...")
    df = ek.get_timeseries(
        rics=RICS_B3,
        fields=["CLOSE", "VOLUME"],
        start_date=START,
        end_date=END,
        interval="daily",
    )
    out = "Raw_Data/retornos_diarios.csv"
    df.to_csv(out)
    print(f"  -> Salvo em {out} ({len(df)} linhas)")


def coletar_fundamentalistas():
    print("[2/3] Coletando indicadores fundamentalistas...")
    campos = [
        "TR.PriceClose", "TR.MarketCap", "TR.CompanyMarketCap",
        "TR.TotalDebt", "TR.TotalEquity", "TR.EBITDA",
        "TR.ReturnonAssets", "TR.ReturnonEquity", "TR.WACC",
        "TR.EVToEBITDA", "TR.PriceToBVPerShare",
    ]
    df, err = ek.get_data(RICS_B3, campos, {"Period": "FY0"})
    out = "Raw_Data/fundamentalistas.csv"
    df.to_csv(out, index=False)
    print(f"  -> Salvo em {out} ({len(df)} empresas)")


def criar_template_eventos():
    print("[3/3] Criando template para eventos de certificacao...")
    template = pd.DataFrame(columns=[
        "data_evento", "ticker", "tipo_evento",
        "descricao", "valor_investimento_brl", "fonte",
    ])
    template.to_csv("Raw_Data/eventos_certificacao_template.csv", index=False)
    print("  -> Template salvo. Preencher manualmente apos busca em comunicados ao mercado.")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    coletar_retornos()
    coletar_fundamentalistas()
    criar_template_eventos()
    print("\nConcluido. Proximos passos:")
    print("1. Verificar retornos_diarios.csv e fundamentalistas.csv")
    print("2. Preencher eventos_certificacao_template.csv com eventos reais")
    print("3. Cruzar com dados do PNCP em C:/Users/Renato/Documents/Doutorado/Base_de_Dados_e_APIs")
