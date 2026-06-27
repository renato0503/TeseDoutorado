"""
ARTIGO 22 - Coleta via yfinance
Estrutura de Capital e Oligopolio nas Compras Publicas de TI

Balanco patrimonial, DRE e indicadores de endividamento de empresas B3
que potencialmente fornecem ao setor publico.
"""
import os
import pandas as pd
import yfinance as yf

TICKERS = [
    "POSI3.SA", "TOTS3.SA", "LWSA3.SA", "MLAS3.SA",
    "INTB3.SA", "BMOB3.SA", "PSSA3.SA", "ITSA4.SA",
    "BBSE3.SA", "ALSO3.SA",
]

START = "2015-01-01"
END = "2024-12-31"

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\22-Estrutura-Capital-Oligopolio-Compras-TI\Raw_Data"
os.makedirs(OUT_DIR, exist_ok=True)


def coletar_balancos():
    print(f"[1/2] Coletando demonstracoes financeiras anuais via yfinance...")
    registros = []
    for t in TICKERS:
        print(f"  - {t}")
        try:
            tk = yf.Ticker(t)
            bs = tk.balance_sheet
            inc = tk.income_stmt
            if bs is None or inc is None or bs.empty or inc.empty:
                continue
            for col in bs.columns:
                ano = col.year if hasattr(col, "year") else pd.Timestamp(col).year
                try:
                    rec = {
                        "ticker": t,
                        "ano": ano,
                        "ativo_total": bs.loc["Total Assets", col] if "Total Assets" in bs.index else None,
                        "passivo_total": bs.loc["Total Liabilities Net Minority Interest", col] if "Total Liabilities Net Minority Interest" in bs.index else (bs.loc["Total Liab", col] if "Total Liab" in bs.index else None),
                        "patrimonio_liquido": bs.loc["Stockholders Equity", col] if "Stockholders Equity" in bs.index else (bs.loc["Total Equity Gross Minority Interest", col] if "Total Equity Gross Minority Interest" in bs.index else None),
                        "divida_total": bs.loc["Total Debt", col] if "Total Debt" in bs.index else None,
                        "caixa": bs.loc["Cash And Cash Equivalents", col] if "Cash And Cash Equivalents" in bs.index else (bs.loc["Cash", col] if "Cash" in bs.index else None),
                        "divida_longo_prazo": bs.loc["Long Term Debt", col] if "Long Term Debt" in bs.index else None,
                        "receita": inc.loc["Total Revenue", col] if "Total Revenue" in inc.index else (inc.loc["Operating Revenue", col] if "Operating Revenue" in inc.index else None),
                        "ebitda": inc.loc["EBITDA", col] if "EBITDA" in inc.index else None,
                        "lucro_liquido": inc.loc["Net Income", col] if "Net Income" in inc.index else None,
                        "despesa_juros": inc.loc["Interest Expense", col] if "Interest Expense" in inc.index else None,
                    }
                    registros.append(rec)
                except KeyError:
                    continue
        except Exception as e:
            print(f"    ! Erro em {t}: {e}")
    df = pd.DataFrame(registros)
    df.to_csv(os.path.join(OUT_DIR, "demonstracoes_financeiras.csv"), index=False)
    print(f"  -> {len(df)} registros salvos")


def calcular_indicadores():
    print("[2/2] Calculando indicadores derivados...")
    df = pd.read_csv(os.path.join(OUT_DIR, "demonstracoes_financeiras.csv"))
    df["endividamento_total"] = df["divida_total"] / df["ativo_total"]
    df["divida_patrimonio"] = df["divida_total"] / df["patrimonio_liquido"]
    df["cobertura_juros"] = df["ebitda"] / df["despesa_juros"].replace(0, float("nan"))
    df["ROA"] = df["lucro_liquido"] / df["ativo_total"]
    df["ROE"] = df["lucro_liquido"] / df["patrimonio_liquido"]
    df["margem_ebitda"] = df["ebitda"] / df["receita"]
    df.to_csv(os.path.join(OUT_DIR, "indicadores_anuais.csv"), index=False)
    print(f"  -> {len(df)} registros com indicadores salvos")


if __name__ == "__main__":
    coletar_balancos()
    calcular_indicadores()
    print("\nConcluido. Arquivos em:", OUT_DIR)
