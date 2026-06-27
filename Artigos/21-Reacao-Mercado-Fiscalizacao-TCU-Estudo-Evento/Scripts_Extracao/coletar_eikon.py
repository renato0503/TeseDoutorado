"""
ARTIGO 21 - Coleta de dados via Refinitiv Eikon (Event Study)
Reacao do Mercado a Fiscalizacao do TCU

Coleta:
1. Retornos diarios de empresas listadas (B3) - 2015-2025
2. Composicao do indice Bovespa (BVSP) para modelo de mercado
3. Identificacao de acordaos do TCU (preencher manualmente)

Saida:
- Raw_Data/retornos_empresas.csv
- Raw_Data/retornos_ibovespa.csv
- Raw_Data/acordaos_tcu_template.csv
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
    "INTB3.SA", "BMOB3.SA", "PETR4.SA", "VALE3.SA",
    "BBSE3.SA", "B3SA3.SA", "ITSA4.SA", "BBDC4.SA",
]

IBOV = "BVSP"

START = "2015-01-01"
END = "2025-12-31"


def coletar_retornos_empresas():
    print(f"[1/3] Coletando retornos diarios de {len(RICS)} empresas ({START} a {END})...")
    df = ek.get_timeseries(
        rics=RICS,
        fields=["CLOSE", "RETURN"],
        start_date=START,
        end_date=END,
        interval="daily",
    )
    df.to_csv("Raw_Data/retornos_empresas.csv")
    print(f"  -> Salvo em Raw_Data/retornos_empresas.csv ({len(df)} linhas)")


def coletar_ibovespa():
    print("[2/3] Coletando retornos do IBOVESPA...")
    df = ek.get_timeseries(
        rics=[IBOV],
        fields=["CLOSE", "RETURN"],
        start_date=START,
        end_date=END,
        interval="daily",
    )
    df.to_csv("Raw_Data/retornos_ibovespa.csv")
    print(f"  -> Salvo em Raw_Data/retornos_ibovespa.csv ({len(df)} linhas)")


def criar_template_acordaos():
    print("[3/3] Criando template para acordaos do TCU...")
    template = pd.DataFrame(columns=[
        "data_publicacao", "numero_acordao", "empresa_citada",
        "ticker", "tipo_penalidade", "valor_multa_brl",
        "setor", "descricao", "url_acordao",
    ])
    template.to_csv("Raw_Data/acordaos_tcu_template.csv", index=False)
    print("  -> Template criado. Buscar acordaos em https://pesquisa.apps.tcu.gov.br/")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    coletar_retornos_empresas()
    coletar_ibovespa()
    criar_template_acordaos()
    print("\nConcluido. Proximos passos:")
    print("1. Preencher acordaos_tcu_template.csv com acordaos do TCU")
    print("2. Identificar empresas listadas entre as citadas")
    print("3. Calcular retornos anormais acumulados (CAR) por janela de evento")
