"""
Preparação de Datasets do PNCP para Artigos
============================================
Este script processa os dados consolidados do PNCP
e gera datasets específicos para cada artigo.

Autor: Renato de Oliveira Rosa
Data: 02/07/2026
"""
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
from datetime import datetime

print("=" * 70)
print("PREPARAÇÃO DE DATASETS PNCP PARA ARTIGOS")
print("=" * 70)

# Carregar dados processados
DADOS_PROCESSED = Path(r"C:\Users\Renato\Documents\Doutorado\dados\processed")
ARTIGOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\Artigos")

df = pd.read_csv(DADOS_PROCESSED / "pncp_contratos_full.csv", encoding="utf-8-sig")
print(f"\nCarregados {len(df):,} contratos")

# DataFrame de ranking de fornecedores
df_ranking = pd.read_csv(DADOS_PROCESSED / "pncp_fornecedores_ranking.csv", encoding="utf-8-sig")

print("\n" + "=" * 70)
print("ARTIGO 20 - RISCO DE CRÉDITO DE FORNECEDORES")
print("=" * 70)

# Dataset para Artigo 20: Fornecedores com histórico de contratos
art20_output = ARTIGOS_DIR / "20-Risco-Credito-Fornecedores-Custos-Transacao" / "Raw_Data"

# 1. Dataset de fornecedores com métricas de risco
df_risco = df.groupby("fornecedor_cnpj").agg({
    "fornecedor_nome": "first",
    "valor_global": ["sum", "mean", "count", "std"],
    "orgao": "nunique",
    "uf": "nunique",
    "data_assinatura": ["min", "max"]
}).reset_index()

df_risco.columns = [
    "cnpj_fornecedor",
    "nome_fornecedor",
    "valor_total_contratos",
    "valor_medio_contrato",
    "qtd_contratos",
    "desvio_padrao_valor",
    "qtd_orgaos",
    "qtd_ufs",
    "primeiro_contrato",
    "ultimo_contrato"
]

# Calcular métricas de concentração
df_risco["participacao_mercado"] = df_risco["valor_total_contratos"] / df_risco["valor_total_contratos"].sum() * 100
df_risco["tempo_relacionamento"] = (pd.to_datetime(df_risco["ultimo_contrato"]) - pd.to_datetime(df_risco["primeiro_contrato"])).dt.days

# Score de risco simplificado (baseado em quantidade de contratos e dispersão)
df_risco["score_risco"] = (
    np.log1p(df_risco["qtd_contratos"]) * 0.3 +
    np.log1p(df_risco["qtd_orgaos"]) * 0.3 +
    np.log1p(df_risco["qtd_ufs"]) * 0.2 +
    np.log1p(df_risco["tempo_relacionamento"].fillna(0)) * 0.2
)

df_risco = df_risco.sort_values("score_risco", ascending=False)

output_risco = art20_output / "pncp_fornecedores_risco.csv"
df_risco.to_csv(output_risco, index=False, encoding="utf-8-sig")
print(f"  Dataset fornecedores risco: {output_risco.name} ({len(df_risco):,} registros)")

# 2. Dataset de contratos por UF para análise de concentração
df_uf = df.groupby(["uf", "fornecedor_cnpj"]).agg({
    "valor_global": "sum",
    "fornecedor_nome": "first",
}).reset_index()
df_uf.columns = ["uf", "cnpj_fornecedor", "valor_total_uf", "nome_fornecedor"]
df_uf["qtd_contratos"] = df.groupby(["uf", "fornecedor_cnpj"]).size().values
df_uf = df_uf.sort_values(["uf", "valor_total_uf"], ascending=[True, False])

output_uf = art20_output / "pncp_concentracao_uf.csv"
df_uf.to_csv(output_uf, index=False, encoding="utf-8-sig")
print(f"  Dataset concentração UF: {output_uf.name} ({len(df_uf):,} registros)")

