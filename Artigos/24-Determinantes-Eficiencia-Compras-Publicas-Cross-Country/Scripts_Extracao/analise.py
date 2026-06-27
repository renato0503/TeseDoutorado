"""
ARTIGO 24 - Análise empírica
Determinantes da Eficiencia em Compras Publicas cross-country
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\24-Determinantes-Eficiencia-Compras-Publicas-Cross-Country"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(IMG, exist_ok=True)


def carregar_dados():
    df = pd.read_csv(os.path.join(RAW, "dataset_consolidado_wb.csv"))
    df["ano"] = df["ano"].astype(int)
    return df


def estatisticas_descritivas(df):
    print("=" * 70)
    print("ESTATISTICAS DESCRITIVAS CROSS-COUNTRY")
    print("=" * 70)
    cols = ["pib_per_capita_usd", "crescimento_pib_pct", "abertura_comercial_pct_pib",
            "usuarios_internet_pct", "celulares_por_100",
            "gasto_publico_educacao_pct_pib", "acesso_eletricidade_pct"]
    cols_existentes = [c for c in cols if c in df.columns]
    desc = df[cols_existentes].describe().T.round(3)
    print(desc)
    desc.to_csv(os.path.join(RAW, "estatisticas_descritivas_cross.csv"))
    return desc


def grafico_pib_per_capita(df):
    """Top 20 PIB per capita em 2023."""
    df_2023 = df[df["ano"] == 2023].dropna(subset=["pib_per_capita_usd"])
    top = df_2023.nlargest(20, "pib_per_capita_usd").sort_values("pib_per_capita_usd")
    fig, ax = plt.subplots(figsize=(10, 7))
    cores = ["#27ae60" if p == "BRA" else "#3498db" for p in top["pais"]]
    ax.barh(top["pais"], top["pib_per_capita_usd"] / 1000, color=cores)
    ax.set_xlabel("PIB per capita (USD milhares)", fontsize=11)
    ax.set_title("Top 20 Paises - PIB per capita em 2023", fontsize=12)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "top_pib_per_capita.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: top_pib_per_capita.png")


def grafico_internet_celular(df):
    """Evolucao de usuarios de internet nos top 10 paises."""
    top10 = ["USA", "CHN", "GBR", "DEU", "FRA", "BRA", "IND", "JPN", "KOR", "CAN"]
    df_top = df[df["pais"].isin(top10)].dropna(subset=["usuarios_internet_pct"])
    if df_top.empty:
        return
    fig, ax = plt.subplots(figsize=(12, 6))
    for p in top10:
        sub = df_top[df_top["pais"] == p].sort_values("ano")
        if not sub.empty:
            ax.plot(sub["ano"], sub["usuarios_internet_pct"], marker="o", label=p, linewidth=1.5)
    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("Usuarios de Internet (% da populacao)", fontsize=11)
    ax.set_title("Penetracao de Internet - Top 10 Economias", fontsize=12)
    ax.legend(loc="lower right", fontsize=9, ncol=2)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "evolucao_internet.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: evolucao_internet.png")


def grafico_scatter_pib_internet(df):
    df_clean = df.dropna(subset=["pib_per_capita_usd", "usuarios_internet_pct"])
    if df_clean.empty:
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df_clean["pib_per_capita_usd"] / 1000, df_clean["usuarios_internet_pct"],
               alpha=0.6, s=30, color="#3498db")
    # Destacar Brasil
    br = df_clean[df_clean["pais"] == "BRA"]
    if not br.empty:
        ax.scatter(br["pib_per_capita_usd"] / 1000, br["usuarios_internet_pct"],
                   s=200, color="#e74c3c", label="Brasil", edgecolors="black", zorder=5)
        ax.legend()
    ax.set_xlabel("PIB per capita (USD milhares)", fontsize=11)
    ax.set_ylabel("Usuarios de Internet (%)", fontsize=11)
    ax.set_title("Relacao entre Riqueza e Infraestrutura Digital", fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "scatter_pib_internet.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: scatter_pib_internet.png")


def grafico_evolucao_pib_brasil(df):
    """Foco no Brasil."""
    br = df[df["pais"] == "BRA"].sort_values("ano")
    if br.empty:
        return
    fig, ax1 = plt.subplots(figsize=(11, 6))
    ax1.bar(br["ano"], br["pib_per_capita_usd"] / 1000, color="#3498db", alpha=0.6, label="PIB per capita")
    ax1.set_xlabel("Ano", fontsize=11)
    ax1.set_ylabel("PIB per capita (USD milhares)", fontsize=11, color="#3498db")
    ax1.tick_params(axis="y", labelcolor="#3498db")

    ax2 = ax1.twinx()
    ax2.plot(br["ano"], br["usuarios_internet_pct"], color="#e74c3c", marker="o", linewidth=2, label="Internet %")
    ax2.set_ylabel("Usuarios de Internet (%)", fontsize=11, color="#e74c3c")
    ax2.tick_params(axis="y", labelcolor="#e74c3c")
    plt.title("Brasil: Evolucao do PIB per capita e Infraestrutura Digital", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "brasil_evolucao.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: brasil_evolucao.png")


def correlacoes(df):
    print("\n" + "=" * 70)
    print("MATRIZ DE CORRELACAO")
    print("=" * 70)
    cols = ["pib_per_capita_usd", "crescimento_pib_pct", "abertura_comercial_pct_pib",
            "usuarios_internet_pct", "celulares_por_100", "gasto_publico_educacao_pct_pib"]
    cols_existentes = [c for c in cols if c in df.columns]
    df_corr = df[cols_existentes].dropna(how="all")
    corr = df_corr.corr(min_periods=10)
    print(corr.round(3))
    corr.to_csv(os.path.join(RAW, "correlacao_indicadores.csv"))

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols_existentes)))
    ax.set_yticks(range(len(cols_existentes)))
    ax.set_xticklabels(cols_existentes, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(cols_existentes, fontsize=9)
    for i in range(len(cols_existentes)):
        for j in range(len(cols_existentes)):
            val = corr.iloc[i, j]
            if not pd.isna(val):
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=10, color="black")
    plt.colorbar(im, ax=ax)
    ax.set_title("Correlacao entre Indicadores de Desenvolvimento", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "correlacao_indicadores.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: correlacao_indicadores.png")


def regressao(df):
    print("\n" + "=" * 70)
    print("REGRESSAO: Penetração Internet ~ PIB per capita + Educação + Celular")
    print("=" * 70)
    dfr = df.dropna(subset=["usuarios_internet_pct", "pib_per_capita_usd",
                            "gasto_publico_educacao_pct_pib", "celulares_por_100"]).copy()
    dfr["log_pib"] = np.log(dfr["pib_per_capita_usd"].astype(float))
    print(f"Observacoes validas: {len(dfr)}")
    if len(dfr) < 5:
        return
    X = dfr[["log_pib", "gasto_publico_educacao_pct_pib", "celulares_por_100"]].values
    X_ = np.column_stack([np.ones(len(X)), X])
    y = dfr["usuarios_internet_pct"].values
    beta, _, _, _ = np.linalg.lstsq(X_, y, rcond=None)
    y_hat = X_ @ beta
    ss_res = ((y - y_hat) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot
    print(f"\nCoeficientes:")
    print(f"  Intercepto: {beta[0]:.3f}")
    print(f"  log(PIB): {beta[1]:.3f}")
    print(f"  Gasto Educacao: {beta[2]:.3f}")
    print(f"  Celular por 100: {beta[3]:.3f}")
    print(f"R²: {r2:.3f}")


def main():
    df = carregar_dados()
    print(f"Observacoes: {len(df)}")
    print(f"Paises: {df['pais'].nunique()}")
    print(f"Periodo: {df['ano'].min()}-{df['ano'].max()}")

    estatisticas_descritivas(df)
    grafico_pib_per_capita(df)
    grafico_internet_celular(df)
    grafico_scatter_pib_internet(df)
    grafico_evolucao_pib_brasil(df)
    correlacoes(df)
    regressao(df)
    print("\nConcluido")


if __name__ == "__main__":
    main()
