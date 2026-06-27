"""
ARTIGO 21 - Coleta via yfinance
Reacao do Mercado a Fiscalizacao do TCU

Retornos diarios de empresas listadas na B3 e IBOVESPA
para estudo de eventos em torno de acordaos do TCU.
"""
import os
import pandas as pd
import yfinance as yf

TICKERS = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "PSSA3.SA",
    "PETR4.SA", "VALE3.SA", "ITSA4.SA", "BBDC4.SA",
    "BBSE3.SA", "B3SA3.SA",
]

# ^BVSP e o ticker Yahoo para o IBOVESPA
IBOV = "^BVSP"

START = "2015-01-01"
END = "2025-06-30"

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\21-Reacao-Mercado-Fiscalizacao-TCU-Estudo-Evento\Raw_Data"
os.makedirs(OUT_DIR, exist_ok=True)


def coletar_retornos():
    print(f"[1/2] Baixando retornos de {len(TICKERS)} empresas + IBOVESPA ({START} a {END})...")
    all_tickers = TICKERS + [IBOV]
    df = yf.download(all_tickers, start=START, end=END, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        close = df["Close"]
        vol = df["Volume"]
    else:
        close = df[["Close"]]
        vol = df[["Volume"]]
    close.to_csv(os.path.join(OUT_DIR, "precos_fechamento.csv"))
    vol.to_csv(os.path.join(OUT_DIR, "volume.csv"))

    # Calcular retornos diarios
    ret = close.pct_change().dropna(how="all")
    ret.to_csv(os.path.join(OUT_DIR, "retornos_diarios.csv"))
    print(f"  -> {len(close)} dias de precos e {len(ret)} dias de retornos salvos")


def criar_template_acordaos():
    print("[2/2] Criando template para acordaos do TCU...")
    cols = [
        "data_publicacao", "numero_acordao", "empresa_citada",
        "ticker", "tipo_penalidade", "valor_multa_brl",
        "setor", "descricao", "url_acordao",
    ]
    template = pd.DataFrame(columns=cols)
    template.to_csv(os.path.join(OUT_DIR, "acordaos_tcu_template.csv"), index=False)
    print(f"  -> Template salvo. Preencher manualmente com acordaos do TCU.")
    print(f"  -> Fonte: https://pesquisa.apps.tcu.gov.br/")


if __name__ == "__main__":
    coletar_retornos()
    criar_template_acordaos()
    print("\nConcluido. Arquivos em:", OUT_DIR)