# 3. Estatísticas descritivas para o artigo
estatisticas = {
    "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "periodo": "2021-09 a 2024-08",
    "total_contratos": int(len(df)),
    "fornecedores_unicos": int(df["fornecedor_cnpj"].nunique()),
    "valor_total": float(df["valor_global"].sum()),
    "valor_medio": float(df["valor_global"].mean()),
    "valor_mediano": float(df["valor_global"].median()),
    "desvio_padrao": float(df["valor_global"].std()),
    "valor_minimo": float(df["valor_global"].min()),
    "valor_maximo": float(df["valor_global"].max()),
    "cnpjs_maior_risco": df_risco.head(20)[["cnpj_fornecedor", "nome_fornecedor", "qtd_contratos", "score_risco"]].to_dict("records"),
}

output_estat = art20_output / "pncp_estatisticas_contratos.json"
with open(output_estat, "w", encoding="utf-8") as f:
    json.dump(estatisticas, f, ensure_ascii=False, indent=2)
print(f"  Estatísticas JSON: {output_estat.name}")

print("\n" + "=" * 70)
print("ARTIGO 18 - COMPLIANCE ALGORÍTMICO")
print("=" * 70)

art18_output = ARTIGOS_DIR / "18-Compliance-Algoritmico-Integrado" / "Raw_Data"

# Dataset de compliance: anomalias e padrões
# 1. Contratos com valores outliers (alto desvio padrão)
df_compliance = df.copy()
df_compliance["valor_zscore"] = (df_compliance["valor_global"] - df_compliance["valor_global"].mean()) / df_compliance["valor_global"].std()

# Marcar anomalias
df_compliance["flag_outlier"] = np.abs(df_compliance["valor_zscore"]) > 3
df_compliance["flag_valor_zero"] = df_compliance["valor_global"] == 0

# Estatísticas por órgão para compliance
df_compliance_orgaos = df_compliance.groupby("orgao").agg({
    "valor_global": ["sum", "mean", "std", "count"],
    "flag_outlier": "sum",
    "flag_valor_zero": "sum",
    "fornecedor_cnpj": "nunique"
}).reset_index()

df_compliance_orgaos.columns = [
    "orgao", "valor_total", "valor_medio", "desvio_padrao", "qtd_contratos",
    "qtd_outliers", "qtd_valores_zero", "fornecedores_unicos"
]

# Razão de outliers por órgão
df_compliance_orgaos["razao_outliers"] = df_compliance_orgaos["qtd_outliers"] / df_compliance_orgaos["qtd_contratos"] * 100

# Score de compliance (menor é melhor - menos anomalias)
df_compliance_orgaos["score_compliance"] = (
    df_compliance_orgaos["razao_outliers"] * 0.5 +
    (df_compliance_orgaos["qtd_valores_zero"] / df_compliance_orgaos["qtd_contratos"].replace(0, 1)) * 0.5
)

df_compliance_orgaos = df_compliance_orgaos.sort_values("score_compliance", ascending=False)

output_compliance = art18_output / "pncp_compliance_orgaos.csv"
df_compliance_orgaos.to_csv(output_compliance, index=False, encoding="utf-8-sig")
print(f"  Dataset compliance órgãos: {output_compliance.name} ({len(df_compliance_orgaos):,} registros)")

# 2. Fornecedores com padrões suspeitos
df_fornecedores_suspeitos = df_compliance.groupby("fornecedor_cnpj").agg({
    "valor_global": ["sum", "mean", "std", "count"],
    "flag_outlier": "sum",
    "orgao": "nunique",
    "uf": "nunique"
}).reset_index()

df_fornecedores_suspeitos.columns = [
    "cnpj", "valor_total", "valor_medio", "desvio_padrao", "qtd_contratos",
    "qtd_outliers", "qtd_orgaos", "qtd_ufs"
]

