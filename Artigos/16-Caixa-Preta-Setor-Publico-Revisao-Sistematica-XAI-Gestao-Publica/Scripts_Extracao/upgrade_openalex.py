"""
ARTIGO 16 - UPGRADE com OpenAlex
Validacao cruzada da revisao sistematica local de XAI no setor publico
contra a base OpenAlex (8.309+ artigos relacionados)
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pyalex
from pyalex import Works

pyalex.config.email = "renato0503@gmail.com"
pyalex.config.max_retries = 3

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica"
RAW_LOCAL = r"C:\Users\Renato\Documents\Doutorado\Base_de_Dados_e_APIs\Raw_Data\Revisao_Sistematica\xai_public_sector.csv"
RAW_NEW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(RAW_NEW, exist_ok=True)
os.makedirs(IMG, exist_ok=True)


def carregar_local():
    print("=" * 70)
    print("CARREGANDO BASE LOCAL (52 artigos)")
    print("=" * 70)
    df = pd.read_csv(RAW_LOCAL)
    print(f"  -> {len(df)} artigos locais")
    print(f"  Colunas: {df.columns.tolist()[:10]}")
    return df


def buscar_openalex():
    print("\n" + "=" * 70)
    print("BUSCANDO NO OPENALEX: explainable AI + public sector")
    print("=" * 70)
    query = (
        Works()
        .search("explainable AI")
        .filter(type="article", is_oa=True)
    )
    registros = []
    n = 0
    for page in query.paginate(per_page=200):
        for w in page:
            try:
                titulo = w.get("title") or ""
                if not any(t in titulo.lower() for t in ["explainable", "xai", "interpretable", "transparency", "black box"]):
                    continue
                autores = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
                paises = []
                for a in w.get("authorships", []):
                    for inst in a.get("institutions", []):
                        if inst.get("country_code"):
                            paises.append(inst["country_code"])
                loc = w.get("primary_location") or {}
                src = loc.get("source") or {}
                conceitos = [c["display_name"] for c in w.get("concepts", []) if c.get("display_name")][:5]
                registros.append({
                    "id": w.get("id"),
                    "doi": w.get("doi"),
                    "titulo": titulo,
                    "ano": w.get("publication_year"),
                    "periodico": src.get("display_name") if isinstance(src, dict) else None,
                    "citacoes": w.get("cited_by_count"),
                    "fwci": w.get("fwci"),
                    "open_access": (w.get("open_access") or {}).get("is_oa"),
                    "autores": "; ".join(autores) if autores else None,
                    "n_autores": len(autores),
                    "paises": "; ".join(set(paises)) if paises else None,
                    "conceitos": "; ".join(conceitos),
                })
                n += 1
                if n % 100 == 0:
                    print(f"  ... {n} artigos relevantes")
            except Exception:
                continue
        if n > 1500:  # Limite para nao demorar muito
            break
    df = pd.DataFrame(registros).drop_duplicates(subset="id")
    df.to_csv(os.path.join(RAW_NEW, "xai_openalex.csv"), index=False)
    print(f"  -> {len(df)} artigos unicos salvos")
    return df


def comparacao(local, openalex):
    print("\n" + "=" * 70)
    print("COMPARACAO: LOCAL vs OPENALEX")
    print("=" * 70)
    # Cobertura por ano
    local["ano"] = pd.to_numeric(local.get("Publication Year", local.get("year", pd.Series())), errors="coerce")
    openalex["ano"] = pd.to_numeric(openalex["ano"], errors="coerce")
    dist_local = local.groupby("ano").size().reset_index(name="n_artigos")
    dist_open = openalex.groupby("ano").size().reset_index(name="n_artigos")
    dist_local["fonte"] = "Local (52 artigos)"
    dist_open["fonte"] = "OpenAlex"
    combinado = pd.concat([dist_local, dist_open], ignore_index=True)
    combinado.to_csv(os.path.join(RAW_NEW, "comparacao_distribuicao.csv"), index=False)
    print("\nLocal:")
    print(dist_local.tail(5).to_string(index=False))
    print("\nOpenAlex:")
    print(dist_open.tail(5).to_string(index=False))

    # Grafico comparativo
    fig, ax = plt.subplots(figsize=(12, 6))
    for fonte, grupo in combinado.groupby("fonte"):
        grupo_sorted = grupo.sort_values("ano")
        ax.plot(grupo_sorted["ano"], grupo_sorted["n_artigos"],
                marker="o", label=fonte, linewidth=2)
    ax.set_xlabel("Ano", fontsize=11)
    ax.set_ylabel("Numero de Artigos", fontsize=11)
    ax.set_title("Comparacao: Revisao Local vs OpenAlex", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "comparacao_local_openalex.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: comparacao_local_openalex.png")


def grafico_conceitos_openalex(df):
    """Top conceitos relacionados a XAI."""
    conceitos = df["conceitos"].dropna().str.split("; ").explode()
    conceitos = conceitos.str.strip()
    conceitos = conceitos[conceitos != ""]
    top = conceitos.value_counts().head(20).reset_index()
    top.columns = ["conceito", "n"]
    top.to_csv(os.path.join(RAW_NEW, "top_conceitos_xai.csv"), index=False)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(top["conceito"][::-1], top["n"][::-1], color=plt.cm.viridis(0.5))
    ax.set_xlabel("Frequencia")
    ax.set_title("Top 20 Conceitos relacionados a XAI no OpenAlex", fontsize=12)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "top_conceitos_xai.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: top_conceitos_xai.png")


def main():
    local = carregar_local()
    openalex = buscar_openalex()
    if not openalex.empty:
        comparacao(local, openalex)
        grafico_conceitos_openalex(openalex)
    print("\nConcluido. Arquivos em:", RAW_NEW)


if __name__ == "__main__":
    main()
