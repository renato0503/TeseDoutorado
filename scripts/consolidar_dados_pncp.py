"""
Consolidação dos dados do PNCP baixados
========================================
Este script consolida todos os arquivos CSV do PNCP em datasets
prontos para análise nos artigos.

Dados disponíveis:
- contratacoes: Ago/2021 a Ago/2024 (36 meses)
- contratos: Set/2021 a Ago/2024 (36 meses)
"""
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
DADOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados")
PNCP_RAW = DADOS_DIR / "pncp_raw"
OUTPUT_DIR = DADOS_DIR / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("CONSOLIDAÇÃO DOS DADOS DO PNCP")
print("=" * 70)

# ============================================================
# 1. CONTRATAÇÕES
# ============================================================
print("\n[1/4] Consolidando contratações...")

contratacoes_files = sorted(PNCP_RAW.glob("contratacoes/*.csv"))
print(f"   Encontrados {len(contratacoes_files)} arquivos")

dfs_contratacoes = []
for f in contratacoes_files:
    try:
        df = pd.read_csv(f, sep=";", encoding="utf-8", low_memory=False)
        dfs_contratacoes.append(df)
    except Exception as e:
        print(f"   ERRO em {f.name}: {e}")

if dfs_contratacoes:
    df_contratacoes = pd.concat(dfs_contratacoes, ignore_index=True)
    print(f"   Total de registros: {len(df_contratacoes):,}")

    # Estatísticas básicas
    print(f"\n   Colunas disponíveis:")
    for col in df_contratacoes.columns:
        print(f"      - {col}")

    # Limpar e converter valores
    if "valorTotalEstimado" in df_contratacoes.columns:
        df_contratacoes["valorTotalEstimado"] = pd.to_numeric(
            df_contratacoes["valorTotalEstimado"].astype(str).str.replace(",", "."),
            errors="coerce"
        ).fillna(0)

    if "valorTotalHomologado" in df_contratacoes.columns:
        df_contratacoes["valorTotalHomologado"] = pd.to_numeric(
            df_contratacoes["valorTotalHomologado"].astype(str).str.replace(",", "."),
            errors="coerce"
        ).fillna(0)

    # Extrair UF
    if "unidadeOrgao.ufSigla" in df_contratacoes.columns:
        df_contratacoes["uf"] = df_contratacoes["unidadeOrgao.ufSigla"].fillna("ND")

    # Estatísticas por UF
    print(f"\n   Top 10 UFs por número de contratações:")
    top_ufs = df_contratacoes["uf"].value_counts().head(10)
    for uf, count in top_ufs.items():
        print(f"      {uf}: {count:,}")

    # Estatísticas por modalidade
    if "modalidadeNome" in df_contratacoes.columns:
        print(f"\n   Contratações por modalidade:")
        for mod, count in df_contratacoes["modalidadeNome"].value_counts().items():
            print(f"      {mod}: {count:,}")

    # Fornecedores mais frequentes
    if "usuarioNome" in df_contratacoes.columns:
        print(f"\n   Top 10 fornecedores (por número de contratos):")
        top_fornecedores = df_contratacoes["usuarioNome"].value_counts().head(10)
        for forn, count in top_fornecedores.items():
            print(f"      {forn[:50]}: {count:,}")

    # Valor total
    valor_total_estimado = df_contratacoes["valorTotalEstimado"].sum()
    valor_total_homologado = df_contratacoes["valorTotalHomologado"].sum()
    print(f"\n   Valor Total Estimado: R$ {valor_total_estimado:,.2f}")
    print(f"   Valor Total Homologado: R$ {valor_total_homologado:,.2f}")

    # Salvar
    output_contratacoes = OUTPUT_DIR / "pncp_contratacoes_consolidado.csv"
    df_contratacoes.to_csv(output_contratacoes, index=False, encoding="utf-8-sig")
    print(f"\n   Salvo em: {output_contratacoes}")
else:
    print("   NENHUM arquivo de contratações encontrado!")

# ============================================================
# 2. CONTRATOS
# ============================================================
print("\n[2/4] Consolidando contratos...")

contratos_files = sorted(PNCP_RAW.glob("contratos/*.csv"))
print(f"   Encontrados {len(contratos_files)} arquivos")

dfs_contratos = []
for f in contratos_files:
    try:
        df = pd.read_csv(f, sep=";", encoding="utf-8", low_memory=False)
        dfs_contratos.append(df)
    except Exception as e:
        print(f"   ERRO em {f.name}: {e}")