df_fornecedores_suspeitos = df_fornecedores_suspeitos.sort_values("qtd_outliers", ascending=False).head(100)

output_suspeitos = art18_output / "pncp_fornecedores_suspeitos.csv"
df_fornecedores_suspeitos.to_csv(output_suspeitos, index=False, encoding="utf-8-sig")
print(f"  Dataset fornecedores suspeitos: {output_suspeitos.name} ({len(df_fornecedores_suspeitos):,} registros)")

print("\n" + "=" * 70)
print("ARTIGO 03 - PREDIÇÃO DE FRACASSO CONTRATUAL")
print("=" * 70)

art03_output = ARTIGOS_DIR / "03-Predicao-Fracasso-Risco-Aditivos-Cancelamentos" / "Raw_Data"

# Dataset de inadimplência/adiantamento baseado em vigência
df_fracasso = df.copy()
df_fracasso["data_vigencia_inicio"] = pd.to_datetime(df_fracasso["data_vigencia_inicio"], errors="coerce")
df_fracasso["data_vigencia_fim"] = pd.to_datetime(df_fracasso["data_vigencia_fim"], errors="coerce")
df_fracasso["duracao_contrato"] = (df_fracasso["data_vigencia_fim"] - df_fracasso["data_vigencia_inicio"]).dt.days

# Flag de contrato de curta duração (< 30 dias = suspeito)
df_fracasso["flag_curta_duracao"] = df_fracasso["duracao_contrato"] < 30
df_fracasso["flag_duracao_zero"] = df_fracasso["duracao_contrato"] <= 0

# Flag de valor atípico (muito baixo para o objeto)
df_fracasso["flag_valor_atipico"] = df_fracasso["valor_global"] < 100

# Contratos vigentes vs encerrados
df_fracasso["data_assinatura_dt"] = pd.to_datetime(df_fracasso["data_assinatura"], errors="coerce")
df_fracasso["ano_assinatura"] = df_fracasso["data_assinatura_dt"].dt.year

# Dataset para predição
df_predicao = df_fracasso.groupby("fornecedor_cnpj").agg({
    "valor_global": ["sum", "mean", "count", "std"],
    "duracao_contrato": ["mean", "min", "max"],
    "flag_curta_duracao": "sum",
    "flag_duracao_zero": "sum",
    "flag_valor_atipico": "sum",
    "ano_assinatura": ["min", "max"],
    "orgao": "nunique"
}).reset_index()

df_predicao.columns = [
    "cnpj_fornecedor", "valor_total", "valor_medio", "qtd_contratos", "desvio_valor",
    "duracao_media", "duracao_min", "duracao_max",
    "qtd_curta_duracao", "qtd_duracao_zero", "qtd_valor_atipico",
    "primeiro_contrato", "ultimo_contrato", "qtd_orgaos"
]

# Score de risco de fracasso (maior = mais provável)
df_predicao["score_fracasso"] = (
    (df_predicao["qtd_curta_duracao"] / df_predicao["qtd_contratos"].replace(0, 1)) * 30 +
    (df_predicao["qtd_duracao_zero"] / df_predicao["qtd_contratos"].replace(0, 1)) * 30 +
    (df_predicao["qtd_valor_atipico"] / df_predicao["qtd_contratos"].replace(0, 1)) * 20 +
    (1 / (np.log1p(df_predicao["qtd_contratos"]) + 1)) * 20
)

df_predicao = df_predicao.sort_values("score_fracasso", ascending=False)

output_fracasso = art03_output / "pncp_risco_fracasso.csv"
df_predicao.to_csv(output_fracasso, index=False, encoding="utf-8-sig")
print(f"  Dataset risco fracasso: {output_fracasso.name} ({len(df_predicao):,} registros)")

print("\n" + "=" * 70)
print("ARTIGO 05 - REDES DE FORNECIMENTO E OLIGOPÓLIOS")
print("=" * 70)

