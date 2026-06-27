"""
ARTIGO 23 - Re-coleta OpenAlex com query corrigida
Busca todos os artigos (open access ou nao) sobre governanca algoritmica
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


def buscar_por_ano(ano):
    """Busca todos os artigos de um ano especifico."""
    time.sleep(2)
    query = Works().filter(type="article", publication_year=str(ano))
    registros = []
    try:
        for page in query.paginate(per_page=200):
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
                    registros.append({
                        "id": w.get("id"),
                        "doi": w.get("doi"),
                        "titulo": w.get("title"),
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
    print("Coletando artigos por ano (2010-2024)...")
    total_geral = []
    for ano in range(2010, 2025):
        print(f"  - {ano}...", end=" ")
        regs = buscar_por_ano(ano)
        print(f"{len(regs)} artigos")
        total_geral.extend(regs)
        # Salvar parcial a cada 5 anos para seguranca
        if ano % 5 == 0 or ano == 2024:
            df = pd.DataFrame(total_geral)
            df.to_csv(os.path.join(OUT_DIR, "artigos_por_ano_parcial.csv"), index=False)
            print(f"    [Parcial salvo: {len(df)} artigos]")

    df = pd.DataFrame(total_geral)
    df.to_csv(os.path.join(OUT_DIR, "artigos_completos_2010_2024.csv"), index=False)
    print(f"\nTotal: {len(df)} artigos salvos")


if __name__ == "__main__":
    main()
