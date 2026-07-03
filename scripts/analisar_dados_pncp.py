"""
Análise Consolidada dos Dados do PNCP
====================================
Este script processa os arquivos JSON de contratos do PNCP
para gerar estatísticas descritivas e datasets para os artigos.

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

# Paths
DADOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados")
PNCP_RAW = DADOS_DIR / "pncp_raw" / "contratos"
OUTPUT_DIR = DADOS_DIR / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("ANÁLISE CONSOLIDADA DOS DADOS DO PNCP - CONTRATOS")
print("=" * 70)

# Lista de arquivos JSON
json_files = sorted(PNCP_RAW.glob("contratos_*.json"))
print(f"\n[{len(json_files)}] arquivos JSON encontrados")

# Acumuladores
all_contracts = []
fornecedores_stats = defaultdict(lambda: {
    "qtd_contratos": 0,
    "valor_total": 0.0,
    "valor_medio": 0.0,
    "orgaos": set(),
    "ufs": set(),
    "cnpjs": set()
})

# Processar cada arquivo
for i, json_file in enumerate(json_files):
    print(f"  Processando {json_file.name}...", end=" ", flush=True)

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    # Extrair dados
                    forn_nome = item.get("nomeRazaoSocialFornecedor", "DESCONHECIDO")
                    forn_cnpj = item.get("niFornecedor", "ND")
                    forn_cnpj = forn_cnpj[:8] if forn_cnpj else "ND"  # CNPJ sem filial

                    valor = item.get("valorGlobal", 0)
                    if isinstance(valor, str):
                        valor = float(valor.replace(",", ".")) if valor else 0
                    valor = float(valor) if valor else 0

                    orgao = item.get("orgaoEntidade", {})
                    orgao_nome = orgao.get("razaoSocial", "ND") if isinstance(orgao, dict) else "ND"

                    unidade = item.get("unidadeOrgao", {})
                    uf = unidade.get("ufSigla", "ND") if isinstance(unidade, dict) else "ND"

                    objeto = item.get("objetoContrato", "")
                    tipo = item.get("tipoContrato", {})
                    tipo_nome = tipo.get("nome", "ND") if isinstance(tipo, dict) else "ND"

                    # Acumular
                    all_contracts.append({
                        "fornecedor_nome": forn_nome,
                        "fornecedor_cnpj": forn_cnpj,
                        "valor_global": valor,
                        "orgao": orgao_nome,
                        "uf": uf,
                        "objeto": objeto[:200] if objeto else "",
                        "tipo_contrato": tipo_nome,
                        "data_assinatura": item.get("dataAssinatura", ""),
                        "data_vigencia_inicio": item.get("dataVigenciaInicio", ""),
                        "data_vigencia_fim": item.get("dataVigenciaFim", ""),
                    })

                    # Estatísticas por fornecedor
                    stats = fornecedores_stats[forn_nome]
                    stats["qtd_contratos"] += 1
                    stats["valor_total"] += valor
                    stats["orgaos"].add(orgao_nome)
                    stats["ufs"].add(uf)
                    stats["cnpjs"].add(forn_cnpj)

            print(f"=> {len(data)} contratos")
        else:
            print("=> formato inválido")

    except Exception as e:
        print(f"ERRO: {e}")

print(f"\nTotal de contratos processados: {len(all_contracts):,}")

# Criar DataFrame
df = pd.DataFrame(all_contracts)
print(f"\nDataFrame criado com {len(df):,} registros")

# Estatísticas descritivas
print("\n" + "=" * 70)
print("ESTATÍSTICAS DESCRITIVAS")
print("=" * 70)

print(f"\n[1] FORNECEDORES")
print(f"    Fornecedores únicos: {df['fornecedor_nome'].nunique():,}")
print(f"    CNPJs únicos: {df['fornecedor_cnpj'].nunique():,}")

print(f"\n[2] VALOR")
print(f"    Valor Total: R$ {df['valor_global'].sum():,.2f}")
print(f"    Valor Médio: R$ {df['valor_global'].mean():,.2f}")
print(f"    Valor Mediano: R$ {df['valor_global'].median():,.2f}")
print(f"    Valor Máximo: R$ {df['valor_global'].max():,.2f}")
print(f"    Valor Mínimo: R$ {df['valor_global'].min():,.2f}")

# Filtrar outliers (valores muito altos ou zerados)
df_clean = df[(df['valor_global'] > 0) & (df['valor_global'] < 1_000_000_000)]
print(f"\n    (Após remover outliers e zeros: {len(df_clean):,} registros)")

print(f"\n[3] DISTRIBUIÇÃO POR UF")
uf_counts = df["uf"].value_counts().head(10)
for uf, count in uf_counts.items():
    print(f"    {uf}: {count:,}")

print(f"\n[4] TOP 10 FORNECEDORES POR VALOR")
top_fornecedores = df.groupby("fornecedor_nome").agg({
    "valor_global": "sum",
    "fornecedor_cnpj": "first",
}).sort_values("valor_global", ascending=False).head(10)
top_fornecedores["qtd_contratos"] = df.groupby("fornecedor_nome").size().loc[top_fornecedores.index]
top_fornecedores = top_fornecedores.reset_index()

for i, row in top_fornecedores.iterrows():
    print(f"    {i+1}. {row['fornecedor_nome'][:50]}")
    print(f"       CNPJ: {row['fornecedor_cnpj']}, Contratos: {int(row['qtd_contratos'])}, Valor: R$ {row['valor_global']:,.2f}")

print(f"\n[5] DISTRIBUIÇÃO POR TIPO DE CONTRATO")
tipo_counts = df["tipo_contrato"].value_counts()
for tipo, count in tipo_counts.items():
    print(f"    {tipo}: {count:,}")

# Salvar datasets processados
print("\n" + "=" * 70)
print("SALVANDO DADOS PROCESSADOS")
print("=" * 70)

# Dataset completo
output_all = OUTPUT_DIR / "pncp_contratos_full.csv"
df.to_csv(output_all, index=False, encoding="utf-8-sig")
print(f"  Dataset completo: {output_all}")

# Dataset de fornecedores
df_forn = pd.DataFrame([
    {
        "fornecedor": name,
        "cnpj": list(stats["cnpjs"])[0] if stats["cnpjs"] else "ND",
        "qtd_contratos": stats["qtd_contratos"],
        "valor_total": stats["valor_total"],
        "valor_medio": stats["valor_total"] / stats["qtd_contratos"] if stats["qtd_contratos"] > 0 else 0,
        "qtd_orgaos": len(stats["orgaos"]),
        "qtd_ufs": len(stats["ufs"]),
        "ufs": ",".join(sorted(stats["ufs"])),
    }
    for name, stats in fornecedores_stats.items()
]).sort_values("valor_total", ascending=False)

output_forn = OUTPUT_DIR / "pncp_fornecedores_ranking.csv"
df_forn.to_csv(output_forn, index=False, encoding="utf-8-sig")
print(f"  Ranking fornecedores: {output_forn}")

# Resumo executivo
resumo = {
    "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "periodo_coberto": "2021-08 a 2024-08",
    "total_contratos": len(df),
    "fornecedores_unicos": int(df['fornecedor_nome'].nunique()),
    "cnpjs_unicos": int(df['fornecedor_cnpj'].nunique()),
    "orgaos_unicos": int(df['orgao'].nunique()),
    "ufs_cobertas": int(df['uf'].nunique()),
    "valor_total": float(df['valor_global'].sum()),
    "valor_medio": float(df['valor_global'].mean()),
    "valor_mediano": float(df['valor_global'].median()),
    "top_fornecedor": top_fornecedores.iloc[0]["fornecedor_nome"] if len(top_fornecedores) > 0 else "ND",
    "top_fornecedor_valor": float(top_fornecedores.iloc[0]["valor_global"]) if len(top_fornecedores) > 0 else 0,
}

output_resumo = OUTPUT_DIR / "resumo_pncp_contratos.json"
with open(output_resumo, "w", encoding="utf-8") as f:
    json.dump(resumo, f, ensure_ascii=False, indent=2)
print(f"  Resumo JSON: {output_resumo}")

print("\n" + "=" * 70)
print("✅ ANÁLISE CONCLUÍDA!")
print("=" * 70)
print(f"\nArquivos gerados em: {OUTPUT_DIR}")