art05_output = ARTIGOS_DIR / "05-Redes-Fornecimento-Oligopolios-Analise-Grafos" / "Raw_Data"

# Dataset de arestas para grafo (fornecedor-UF)
edges_uf = df.groupby(["fornecedor_cnpj", "uf"]).agg({
    "valor_global": "sum",
    "fornecedor_nome": "first",
}).reset_index()
edges_uf["qtd_contratos"] = df.groupby(["fornecedor_cnpj", "uf"]).size().values
edges_uf.columns = ["source", "target", "weight", "source_name", "qtd_contratos"]

# Filtrar apenas relações significativas (> R$ 1 milhão ou > 5 contratos)
edges_uf_filtered = edges_uf[(edges_uf["weight"] > 1_000_000) | (edges_uf["qtd_contratos"] > 5)]

output_edges_uf = art05_output / "pncp_grafo_fornecedor_uf.csv"
edges_uf_filtered.to_csv(output_edges_uf, index=False, encoding="utf-8-sig")
print(f"  Dataset grafo Fornecedor-UF: {output_edges_uf.name} ({len(edges_uf_filtered):,} arestas)")

# Dataset de arestas Fornecedor-Órgão
edges_orgao = df.groupby(["fornecedor_cnpj", "orgao"]).agg({
    "valor_global": "sum",
    "fornecedor_nome": "first",
}).reset_index()
edges_orgao["qtd_contratos"] = df.groupby(["fornecedor_cnpj", "orgao"]).size().values
edges_orgao.columns = ["source", "target", "weight", "source_name", "qtd_contratos"]

# Filtrar apenas relações significativas
edges_orgao_filtered = edges_orgao[(edges_orgao["weight"] > 5_000_000) | (edges_orgao["qtd_contratos"] > 10)]

output_edges_orgao = art05_output / "pncp_grafo_fornecedor_orgao.csv"
edges_orgao_filtered.to_csv(output_edges_orgao, index=False, encoding="utf-8-sig")
print(f"  Dataset grafo Fornecedor-Órgão: {output_edges_orgao.name} ({len(edges_orgao_filtered):,} arestas)")

# Nós do grafo (fornecedores)
nodes_fornecedores = df.groupby("fornecedor_cnpj").agg({
    "fornecedor_nome": "first",
    "valor_global": "sum",
    "uf": "nunique",
    "orgao": "nunique"
}).reset_index()
nodes_fornecedores["qtd_contratos"] = df.groupby("fornecedor_cnpj").size().values
nodes_fornecedores.columns = ["id", "label", "weight", "qtd_ufs", "qtd_orgaos", "qtd_contratos"]

# Centralidade simplificada (baseada em valor e dispersão)
nodes_fornecedores["centrality"] = (
    np.log1p(nodes_fornecedores["weight"]) * 0.4 +
    np.log1p(nodes_fornecedores["qtd_ufs"]) * 0.3 +
    np.log1p(nodes_fornecedores["qtd_orgaos"]) * 0.3
)

nodes_fornecedores = nodes_fornecedores.sort_values("centrality", ascending=False)

output_nodes = art05_output / "pncp_grafo_nos_fornecedores.csv"
nodes_fornecedores.to_csv(output_nodes, index=False, encoding="utf-8-sig")
print(f"  Dataset nós fornecedores: {output_nodes.name} ({len(nodes_fornecedores):,} nós)")

print("\n" + "=" * 70)
print("ARTIGO 02 - AUDITORIA CONTÍNUA E ANOMALIAS")
print("=" * 70)

art02_output = ARTIGOS_DIR / "02-Auditoria-Continua-Deteccao-Anomalias-Precos" / "Raw_Data"

# Dataset de anomalias por UF e modalidade
df_anomalias = df.copy()

