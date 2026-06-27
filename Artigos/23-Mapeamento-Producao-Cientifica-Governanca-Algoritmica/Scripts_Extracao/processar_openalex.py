"""
ARTIGO 23 - Processamento dos dados do OpenAlex
Reaproveita artigos_openalex.csv ja coletado
e filtra por ano localmente
"""
import os
import pandas as pd

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\23-Mapeamento-Producao-Cientifica-Governanca-Algoritmica\Raw_Data"
START_YEAR = 2010
END_YEAR = 2024

print("[1/4] Carregando dataset bruto do OpenAlex...")
df = pd.read_csv(os.path.join(OUT_DIR, "artigos_openalex.csv"))
print(f"  -> {len(df)} artigos carregados")

# Limpar e converter ano
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
df["citacoes"] = pd.to_numeric(df.get("citacoes", pd.Series()), errors="coerce")
df["fwci"] = pd.to_numeric(df.get("fwci", pd.Series()), errors="coerce")
df["n_autores"] = pd.to_numeric(df.get("n_autores", pd.Series()), errors="coerce")

# Filtrar por ano (o filtro da API nao funcionou)
df_filtrado = df[(df["ano"] >= START_YEAR) & (df["ano"] <= END_YEAR)].copy()
print(f"  -> {len(df_filtrado)} artigos no periodo {START_YEAR}-{END_YEAR}")
df_filtrado.to_csv(os.path.join(OUT_DIR, "artigos_filtrados_2010_2024.csv"), index=False)

print("\n[2/4] Estatisticas de distribuicao por ano...")
dist_ano = df_filtrado.groupby("ano").size().reset_index(name="n_artigos")
dist_ano.to_csv(os.path.join(OUT_DIR, "distribuicao_por_ano.csv"), index=False)
print(dist_ano.to_string(index=False))

print("\n[3/4] Top periodicos...")
dist_per = (
    df_filtrado.groupby("periodico")
    .size()
    .reset_index(name="n_artigos")
    .sort_values("n_artigos", ascending=False)
    .head(30)
)
dist_per.to_csv(os.path.join(OUT_DIR, "distribuicao_por_periodico.csv"), index=False)
print(dist_per.head(15).to_string(index=False))

print("\n[4/4] Top paises...")
paises_exp = df_filtrado["paises"].dropna().str.split("; ").explode()
paises_exp = paises_exp.str.strip()
paises_exp = paises_exp[paises_exp != ""]
dist_pais = (
    paises_exp.value_counts()
    .reset_index()
)
dist_pais.columns = ["pais", "n_artigos"]
dist_pais.to_csv(os.path.join(OUT_DIR, "distribuicao_por_pais.csv"), index=False)
print(dist_pais.head(20).to_string(index=False))

print("\n[5/5] Top 50 artigos mais citados (base para cocitacao)...")
top = (
    df_filtrado.nlargest(50, "citacoes")[["id", "doi", "titulo", "ano", "citacoes", "fwci"]]
)
top.to_csv(os.path.join(OUT_DIR, "top_citados_50.csv"), index=False)
print(top.head(10).to_string(index=False))

# Estatisticas de citacoes
print("\n[Resumo]")
print(f"  Total de artigos (2010-2024): {len(df_filtrado)}")
print(f"  Citacoes totais: {int(df_filtrado['citacoes'].sum()):,}")
print(f"  Citacoes medias por artigo: {df_filtrado['citacoes'].mean():.1f}")
print(f"  FWCI medio: {df_filtrado['fwci'].mean():.2f}")
print(f"  Periodicos distintos: {df_filtrado['periodico'].nunique()}")
print(f"  Paises distintos: {paises_exp.nunique()}")
print("\nConcluido.")
