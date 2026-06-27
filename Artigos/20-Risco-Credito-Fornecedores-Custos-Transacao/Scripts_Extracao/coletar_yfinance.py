"""
ARTIGO 20 - Coleta via yfinance
Score de Risco de Credito de Fornecedores Publicos

Indicadores financeiros de empresas B3 que potencialmente fornecem
ao setor publico, para modelagem de risco de credito corporativo.
"""
import os
import pandas as pd
import yfinance as yf

TICKERS = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "PSSA3.SA", "ITSA4.SA",
    "BBSE3.SA", "ALSO3.SA", "LJQQ3.SA", "SQIA3.SA",
]

START = "2017-01-01"
END = "2024-12-31"

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\20-Risco-Credito-Fornecedores-Custos-Transacao\Raw_Data"
os.makedirs(OUT_DIR, exist_ok=True)


def coletar_info():
    print(f"[1/2] Coletando informacoes de risco e indicadores...")
    linhas = []
    for t in TICKERS:
        try:
            tk = yf.Ticker(t)
            info = tk.info
            linha = {
                "ticker": t,
                "nome": info.get("longName", ""),
                "setor": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "market_cap": info.get("marketCap"),
                "total_debt": info.get("totalDebt"),
                "total_cash": info.get("totalCash"),
                "total_equity": info.get("totalStockholderEquity"),
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),
                "quick_ratio": info.get("quickRatio"),
                "interest_coverage": info.get("interestCoverage"),
                "profit_margin": info.get("profitMargins"),
                "operating_margin": info.get("operatingMargins"),
                "return_on_assets": info.get("returnOnAssets"),
                "return_on_equity": info.get("returnOnEquity"),
                "beta": info.get("beta"),
                "trailing_pe": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "price_to_book": info.get("priceToBook"),
            }
            linhas.append(linha)
        except Exception as e:
            print(f"  ! Erro em {t}: {e}")
    df = pd.DataFrame(linhas)
    df.to_csv(os.path.join(OUT_DIR, "credit_metrics_snapshot.csv"), index=False)
    print(f"  -> {len(df)} empresas com indicadores de risco salvos")


def coletar_precos_historicos():
    print(f"[2/2] Coletando precos historicos para volatilidade ({START} a {END})...")
    df = yf.download(TICKERS, start=START, end=END, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        close = df["Close"]
    else:
        close = df[["Close"]]
    close.to_csv(os.path.join(OUT_DIR, "precos_fechamento.csv"))
    retornos = close.pct_change().dropna(how="all")
    retornos.to_csv(os.path.join(OUT_DIR, "retornos_diarios.csv"))
    vol_anual = retornos.std() * (252 ** 0.5)
    vol_anual.to_csv(os.path.join(OUT_DIR, "volatilidade_anual.csv"), header=["vol_anual"])
    print(f"  -> {len(close)} dias de precos e volatilidade calculada")


if __name__ == "__main__":
    coletar_info()
    coletar_precos_historicos()
    print("\nConcluido. Arquivos em:", OUT_DIR)
