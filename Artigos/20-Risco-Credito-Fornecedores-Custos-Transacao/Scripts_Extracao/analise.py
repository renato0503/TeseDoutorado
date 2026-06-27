"""
ARTIGO 20 - Análise empírica
Score de Risco de Credito de Fornecedores Publicos
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\20-Risco-Credito-Fornecedores-Custos-Transacao"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(IMG, exist_ok=True)


def carregar_dados():
    metrics = pd.read_csv(os.path.join(RAW, "credit_metrics_snapshot.csv"))
    precos = pd.read_csv(os.path.join(RAW, "precos_fechamento.csv"), index_col=0, parse_dates=True)
    vol = pd.read_csv(os.path.join(RAW, "volatilidade_anual.csv"), index_col=0)
    return metrics, precos, vol


def estatisticas_descritivas(metrics):
    print("=" * 70)
    print("ESTATISTICAS DESCRITIVAS - INDICADORES DE RISCO")
    print("=" * 70)
    cols = ["market_cap", "total_debt", "total_equity", "debt_to_equity",
            "current_ratio", "interest_coverage", "beta"]
    desc = metrics[cols].describe().T.round(3)
    print(desc)
    desc.to_csv(os.path.join(RAW, "estatisticas_descritivas_risco.csv"))
    return desc


def classificar_risco(metrics):
    """Classifica empresas em faixas de risco baseado em leverage e cobertura de juros."""
    df = metrics.copy()
    # Quanto maior o endividamento, maior o risco
    # Quanto menor a cobertura de juros, maior o risco
    condicoes = [
        (df["debt_to_equity"] < 50) & (df["interest_coverage"] > 5),
        ((df["debt_to_equity"] >= 50) & (df["debt_to_equity"] < 150)) |
        ((df["interest_coverage"] <= 5) & (df["interest_coverage"] > 2)),
        (df["debt_to_equity"] >= 150) | (df["interest_coverage"] <= 2),
    ]
    classes = ["Baixo Risco", "Medio Risco", "Alto Risco"]
    df["classificacao_risco"] = np.select(condicoes, classes, default="Medio Risco")
    print("\nClassificacao de risco:")
    print(df[["ticker", "nome", "debt_to_equity", "interest_coverage", "classificacao_risco"]].to_string(index=False))
    df.to_csv(os.path.join(RAW, "credit_classificacao.csv"), index=False)
    return df


def grafico_leverage_coverage(metrics):
    fig, ax = plt.subplots(figsize=(11, 7))
    cores = {"Baixo Risco": "#2ecc71", "Medio Risco": "#f39c12", "Alto Risco": "#e74c3c"}
    df = classificar_risco(metrics)
    for classe in cores.keys():
        subset = df[df["classificacao_risco"] == classe]
        if not subset.empty:
            ax.scatter(
                subset["debt_to_equity"], subset["interest_coverage"],
                s=200, alpha=0.7, c=cores[classe], label=classe, edgecolors="black",
            )
            for _, row in subset.iterrows():
                ax.annotate(row["ticker"], (row["debt_to_equity"], row["interest_coverage"]),
                            fontsize=9, ha="center", va="center", fontweight="bold", color="white")
    ax.set_xlabel("Debt/Equity (%)", fontsize=12)
    ax.set_ylabel("Interest Coverage (x)", fontsize=12)
    ax.set_title("Mapa de Risco de Credito: Leverage vs Cobertura de Juros", fontsize=13)
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)
    # Filtra apenas valores positivos para escala log
    if (df["interest_coverage"] > 0).all():
        ax.set_yscale("log")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "mapa_risco_credito.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: mapa_risco_credito.png")


def grafico_volatilidade_risco(vol, metrics):
    fig, ax = plt.subplots(figsize=(11, 6))
    df_vol = vol.reset_index()
    df_vol.columns = ["ticker", "vol_anual"]
    df = df_vol.merge(metrics[["ticker", "debt_to_equity"]], on="ticker", how="left").dropna()
    df_sorted = df.sort_values("vol_anual", ascending=True)
    cores = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(df_sorted)))
    bars = ax.barh(df_sorted["ticker"], df_sorted["vol_anual"], color=cores)
    for i, (_, row) in enumerate(df_sorted.iterrows()):
        if not pd.isna(row["debt_to_equity"]):
            ax.text(row["vol_anual"] + 0.5, i, f"D/E: {row['debt_to_equity']:.0f}%",
                    va="center", fontsize=8, color="dimgray")
    ax.set_xlabel("Volatilidade anualizada (%)", fontsize=12)
    ax.set_title("Volatilidade vs Endividamento", fontsize=13)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "volatilidade_endividamento.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: volatilidade_endividamento.png")


def correlacoes(metrics):
    print("\n" + "=" * 70)
    print("MATRIZ DE CORRELACAO - INDICADORES DE RISCO")
    print("=" * 70)
    cols = ["debt_to_equity", "current_ratio", "interest_coverage",
            "profit_margin", "return_on_assets", "beta"]
    df = metrics[cols].dropna(how="all")
    # Calcular correlacao par a par
    corr = df.corr(min_periods=3)
    print(corr.round(3))
    corr.to_csv(os.path.join(RAW, "correlacao_indicadores.csv"))

    # Heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(cols, fontsize=9)
    for i in range(len(cols)):
        for j in range(len(cols)):
            val = corr.iloc[i,j]
            if not pd.isna(val):
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=10, color="black")
    plt.colorbar(im, ax=ax, label="Correlacao de Pearson")
    ax.set_title("Correlacao entre Indicadores de Risco", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "correlacao_indicadores.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: correlacao_indicadores.png")


def main():
    metrics, precos, vol = carregar_dados()
    print(f"Empresas: {len(metrics)}")
    print(f"Periodo de precos: {precos.index[0].date()} a {precos.index[-1].date()}")

    desc = estatisticas_descritivas(metrics)
    grafico_leverage_coverage(metrics)
    grafico_volatilidade_risco(vol, metrics)
    correlacoes(metrics)

    # Relatorio
    with open(os.path.join(RAW, "relatorio_analise.txt"), "w", encoding="utf-8") as f:
        f.write("RELATORIO DE ANALISE - ARTIGO 20\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total de empresas: {len(metrics)}\n")
        f.write(f"Periodo: {precos.index[0].date()} a {precos.index[-1].date()}\n\n")
        f.write("ESTATISTICAS DESCRITIVAS:\n")
        f.write(desc.to_string() + "\n")
    print("\nConcluido")


if __name__ == "__main__":
    main()
