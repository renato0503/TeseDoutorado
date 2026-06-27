"""
ARTIGO 23 - Análise empírica
Mapeamento Bibliometrico via OpenAlex
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\23-Mapeamento-Producao-Cientifica-Governanca-Algoritmica"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(IMG, exist_ok=True)


def carregar_dados():
    df = pd.read_csv(os.path.join(RAW, "artigos_openalex.csv"))
    return df


def estatisticas_gerais(df):
    print("=" * 70)
    print("ESTATISTICAS GERAIS")
    print("=" * 70)
    print(f"Total de artigos: {len(df)}")
    print(f"Periodos distintos (citacoes preenchidas): {df['citacoes'].notna().sum()}")
    print(f"Citacoes totais: {int(df['citacoes'].sum()):,}")
    print(f"Citacoes medias: {df['citacoes'].mean():.1f}")
    print(f"Periodicos distintos: {df['periodico'].nunique()}")
    print(f"Artigos com pais: {df['paises'].notna().sum()}")


def distribuicao_por_ano(df):
    print("\n" + "=" * 70)
    print("DISTRIBUICAO POR ANO")
    print("=" * 70)
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    dist = df.groupby("ano").size().reset_index(name="n_artigos").sort_values("ano")
    print(dist.to_string(index=False))
    dist.to_csv(os.path.join(RAW, "distribuicao_por_ano.csv"), index=False)
    return dist


def grafico_distribuicao_ano(dist):
    fig, ax = plt.subplots(figsize=(11, 5))
    cores = plt.cm.viridis(np.linspace(0.1, 0.9, len(dist)))
    ax.bar(dist["ano"].astype(str), dist["n_artigos"], color=cores)
    ax.set_xlabel("Ano de Publicacao", fontsize=11)
    ax.set_ylabel("Numero de Artigos", fontsize=11)
    ax.set_title("Evolucao da Producao Cientifica sobre Governanca Algoritmica", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "distribuicao_ano.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: distribuicao_ano.png")


def top_periodicos(df):
    print("\n" + "=" * 70)
    print("TOP 20 PERIODICOS")
    print("=" * 70)
    top = df["periodico"].value_counts().head(20).reset_index()
    top.columns = ["periodico", "n_artigos"]
    print(top.to_string(index=False))
    top.to_csv(os.path.join(RAW, "top_periodicos.csv"), index=False)
    return top


def grafico_top_periodicos(top):
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(top["periodico"][::-1], top["n_artigos"][::-1], color=plt.cm.viridis(0.5))
    ax.set_xlabel("Numero de Artigos", fontsize=11)
    ax.set_title("Top 20 Periodicos em Governanca Algoritmica", fontsize=12)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "top_periodicos.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: top_periodicos.png")


def top_paises(df):
    print("\n" + "=" * 70)
    print("DISTRIBUICAO POR PAIS")
    print("=" * 70)
    paises = df["paises"].dropna().str.split("; ").explode()
    paises = paises.str.strip()
    paises = paises[paises != ""]
    top = paises.value_counts().head(20).reset_index()
    top.columns = ["pais", "n_artigos"]
    print(top.to_string(index=False))
    top.to_csv(os.path.join(RAW, "distribuicao_pais.csv"), index=False)
    return top


def grafico_top_paises(top):
    fig, ax = plt.subplots(figsize=(10, 6))
    cores = ["#27ae60" if p == "BR" else "#3498db" for p in top["pais"]]
    ax.barh(top["pais"][::-1], top["n_artigos"][::-1], color=cores[::-1])
    ax.set_xlabel("Numero de Artigos", fontsize=11)
    ax.set_title("Top 20 Paises em Governanca Algoritmica", fontsize=12)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "top_paises.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: top_paises.png")


def analise_brasil(df):
    """Analise especifica do Brasil."""
    brasil = df[df["paises"].fillna("").str.contains("BR")]
    print("\n" + "=" * 70)
    print("ANALISE BRASIL")
    print("=" * 70)
    print(f"Total de artigos com autor brasileiro: {len(brasil)}")
    if len(brasil) > 0:
        print(f"Periodo: {brasil['ano'].min()}-{brasil['ano'].max()}")
        top_br = brasil["periodico"].value_counts().head(10)
        print(f"\nTop periodicos BR:")
        print(top_br.to_string())
        top_br.to_csv(os.path.join(RAW, "brasil_top_periodicos.csv"))


def top_citados(df):
    print("\n" + "=" * 70)
    print("TOP 20 ARTIGOS MAIS CITADOS")
    print("=" * 70)
    df_sorted = df.sort_values("citacoes", ascending=False).head(20)
    out = df_sorted[["titulo", "ano", "periodico", "citacoes"]].copy()
    out["titulo"] = out["titulo"].str[:100]
    print(out.to_string(index=False))
    out.to_csv(os.path.join(RAW, "top_citados.csv"), index=False)


def main():
    df = carregar_dados()
    estatisticas_gerais(df)
    dist = distribuicao_por_ano(df)
    grafico_distribuicao_ano(dist)
    top_per = top_periodicos(df)
    grafico_top_periodicos(top_per)
    top_p = top_paises(df)
    grafico_top_paises(top_p)
    analise_brasil(df)
    top_citados(df)
    print("\nConcluido")


if __name__ == "__main__":
    main()
