"""
SPRINT 1.1: Construir target_real observavel a partir dos contratos PNCP.

Este script le os arquivos brutos de contratos do PNCP, extrai features
enriquecidas e constroi uma variavel dependente observavel (target_real)
baseada em desfechos administrativos reais:

  target_real = 1 se QUALQUER destes ocorrer:
    - valorAcumulado > valorGlobal * 1.10 (aditivo > 10%)
    - numeroRetificacao >= 2 (multiplas correcoes)
    - vigencia_dias < 30 (contrato efemero, possivel rescindido)
    - frutoAdesao = True (adesao ATA, maior risco de irregularidade)
    - temRemanejamento = True (orcamento alterado)
  target_real = 0 caso contrario

Saida:
  dados/processed/pncp_target_real.csv  (~100k linhas amostradas)
  dados/processed/target_distribution.json
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

RANDOM_SEED = 42
SAMPLE_SIZE = 100000
RAW_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados\pncp_raw\contratos")
OUT_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados\processed")
OUT_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("CONSTRUCAO DO TARGET REAL (OBSERVAVEL)")
print("=" * 60)

print("\n[1/5] Carregando arquivos brutos de contratos...")
all_files = sorted(RAW_DIR.glob("*.csv"))
dfs = []
total_rows = 0

for f in all_files:
    try:
        chunk = pd.read_csv(f, sep=";", encoding="utf-8", low_memory=False)
        dfs.append(chunk)
        total_rows += len(chunk)
    except Exception as e:
        print(f"  Erro ao ler {f.name}: {e}")

df = pd.concat(dfs, ignore_index=True)
print(f"  {len(all_files)} arquivos carregados")
print(f"  Total bruto: {total_rows:,} linhas")
print(f"  Colunas disponiveis: {len(df.columns)}")

print(f"\n[2/5] Selecionando colunas relevantes...")
cols_keep = [
    "numeroControlePNCP",
    "nomeRazaoSocialFornecedor",
    "niFornecedor",
    "objetoContrato",
    "valorInicial",
    "valorGlobal",
    "valorAcumulado",
    "dataVigenciaInicio",
    "dataVigenciaFim",
    "dataAssinatura",
    "numeroRetificacao",
    "frutoAdesao",
    "temRemanejamento",
    "receita",
    "tipoContrato.nome",
    "unidadeOrgao.ufSigla",
    "unidadeOrgao.nomeUnidade",
    "orgaoEntidade.razaoSocial",
]
cols_available = [c for c in cols_keep if c in df.columns]
df = df[cols_available].copy()
print(f"  {len(cols_available)}/{len(cols_keep)} colunas disponiveis")

print(f"\n[3/5] Limpeza e conversao de tipos...")
for col in ["valorInicial", "valorGlobal", "valorAcumulado"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

for col in ["dataVigenciaInicio", "dataVigenciaFim", "dataAssinatura"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

df["numeroRetificacao"] = pd.to_numeric(df["numeroRetificacao"], errors="coerce").fillna(0).astype(int)
df["frutoAdesao"] = df.get("frutoAdesao", pd.Series([False] * len(df))).fillna(False).astype(bool)
df["temRemanejamento"] = df.get("temRemanejamento", pd.Series([False] * len(df))).fillna(False).astype(bool)
df["receita"] = df.get("receita", pd.Series([False] * len(df))).fillna(False).astype(bool)

df["objetoContrato"] = df["objetoContrato"].fillna("").astype(str)
df["nomeRazaoSocialFornecedor"] = df.get("nomeRazaoSocialFornecedor", pd.Series([""] * len(df))).fillna("").astype(str)
df["niFornecedor"] = df.get("niFornecedor", pd.Series([""] * len(df))).fillna("").astype(str)

print(f"  Registros apos limpeza: {len(df):,}")

print(f"\n[4/5] Construindo target_real observavel...")
df["vigencia_dias"] = (
    (df["dataVigenciaFim"] - df["dataVigenciaInicio"]).dt.days
)
df["vigencia_dias"] = df["vigencia_dias"].fillna(0)
df["vigencia_dias"] = df["vigencia_dias"].clip(lower=0)

df["tem_valor_acumulado"] = df["valorAcumulado"] > 0

df["aditivo_valor"] = (
    (df["tem_valor_acumulado"]) &
    (df["valorAcumulado"] > df["valorGlobal"] * 1.10)
).astype(int)

df["multiplas_retificacoes"] = (df["numeroRetificacao"] >= 2).astype(int)
df["vigencia_curta"] = ((df["vigencia_dias"] < 30) & (df["vigencia_dias"] > 0)).astype(int)
df["adesao_ata"] = df["frutoAdesao"].astype(int)
df["houve_remanejamento"] = df["temRemanejamento"].astype(int)

df["target_real"] = (
    (df["aditivo_valor"] == 1) |
    (df["multiplas_retificacoes"] == 1) |
    (df["vigencia_curta"] == 1) |
    (df["adesao_ata"] == 1) |
    (df["houve_remanejamento"] == 1)
).astype(int)

dist = df["target_real"].value_counts()
pct_pos = df["target_real"].mean() * 100

print(f"  Distribuicao target_real:")
print(f"    Positivos (risco): {dist.get(1, 0):,} ({pct_pos:.1f}%)")
print(f"    Negativos (normal): {dist.get(0, 0):,} ({(100-pct_pos):.1f}%)")

print(f"\n  Contribuicao de cada criterio:")
for col in ["aditivo_valor", "multiplas_retificacoes", "vigencia_curta", "adesao_ata", "houve_remanejamento"]:
    count = df[col].sum()
    print(f"    {col}: {count:,} contratos ({count/len(df)*100:.1f}%)")

print(f"\n[5/5] Amostrando e salvando...")
sample_size = min(SAMPLE_SIZE, len(df))
df_sample = df.sample(sample_size, random_state=RANDOM_SEED).copy()
print(f"  Amostra: {sample_size:,} registros")

df_sample = df_sample.rename(columns={
    "objetoContrato": "objeto",
    "nomeRazaoSocialFornecedor": "fornecedor_nome",
    "niFornecedor": "fornecedor_cnpj",
    "valorGlobal": "valor_global",
    "unidadeOrgao.ufSigla": "uf",
    "tipoContrato.nome": "tipo_contrato",
    "unidadeOrgao.nomeUnidade": "orgao",
})

out_cols = [
    "fornecedor_nome", "fornecedor_cnpj", "valor_global", "orgao", "uf",
    "objeto", "tipo_contrato", "dataAssinatura", "dataVigenciaInicio",
    "dataVigenciaFim", "vigencia_dias", "aditivo_valor",
    "multiplas_retificacoes", "adesao_ata", "houve_remanejamento",
    "target_real",
]
out_cols = [c for c in out_cols if c in df_sample.columns]

out_path = OUT_DIR / "pncp_target_real.csv"
df_sample[out_cols].to_csv(out_path, index=False)
print(f"  Salvo: {out_path}")
print(f"  Tamanho: {out_path.stat().st_size / 1024 / 1024:.1f} MB")

metrics = {
    "data_construcao": datetime.now().isoformat(),
    "registros_total": int(len(df)),
    "registros_amostra": int(sample_size),
    "target_positivos": int(dist.get(1, 0)),
    "target_negativos": int(dist.get(0, 0)),
    "pct_positivos": round(pct_pos, 2),
    "criterios": {
        "aditivo_valor_pct": round(df["aditivo_valor"].mean() * 100, 2),
        "multiplas_retificacoes_pct": round(df["multiplas_retificacoes"].mean() * 100, 2),
        "vigencia_curta_pct": round(df["vigencia_curta"].mean() * 100, 2),
        "adesao_ata_pct": round(df["adesao_ata"].mean() * 100, 2),
        "houve_remanejamento_pct": round(df["houve_remanejamento"].mean() * 100, 2),
    },
}

metrics_path = OUT_DIR / "target_distribution.json"
with open(metrics_path, "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)
print(f"\nMetricas salvas: {metrics_path}")

print("\nCONCLUIDO: target_real construido com sucesso.")
