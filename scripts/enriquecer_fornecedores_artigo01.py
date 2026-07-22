"""
A1-S2: Enriquecer dados de fornecedores via BrasilAPI.

Coleta capital social, CNAE e porte dos CNPJs das compras complexas.

Uso: python scripts/enriquecer_fornecedores_artigo01.py
"""

import pandas as pd
import json
import time
import requests
from pathlib import Path

RANDOM_SEED = 42
ARTIGO_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\01-Artigo-Cientifico-Diagnostico\dados")
DADOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados\processed")

print("=" * 60)
print("ENRIQUECIMENTO DE FORNECEDORES — ARTIGO 01")
print("=" * 60)

df_complexas = pd.read_csv(DADOS_DIR / "pncp_compras_complexas.csv")
df_target = pd.read_csv(DADOS_DIR / "pncp_target_real.csv")

cnpjs = df_complexas["fornecedor_cnpj"].dropna().astype(str).unique()
cnpjs = [c.replace(".", "").replace("/", "").replace("-", "").strip().zfill(14) for c in cnpjs]
cnpjs = list(set(cnpjs))[:200]
print(f"  CNPJs unicos a consultar: {len(cnpjs)}")

resultados = []
erros = 0

for i, cnpj in enumerate(cnpjs):
    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            resultados.append({
                "cnpj": cnpj,
                "razao_social": data.get("razao_social", ""),
                "capital_social": float(data.get("capital_social", 0)),
                "porte": data.get("porte", ""),
                "cnae_principal": data.get("cnae_fiscal_descricao", ""),
                "natureza_juridica": data.get("natureza_juridica", ""),
                "uf": data.get("uf", ""),
                "municipio": data.get("municipio", ""),
            })
        elif resp.status_code == 404:
            pass
        else:
            erros += 1

        if (i + 1) % 20 == 0:
            print(f"  Progresso: {i+1}/{len(cnpjs)} | Sucessos: {len(resultados)} | Erros: {erros}")

        time.sleep(1.5)

    except Exception as e:
        erros += 1

print(f"\n  Consultas concluidas: {len(cnpjs)}")
print(f"  Sucessos: {len(resultados)}")
print(f"  Erros/nao encontrados: {erros}")

if resultados:
    df_out = pd.DataFrame(resultados)
    df_out["capital_social_log"] = df_out["capital_social"].apply(lambda x: float('nan') if x <= 0 else __import__('numpy').log1p(x))

    porte_map = {"01": "ME", "03": "EPP", "05": "Demais"}
    df_out["porte_label"] = df_out["porte"].map(porte_map).fillna("Nao informado")

    out_path = ARTIGO_DIR / "fornecedores_enriquecidos.csv"
    df_out.to_csv(out_path, index=False)
    print(f"\n  Dados salvos: {out_path}")
    print(f"  Registros: {len(df_out)}")
    print(f"  Capital social medio: R$ {df_out['capital_social'].mean():,.2f}")
    print(f"  Capital social mediano: R$ {df_out['capital_social'].median():,.2f}")
    print(f"  Distribuicao porte:")
    for porte, count in df_out["porte_label"].value_counts().items():
        print(f"    {porte}: {count}")

    stats = {
        "fornecedores_consultados": len(cnpjs),
        "fornecedores_encontrados": len(df_out),
        "capital_social_medio": round(float(df_out["capital_social"].mean()), 2),
        "capital_social_mediano": round(float(df_out["capital_social"].median()), 2),
        "distribuicao_porte": df_out["porte_label"].value_counts().to_dict(),
    }
    with open(ARTIGO_DIR / "stats_fornecedores.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

print("\nCONCLUIDO.")
