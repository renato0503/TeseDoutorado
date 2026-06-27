"""
ARTIGO 23 - Coleta final com query focada e busca por ano
"""
import os
import time
import pandas as pd
import pyalex
from pyalex import Works

pyalex.config.email = "renato0503@gmail.com"
pyalex.config.max_retries = 5
pyalex.config.retry_backoff_factor = 1.0

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\23-Mapeamento-Producao-Cientifica-Governanca-Algoritmica\Raw_Data"


def buscar_por_ano(ano, termo="algorithmic governance"):
    """Busca artigos de um ano especifico que mencionam o termo."""
    time.sleep(3)
    query = Works().search(termo).filter(type="article", publication_year=str(ano))
    registros = []
    try:
        for page in query.paginate(per_page=100):
            for w in page:
                try:
                    autores = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
                    instituicoes = []
                    paises = []
                    for a in w.get("authorships", []):
                        for inst in a.get("institutions", []):
                            if inst.get("display_name"):
                                instituicoes.append(inst["display_name"])
                            if inst.get("country_code"):
                                paises.append(inst["country_code"])
                    conceitos = [c["display_name"] for c in w.get("concepts", []) if c.get("display_name")][:5]
                    loc = w.get("primary_location") or {}
                    src = loc.get("source") or {}
                    titulo = w.get("title") or ""
                    # Filtrar artigos com termos relevantes
                    texto_lower = titulo.lower()
                    if not any(t in texto_lower for t in ["governance", "algorithm", "ai", "public sector", "procurement"]):
                        continue
                    registros.append({
                        "id": w.get("id"),
                        "doi": w.get("doi"),
                        "titulo": titulo,
                        "ano": w.get("publication_year"),
                        "data_publicacao": w.get("publication_date"),
                        "periodico": src.get("display_name") if isinstance(src, dict) else None,
                        "tipo": w.get("type"),
                        "open_access": (w.get("open_access") or {}).get("is_oa") if w.get("open_access") else None,
                        "citacoes": w.get("cited_by_count"),
                        "fwci": w.get("fwci"),
                        "autores": "; ".join(autores) if autores else None,
                        "n_autores": len(autores),
                        "instituicoes": "; ".join(set(instituicoes)) if instituicoes else None,
                        "paises": "; ".join(set(paises)) if paises else None,
                        "conceitos": "; ".join(conceitos),
                    })
                except Exception:
                    continue
    except Exception as e:
        print(f"  ! Erro no ano {ano}: {e}")
    return registros


def main():
    print("Coletando artigos sobre 'algorithmic governance' por ano (2010-2024)...")
    total_geral = []
    for ano in range(2010, 2025):
        print(f"  - {ano}...", end=" ", flush=True)
        regs = buscar_por_ano(ano)
        print(f"{len(regs)} artigos relevantes")
        total_geral.extend(regs)

    df = pd.DataFrame(total_geral)
    # Remover duplicatas por ID
    df = df.drop_duplicates(subset="id").reset_index(drop=True)
    df.to_csv(os.path.join(OUT_DIR, "artigos_focados_2010_2024.csv"), index=False)
    print(f"\nTotal: {len(df)} artigos unicos salvos")

    # Gerar estatisticas
    if not df.empty:
        dist_ano = df.groupby("ano").size().reset_index(name="n_artigos").sort_values("ano")
        dist_ano.to_csv(os.path.join(OUT_DIR, "distribuicao_por_ano.csv"), index=False)
        print("\nDistribuicao por ano:")
        print(dist_ano.to_string(index=False))

        dist_per = (
            df.groupby("periodico").size()
            .reset_index(name="n_artigos")
            .sort_values("n_artigos", ascending=False)
            .head(30)
        )
        dist_per.to_csv(os.path.join(OUT_DIR, "distribuicao_por_periodico.csv"), index=False)

        paises_exp = df["paises"].dropna().str.split("; ").explode()
        paises_exp = paises_exp.str.strip()
        paises_exp = paises_exp[paises_exp != ""]
        dist_pais = paises_exp.value_counts().reset_index()
        dist_pais.columns = ["pais", "n_artigos"]
        dist_pais.to_csv(os.path.join(OUT_DIR, "distribuicao_por_pais.csv"), index=False)
        print(f"\nTotal de paises: {paises_exp.nunique()}")
        print(f"Top 5 paises: {dist_pais.head(5).to_dict('records')}")


if __name__ == "__main__":
    main()
