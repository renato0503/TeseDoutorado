"""
ARTIGO 22 - Análise empírica
Estrutura de Capital e Oligopolio nas Compras Publicas de TI
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\22-Estrutura-Capital-Oligopolio-Compras-TI"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(IMG, exist_ok=True)


def carregar_dados():
    df = pd.read_csv(os.path.join(RAW, "indicadores_anuais.csv"))
    return df


def estatisticas_descritivas(df):
    print("=" * 70)
    print("ESTATISTICAS DESCRITIVAS")
    print("=" * 70)
    cols = ["ativo_total", "divida_total", "patrimonio_liquido", "receita",
            "ebitda", "endividamento_total", "cobertura_juros", "ROA", "ROE", "margem_ebitda"]
    cols_existentes = [c for c in cols if c in df.columns]
    desc = df[cols_existentes].describe().T.round(4)
    print(desc)
    desc.to_csv(os.path.join(RAW, "estatisticas_descritivas.csv"))
    return desc


def grafico_endividamento_por_empresa(df):
    df_med = df.groupby("ticker")["endividamento_total"].mean().dropna().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    cores = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(df_med)))
    ax.barh(df_med.index, df_med.values * 100, color=cores)
    ax.set_xlabel("Endividamento medio (% do ativo total)", fontsize=11)
    ax.set_title("Endividamento Medio por Empresa", fontsize=12)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "endividamento_empresas.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: endividamento_empresas.png")


def grafico_evolucao_temporal(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in df["ticker"].unique():
        sub = df[df["ticker"] == ticker].sort_values("ano")
        ax.plot(sub["ano"], sub["endividamento_total"] * 100, marker="o", label=ticker, linewidth=1.5)
    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("Endividamento Total / Ativo Total (%)", fontsize=11)
    ax.set_title("Evolucao do Endividamento por Empresa", fontsize=12)
    ax.legend(loc="best", fontsize=9, ncol=3)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "evolucao_endividamento.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: evolucao_endividamento.png")


def grafico_evolucao_roa(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in df["ticker"].unique():
        sub = df[df["ticker"] == ticker].sort_values("ano")
        ax.plot(sub["ano"], sub["ROA"] * 100, marker="o", label=ticker, linewidth=1.5)
    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("ROA (%)", fontsize=11)
    ax.set_title("Evolucao da Rentabilidade sobre Ativos (ROA)", fontsize=12)
    ax.legend(loc="best", fontsize=9, ncol=3)
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color="black", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "evolucao_roa.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: evolucao_roa.png")


def correlacoes(df):
    print("\n" + "=" * 70)
    print("MATRIZ DE CORRELACAO")
    print("=" * 70)
    cols = ["endividamento_total", "cobertura_juros", "ROA", "ROE", "margem_ebitda"]
    df_corr = df[cols].dropna(how="all")
    corr = df_corr.corr(min_periods=3)
    print(corr.round(3))
    corr.to_csv(os.path.join(RAW, "correlacao_indicadores.csv"))

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(cols, fontsize=9)
    for i in range(len(cols)):
        for j in range(len(cols)):
            val = corr.iloc[i, j]
            if not pd.isna(val):
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=10, color="black")
    plt.colorbar(im, ax=ax)
    ax.set_title("Correlacao entre Indicadores de Estrutura de Capital", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "correlacao_indicadores.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: correlacao_indicadores.png")


def regressao(df):
    print("\n" + "=" * 70)
    print("REGRESSAO: Endividamento ~ Tamanho + ROA")
    print("=" * 70)
    dfr = df.dropna(subset=["endividamento_total", "ativo_total", "ROA"]).copy()
    dfr["log_ativo"] = np.log(dfr["ativo_total"].astype(float))
    dfr["endividamento_pct"] = dfr["endividamento_total"] * 100
    print(f"Observacoes validas: {len(dfr)}")
    if len(dfr) < 3:
        return None, None, None
    X = dfr[["log_ativo", "ROA"]].values
    X_ = np.column_stack([np.ones(len(X)), X])
    y = dfr["endividamento_pct"].values
    beta, _, _, _ = np.linalg.lstsq(X_, y, rcond=None)
    y_hat = X_ @ beta
    ss_res = ((y - y_hat) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot
    print(f"\nCoeficientes:")
    print(f"  Intercepto: {beta[0]:.3f}")
    print(f"  log(Ativo): {beta[1]:.3f}")
    print(f"  ROA: {beta[2]:.3f}")
    print(f"R²: {r2:.3f}")
    return beta, r2, dfr


def main():
    df = carregar_dados()
    print(f"Total de observacoes: {len(df)}")
    print(f"Empresas: {df['ticker'].nunique()}")
    print(f"Anos: {df['ano'].min()}-{df['ano'].max()}")

    estatisticas_descritivas(df)
    grafico_endividamento_por_empresa(df)
    grafico_evolucao_temporal(df)
    grafico_evolucao_roa(df)
    correlacoes(df)
    regressao(df)
    print("\nConcluido")


if __name__ == "__main__":
    main()
