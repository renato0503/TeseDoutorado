"""
ARTIGO 23 - Coleta via OpenAlex API
Mapeamento Bibliometrico da Governanca Algoritmica

OpenAlex: https://openalex.org/
Acesso gratuito e completo, com e-mail para prioridade (polite pool).
"""
import os
import pandas as pd
import pyalex
from pyalex import Works, Authors, Institutions, Concepts

# Polite pool: identifique-se com e-mail institucional
pyalex.config.email = "renato0503@gmail.com"
pyalex.config.max_retries = 3
pyalex.config.retry_backoff_factor = 0.5

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\23-Mapeamento-Producao-Cientifica-Governanca-Algoritmica\Raw_Data"
os.makedirs(OUT_DIR, exist_ok=True)

START_YEAR = 2010
END_YEAR = 2024


def buscar_artigos():
    print(f"[1/3] Buscando artigos sobre governanca algoritmica no OpenAlex ({START_YEAR}-{END_YEAR})...")
    from_year_clause = f"|".join(str(y) for y in range(START_YEAR, END_YEAR + 1))
    query = (
        Works()
        .search("algorithmic governance")
        .filter(type="article", is_oa=True, publication_year=from_year_clause)
        .sort(publication_year="desc")
    )
    registros = []
    n = 0
    for page in query.paginate(per_page=200):
        for w in page:
            try:
                autores = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
                instituicoes = []
                for a in w.get("authorships", []):
                    for inst in a.get("institutions", []):
                        if inst.get("display_name"):
                            instituicoes.append(inst["display_name"])
                paises = []
                for a in w.get("authorships", []):
                    for inst in a.get("institutions", []):
                        if inst.get("country_code"):
                            paises.append(inst["country_code"])
                conceitos = [c["display_name"] for c in w.get("concepts", []) if c.get("display_name")][:5]
                registros.append({
                    "id": w.get("id"),
                    "doi": w.get("doi"),
                    "titulo": w.get("title"),
                    "ano": w.get("publication_year"),
                    "data_publicacao": w.get("publication_date"),
                    "periodico": (w.get("primary_location") or {}).get("source", {}).get("display_name") if w.get("primary_location") else None,
                    "tipo": w.get("type"),
                    "open_access": w.get("open_access", {}).get("is_oa") if w.get("open_access") else None,
                    "citacoes": w.get("cited_by_count"),
                    "fwci": w.get("fwci"),
                    "autores": "; ".join(autores) if autores else None,
                    "n_autores": len(autores),
                    "instituicoes": "; ".join(set(instituicoes)) if instituicoes else None,
                    "paises": "; ".join(set(paises)) if paises else None,
                    "conceitos": "; ".join(conceitos),
                    "resumo": w.get("abstract_inverted_index"),
                })
                n += 1
                if n % 100 == 0:
                    print(f"  ... {n} artigos coletados")
            except Exception as e:
                print(f"  ! Erro em {w.get('id')}: {e}")
    df = pd.DataFrame(registros)
    df.to_csv(os.path.join(OUT_DIR, "artigos_openalex.csv"), index=False)
    print(f"  -> {len(df)} artigos salvos em artigos_openalex.csv")
    return df


def analise_distribuicao(df):
    if df is None or df.empty:
        df = pd.read_csv(os.path.join(OUT_DIR, "artigos_openalex.csv"))
    print("[2/3] Gerando estatisticas de distribuicao...")
    # Por ano
    por_ano = df.groupby("ano").size().reset_index(name="n_artigos")
    por_ano.to_csv(os.path.join(OUT_DIR, "distribuicao_por_ano.csv"), index=False)
    print(f"  -> {len(por_ano)} anos distintos")
    # Por periodico
    por_periodico = df.groupby("periodico").size().reset_index(name="n_artigos").sort_values("n_artigos", ascending=False)
    por_periodico.to_csv(os.path.join(OUT_DIR, "distribuicao_por_periodico.csv"), index=False)
    # Por pais
    paises_exp = df["paises"].dropna().str.split("; ").explode()
    por_pais = paises_exp.value_counts().reset_index()
    por_pais.columns = ["pais", "n_artigos"]
    por_pais.to_csv(os.path.join(OUT_DIR, "distribuicao_por_pais.csv"), index=False)
    print(f"  -> Distribuicoes salvas")


def criar_template_cocitacao(df):
    if df is None or df.empty:
        df = pd.read_csv(os.path.join(OUT_DIR, "artigos_openalex.csv"))
    print("[3/3] Criando template de cocitacao...")
    # Top 50 artigos mais citados serao usados para matriz de cocitacao
    top = df.nlargest(50, "citacoes")[["id", "doi", "titulo", "ano", "citacoes"]]
    top.to_csv(os.path.join(OUT_DIR, "top_citados_template.csv"), index=False)
    print(f"  -> Top 50 artigos salvos para analise de cocitacao")


if __name__ == "__main__":
    df = buscar_artigos()
    analise_distribuicao(df)
    criar_template_cocitacao(df)
    print("\nConcluido. Arquivos em:", OUT_DIR)