if dfs_contratos:
    df_contratos = pd.concat(dfs_contratos, ignore_index=True)
    print(f"   Total de registros: {len(df_contratos):,}")

    print(f"\n   Colunas disponíveis:")
    for col in df_contratos.columns:
        print(f"      - {col}")

    # Limpar valores
    for col in ["valorInicial", "valorGlobal", "valorAcumulado"]:
        if col in df_contratos.columns:
            df_contratos[col] = pd.to_numeric(
                df_contratos[col].astype(str).str.replace(",", "."),
                errors="coerce"
            ).fillna(0)

    # UF
    if "unidadeOrgao.ufSigla" in df_contratos.columns:
        df_contratos["uf"] = df_contratos["unidadeOrgao.ufSigla"].fillna("ND")

    # Fornecedores únicos
    if "nomeRazaoSocialFornecedor" in df_contratos.columns:
        fornecedores_unicos = df_contratos["nomeRazaoSocialFornecedor"].nunique()
        print(f"\n   Fornecedores únicos: {fornecedores_unicos:,}")

    # Órgãos únicos
    if "orgaoEntidade.razaoSocial" in df_contratos.columns:
        orgaos_unicos = df_contratos["orgaoEntidade.razaoSocial"].nunique()
        print(f"   Órgãos únicos: {orgaos_unicos:,}")

    # Valor total
    if "valorGlobal" in df_contratos.columns:
        valor_total = df_contratos["valorGlobal"].sum()
        print(f"   Valor Total Global: R$ {valor_total:,.2f}")

    # Salvar
    output_contratos = OUTPUT_DIR / "pncp_contratos_consolidado.csv"
    df_contratos.to_csv(output_contratos, index=False, encoding="utf-8-sig")
    print(f"\n   Salvo em: {output_contratos}")
else:
    print("   NENHUM arquivo de contratos encontrado!")

# ============================================================
# 3. CRUZAMENTO CONTRATOS x FORNECEDORES
# ============================================================
print("\n[3/4] Gerando cruzamento de contratos com fornecedores...")

if 'df_contratos' in dir() and not df_contratos.empty:
    # Criar dataframe de fornecedores com estatísticas
    if "nomeRazaoSocialFornecedor" in df_contratos.columns:
        forn_stats = df_contratos.groupby("nomeRazaoSocialFornecedor").agg({
            "valorGlobal": ["sum", "mean", "count"],
            "numeroControlePncpCompra": "nunique"
        }).reset_index()
        forn_stats.columns = ["fornecedor", "valor_total", "valor_medio", "qtd_contratos", "qtd_orgaos"]
        forn_stats = forn_stats.sort_values("valor_total", ascending=False)

        print(f"\n   Top 10 fornecedores por valor:")
        for i, row in forn_stats.head(10).iterrows():
            print(f"      {row['fornecedor'][:50]}: R$ {row['valor_total']:,.2f} ({row['qtd_contratos']} contratos)")

        # Salvar
        output_forn = OUTPUT_DIR / "fornecedores_estatisticas.csv"
        forn_stats.to_csv(output_forn, index=False, encoding="utf-8-sig")
        print(f"\n   Salvo em: {output_forn}")

# ============================================================
# 4. RESUMO EXECUTIVO
# ============================================================
print("\n[4/4] Gerando resumo executivo...")

resumo = {
    "contratacoes_total": len(df_contratacoes) if 'df_contratacoes' in dir() and not df_contratacoes.empty else 0,
    "contratos_total": len(df_contratos) if 'df_contratos' in dir() and not df_contratos.empty else 0,
    "fornecedores_unicos": df_contratos["nomeRazaoSocialFornecedor"].nunique() if 'df_contratos' in dir() and not df_contratos.empty and "nomeRazaoSocialFornecedor" in df_contratos.columns else 0,
    "orgaos_unicos": df_contratos["orgaoEntidade.razaoSocial"].nunique() if 'df_contratos' in dir() and not df_contratos.empty and "orgaoEntidade.razaoSocial" in df_contratos.columns else 0,
    "valor_total_contratacoes": df_contratacoes["valorTotalEstimado"].sum() if 'df_contratacoes' in dir() and not df_contratacoes.empty and "valorTotalEstimado" in df_contratacoes.columns else 0,
    "valor_total_contratos": df_contratos["valorGlobal"].sum() if 'df_contratos' in dir() and not df_contratos.empty and "valorGlobal" in df_contratos.columns else 0,
    "periodo_inicio": "2021-08",
    "periodo_fim": "2024-08",
    "ufs_cobertas": df_contratacoes["uf"].nunique() if 'df_contratacoes' in dir() and not df_contratacoes.empty and "uf" in df_contratacoes.columns else 0,
}

print(f"""
================================================================================
RESUMO EXECUTIVO - DADOS PNCP CONSOLIDADOS
================================================================================
Período: {resumo['periodo_inicio']} a {resumo['periodo_fim']}
--------------------------------------------------------------------------------
Contratações:     {resumo['contratacoes_total']:>15,} registros
Contratos:       {resumo['contratos_total']:>15,} registros
Fornecedores:   {resumo['fornecedores_unicos']:>15,} únicos
Órgãos:         {resumo['orgaos_unicos']:>15,} únicos
UFscapturadas:  {resumo['ufs_cobertas']:>15}
--------------------------------------------------------------------------------
Valor Total (Contratações): R$ {resumo['valor_total_contratacoes']:>15,.2f}
Valor Total (Contratos):    R$ {resumo['valor_total_contratos']:>15,.2f}
================================================================================
""")

# Salvar resumo
import json
output_resumo = OUTPUT_DIR / "resumo_executivo.json"
with open(output_resumo, "w", encoding="utf-8") as f:
    json.dump(resumo, f, ensure_ascii=False, indent=2)
print(f"Resumo salvo em: {output_resumo}")

print("\n✅ CONSOLIDAÇÃO CONCLUÍDA!")