# Calcular estatísticas por UF
estat_uf = df_anomalias.groupby("uf")["valor_global"].agg(["mean", "std", "median"]).reset_index()
estat_uf.columns = ["uf", "media_uf", "desvio_uf", "mediana_uf"]
df_anomalias = df_anomalias.merge(estat_uf, on="uf", how="left")

# Calcular desvio do valor em relação à UF
df_anomalias["desvio_zscore_uf"] = (df_anomalias["valor_global"] - df_anomalias["media_uf"]) / df_anomalias["desvio_uf"].replace(0, 1)
df_anomalias["flag_anomalia_uf"] = np.abs(df_anomalias["desvio_zscore_uf"]) > 2.5

# Dataset de anomalias
df_anomalias_dataset = df_anomalias[df_anomalias["flag_anomalia_uf"]].copy()
df_anomalias_dataset = df_anomalias_dataset[[
    "fornecedor_nome", "fornecedor_cnpj", "orgao", "uf", "valor_global",
    "media_uf", "desvio_zscore_uf", "tipo_contrato", "data_assinatura", "objeto"
]]

output_anomalias = art02_output / "pncp_anomalias_uf.csv"
df_anomalias_dataset.to_csv(output_anomalias, index=False, encoding="utf-8-sig")
print(f"  Dataset anomalias UF: {output_anomalias.name} ({len(df_anomalias_dataset):,} registros)")

# Estatísticas por UF
df_estat_uf = estat_uf.copy()
df_estat_uf["qtd_contratos"] = df_anomalias.groupby("uf").size().values
df_estat_uf["qtd_anomalias"] = df_anomalias.groupby("uf")["flag_anomalia_uf"].sum().values
df_estat_uf["razao_anomalias"] = df_estat_uf["qtd_anomalias"] / df_estat_uf["qtd_contratos"] * 100

output_estat_uf = art02_output / "pncp_estatisticas_uf.csv"
df_estat_uf.to_csv(output_estat_uf, index=False, encoding="utf-8-sig")
print(f"  Dataset estatísticas UF: {output_estat_uf.name} ({len(df_estat_uf):,} UFs)")

print("\n" + "=" * 70)
print("ARTIGO 11 - VOZ DO MERCADO (IMPUGNAÇÕES)")
print("=" * 70)

art11_output = ARTIGOS_DIR / "11-Voz-Mercado-Analise-Impugnacoes-Editais-Tecnologia" / "Raw_Data"

# Dataset de objetos de compra por UF
df_objetos = df.copy()
df_objetos["objeto_upper"] = df_objetos["objeto"].str.upper()

# Palavras-chave de tecnologia
tech_keywords = ["SOFTWARE", "INFORMÁTICA", "TECNOLOGIA", "SISTEMA", "COMPUTADOR", "SERVIDOR", "REDE", "INTERNET", "CLOUD", "DIGITAL"]
df_tech = df_objetos[df_objetos["objeto_upper"].str.contains("|".join(tech_keywords), na=False)]

df_tech_agg = df_tech.groupby(["uf", "tipo_contrato"]).agg({
    "valor_global": ["sum", "mean", "count"],
    "fornecedor_cnpj": "nunique"
}).reset_index()
df_tech_agg.columns = ["uf", "tipo_contrato", "valor_total", "valor_medio", "qtd_contratos", "fornecedores_unicos"]

output_tech = art11_output / "pncp_compras_tecnologia.csv"
df_tech_agg.to_csv(output_tech, index=False, encoding="utf-8-sig")
print(f"  Dataset compras tecnologia: {output_tech.name} ({len(df_tech_agg):,} registros)")

# Dataset de fornecedor por objeto (para análise de concentração)
df_concentracao = df_tech.groupby("fornecedor_cnpj").agg({
    "fornecedor_nome": "first",
    "valor_global": ["sum", "mean", "count"],
    "uf": "nunique",
    "tipo_contrato": "nunique"
}).reset_index()
df_concentracao.columns = ["cnpj", "nome", "valor_total", "valor_medio", "qtd_contratos", "qtd_ufs", "qtd_tipos"]

