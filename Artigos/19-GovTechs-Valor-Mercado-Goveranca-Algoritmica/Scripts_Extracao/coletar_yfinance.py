"""
ARTIGO 19 - Coleta via yfinance
O Valor de Mercado das GovTechs e a Governanca Algoritmica

Empresas listadas na B3 potencialmente fornecedoras do setor publico de TI
(selecionadas por triagem inicial com base em CNAE e receita publica estimada).
"""
import os
import pandas as pd
import yfinance as yf

TICKERS = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "PSSA3.SA", "ALSO3.SA",
    "LJQQ3.SA", "SQIA3.SA",
    # Holdings que detem empresas de TI com contratos publicos
    "BBDC4.SA", "ITSA4.SA", "BBSE3.SA",
]

START = "2018-01-01"
END = "2025-06-30"

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\19-GovTechs-Valor-Mercado-Goveranca-Algoritmica\Raw_Data"
os.makedirs(OUT_DIR, exist_ok=True)


def coletar_precos():
    print(f"[1/2] Baixando precos de {len(TICKERS)} ativos via yfinance ({START} a {END})...")
    df = yf.download(TICKERS, start=START, end=END, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df_close = df["Close"]
        df_volume = df["Volume"]
    else:
        df_close = df[["Close"]]
        df_volume = df[["Volume"]]
    df_close.to_csv(os.path.join(OUT_DIR, "precos_fechamento.csv"))
    df_volume.to_csv(os.path.join(OUT_DIR, "volume_negociacao.csv"))
    print(f"  -> {len(df_close)} dias de precos salvos")
    return df_close


def coletar_fundamentalistas():
    print("[2/2] Coletando indicadores fundamentalistas via yfinance...")
    linhas = []
    for t in TICKERS:
        try:
            tk = yf.Ticker(t)
            info = tk.info
            linha = {
                "ticker": t,
                "nome": info.get("longName", ""),
                "setor": info.get("sector", ""),
                "industria": info.get("industry", ""),
                "market_cap": info.get("marketCap"),
                "enterprise_value": info.get("enterpriseValue"),
                "total_debt": info.get("totalDebt"),
                "total_cash": info.get("totalCash"),
                "total_equity": info.get("totalStockholderEquity"),
                "ebitda": info.get("ebitda"),
                "revenue_ttm": info.get("totalRevenue"),
                "profit_margin": info.get("profitMargins"),
                "operating_margin": info.get("operatingMargins"),
                "return_on_assets": info.get("returnOnAssets"),
                "return_on_equity": info.get("returnOnEquity"),
                "beta": info.get("beta"),
                "trailing_pe": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "price_to_book": info.get("priceToBook"),
                "wacc_estimado": None,
            }
            linhas.append(linha)
        except Exception as e:
            print(f"  ! Falha em {t}: {e}")
    df = pd.DataFrame(linhas)
    df.to_csv(os.path.join(OUT_DIR, "fundamentalistas.csv"), index=False)
    print(f"  -> {len(df)} empresas com indicadores salvos")


if __name__ == "__main__":
    coletar_precos()
    coletar_fundamentalistas()
    print("\nConcluido. Arquivos em:", OUT_DIR)