output_concentracao = art11_output / "pncp_fornecedores_tecnologia.csv"
df_concentracao = df_concentracao.sort_values("valor_total", ascending=False)
df_concentracao.to_csv(output_concentracao, index=False, encoding="utf-8-sig")
print(f"  Dataset fornecedores tecnologia: {output_concentracao.name} ({len(df_concentracao):,} registros)")

print("\n" + "=" * 70)
print("ARTIGO 24 - EFICIÊNCIA COMPRAS PÚBLICAS CROSS-COUNTRY")
print("=" * 70)

art24_output = ARTIGOS_DIR / "24-Determinantes-Eficiencia-Compras-Publicas-Cross-Country" / "Raw_Data"

# Dataset de estatísticas por UF para cross-country
df_cross = df.groupby("uf").agg({
    "valor_global": ["sum", "mean", "median", "std", "count"],
    "fornecedor_cnpj": "nunique",
    "orgao": "nunique"
}).reset_index()

df_cross.columns = [
    "uf", "valor_total", "valor_medio", "valor_mediano", "desvio_padrao", "qtd_contratos",
    "fornecedores_unicos", "orgaos_unicos"
]

# Métricas de eficiência
df_cross["valor_por_contrato"] = df_cross["valor_total"] / df_cross["qtd_contratos"]
df_cross["fornecedores_por_contrato"] = df_cross["fornecedores_unicos"] / df_cross["qtd_contratos"]
df_cross["concentracao_contratos"] = df_cross["qtd_contratos"] / df_cross["orgaos_unicos"]
df_cross["valor_por_orgao"] = df_cross["valor_total"] / df_cross["orgaos_unicos"]

output_cross = art24_output / "pncp_estatisticas_uf.csv"
df_cross.to_csv(output_cross, index=False, encoding="utf-8-sig")
print(f"  Dataset cross-country UF: {output_cross.name} ({len(df_cross):,} UFs)")

print("\n" + "=" * 70)
print("RESUMO DOS DATASETS GERADOS")
print("=" * 70)

datasets_gerados = {
    "Artigo 20 - Risco de Crédito": [
        str(output_risco.relative_to(ARTIGOS_DIR.parent)),
        str(output_uf.relative_to(ARTIGOS_DIR.parent)),
        str(output_estat.relative_to(ARTIGOS_DIR.parent)),
    ],
    "Artigo 18 - Compliance": [
        str(output_compliance.relative_to(ARTIGOS_DIR.parent)),
        str(output_suspeitos.relative_to(ARTIGOS_DIR.parent)),
    ],
    "Artigo 03 - Fracasso": [
        str(output_fracasso.relative_to(ARTIGOS_DIR.parent)),
    ],
    "Artigo 05 - Redes": [
        str(output_edges_uf.relative_to(ARTIGOS_DIR.parent)),
        str(output_edges_orgao.relative_to(ARTIGOS_DIR.parent)),
        str(output_nodes.relative_to(ARTIGOS_DIR.parent)),
    ],
    "Artigo 02 - Auditoria": [
        str(output_anomalias.relative_to(ARTIGOS_DIR.parent)),
        str(output_estat_uf.relative_to(ARTIGOS_DIR.parent)),
    ],
    "Artigo 11 - Voz Mercado": [
        str(output_tech.relative_to(ARTIGOS_DIR.parent)),
        str(output_concentracao.relative_to(ARTIGOS_DIR.parent)),
    ],
    "Artigo 24 - Cross-Country": [
        str(output_cross.relative_to(ARTIGOS_DIR.parent)),
    ],
}

for artigo, datasets in datasets_gerados.items():
    print(f"\n{artigo}:")
    for ds in datasets:
        print(f"  - {ds}")

print("\n" + "=" * 70)
print("✅ PROCESSAMENTO CONCLUÍDO!")
print("=" * 70)
