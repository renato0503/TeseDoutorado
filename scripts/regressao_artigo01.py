"""
A1-S1: Regressao logistica para o Artigo 01 (Diagnostico Empirico).

Estima modelo Logit com target_real como VD e caracteristicas
da unidade compradora e do contrato como IVs, conforme orientacao
do professor (Direcionamento.md §5).

Hipotese central: O fracasso em compras publicas decorre de fatores
estruturais (porte do orgao, tipo de compra, vigencia), nao de
omissao comportamental do gestor ("apagao das canetas").

Uso: python scripts/regressao_artigo01.py
"""

import pandas as pd
import numpy as np
import json
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report
from pathlib import Path

RANDOM_SEED = 42
DADOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados\processed")
ARTIGO_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\01-Artigo-Cientifico-Diagnostico\dados")
ARTIGO_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("REG RESSAO LOGISTICA — ARTIGO 01")
print("=" * 60)

# ============================================================
# 1. CARREGAR DADOS
# ============================================================
print("\n[1/5] Carregando dados...")

df = pd.read_csv(DADOS_DIR / "pncp_target_real.csv")
df_complexas = pd.read_csv(DADOS_DIR / "pncp_compras_complexas.csv")

df["objeto"] = df["objeto"].fillna("").astype(str)
df["valor_global"] = pd.to_numeric(df["valor_global"], errors="coerce").fillna(0)
df["vigencia_dias"] = pd.to_numeric(df["vigencia_dias"], errors="coerce").fillna(0)

complexas_ids = set(df_complexas["objeto"].dropna().astype(str).str[:80].unique())
df["is_complexa"] = df["objeto"].str[:80].isin(complexas_ids).astype(int)

n_complexas = df["is_complexa"].sum()
n_normais = len(df) - n_complexas

print(f"  Total: {len(df):,} contratos")
print(f"  Complexas: {n_complexas:,} ({n_complexas/len(df)*100:.1f}%)")
print(f"  Normais: {n_normais:,} ({n_normais/len(df)*100:.1f}%)")

# ============================================================
# 2. ANALISE COMPARATIVA (COMPLEXAS vs. NORMAIS)
# ============================================================
print("\n[2/5] Analise comparativa: complexas vs. normais...")

fracasso_complexas = df[df["is_complexa"] == 1]["target_real"].mean()
fracasso_normais = df[df["is_complexa"] == 0]["target_real"].mean()
odds_complexas = fracasso_complexas / (1 - fracasso_complexas) if fracasso_complexas < 1 else float("inf")
odds_normais = fracasso_normais / (1 - fracasso_normais)
odds_ratio = odds_complexas / odds_normais if odds_normais > 0 else float("inf")

n1 = n_complexas
n2 = n_normais
p1 = fracasso_complexas
p2 = fracasso_normais
p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
z_stat = (p1 - p2) / se if se > 0 else 0
from scipy import stats as scipy_stats
p_value_z = 2 * (1 - scipy_stats.norm.cdf(abs(z_stat)))

comp_stats = {
    "taxa_fracasso_complexas": round(fracasso_complexas * 100, 2),
    "taxa_fracasso_normais": round(fracasso_normais * 100, 2),
    "diferenca_pp": round((fracasso_complexas - fracasso_normais) * 100, 2),
    "odds_ratio": round(odds_ratio, 3),
    "z_statistic": round(z_stat, 3),
    "p_value_z": round(p_value_z, 4),
    "n_complexas": int(n_complexas),
    "n_normais": int(n_normais),
}

print(f"  Taxa fracasso - Complexas: {comp_stats['taxa_fracasso_complexas']:.1f}%")
print(f"  Taxa fracasso - Normais:  {comp_stats['taxa_fracasso_normais']:.1f}%")
print(f"  Diferenca: {comp_stats['diferenca_pp']:.1f} pp")
print(f"  Odds Ratio: {comp_stats['odds_ratio']:.3f}")
print(f"  z = {z_stat:.2f}, p = {p_value_z:.4f} {'***' if p_value_z < 0.001 else '**' if p_value_z < 0.01 else '*' if p_value_z < 0.05 else 'ns'}")

# ============================================================
# 3. ENGENHARIA DE FEATURES PARA REGRESSAO
# ============================================================
print("\n[3/5] Preparando features para regressao...")

df["valor_log"] = np.log1p(df["valor_global"])
df["vigencia_log"] = np.log1p(df["vigencia_dias"].clip(lower=1))
df["porte_orgao_log"] = np.log1p(df["valor_global"])

le_uf = pd.factorize(df["uf"].fillna("ND"))[0]
df["uf_encoded"] = le_uf

X_vars = [
    "is_complexa",
    "vigencia_log",
    "valor_log",
]
X = df[X_vars].copy()
X = sm.add_constant(X)
y = df["target_real"].astype(int)

print(f"  Features: {X_vars}")
print(f"  Observacoes: {len(X):,}")

# ============================================================
# 4. ESTIMAR REGRESSAO LOGISTICA
# ============================================================
print("\n[4/5] Estimando regressao logistica...")

model = sm.Logit(y, X)
result = model.fit(disp=False)

print(result.summary())

coef_table = []
for i, var in enumerate(X.columns):
    coef = result.params[i]
    se = result.bse[i]
    z_val = result.tvalues[i]
    p_val = result.pvalues[i]
    or_val = np.exp(coef)
    ci_lower = np.exp(coef - 1.96 * se)
    ci_upper = np.exp(coef + 1.96 * se)

    sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
    coef_table.append({
        "variavel": var,
        "coeficiente_beta": round(coef, 4),
        "erro_padrao": round(se, 4),
        "z": round(z_val, 4),
        "p_valor": round(p_val, 4),
        "significancia": sig,
        "odds_ratio": round(or_val, 4),
        "ic_95_lower": round(ci_lower, 4),
        "ic_95_upper": round(ci_upper, 4),
    })
    print(f"  {var:20s}  beta={coef:8.4f}  SE={se:7.4f}  z={z_val:7.2f}  p={p_val:.4f} {sig}  OR={or_val:.4f}")

y_pred_proba = result.predict(X)
y_pred = (y_pred_proba >= 0.5).astype(int)
auc = roc_auc_score(y, y_pred_proba)
acc = (y_pred == y).mean()
cm = confusion_matrix(y, y_pred)

pseudo_r2 = result.prsquared

print(f"\n  Pseudo R2 (McFadden): {pseudo_r2:.4f}")
print(f"  Acuracia: {acc*100:.2f}%")
print(f"  AUC-ROC: {auc*100:.2f}%")
print(f"  Matriz de confusao:")
print(f"    TN={cm[0][0]:,}  FP={cm[0][1]:,}")
print(f"    FN={cm[1][0]:,}  TP={cm[1][1]:,}")

# ============================================================
# 5. SALVAR RESULTADOS
# ============================================================
print("\n[5/5] Salvando resultados...")

resultados = {
    "data_estimacao": pd.Timestamp.now().isoformat(),
    "n_observacoes": int(len(X)),
    "n_complexas": int(n_complexas),
    "n_normais": int(n_normais),
    "comparativo_complexas_vs_normais": comp_stats,
    "pseudo_r2_mcfadden": round(pseudo_r2, 4),
    "acuracia": round(acc, 4),
    "auc_roc": round(auc, 4),
    "matriz_confusao": {"tn": int(cm[0][0]), "fp": int(cm[0][1]), "fn": int(cm[1][0]), "tp": int(cm[1][1])},
    "coeficientes": coef_table,
    "hipoteses": [
        {"id": "H1", "enunciado": "O tipo de compra (complexa vs. normal) esta positivamente associado a probabilidade de fracasso", "variavel": "is_complexa", "suportada": coef_table[1]["p_valor"] < 0.05},
        {"id": "H2", "enunciado": "A vigencia do contrato esta negativamente associada a probabilidade de fracasso", "variavel": "vigencia_log", "suportada": coef_table[2]["p_valor"] < 0.05 and coef_table[2]["coeficiente_beta"] < 0},
        {"id": "H3", "enunciado": "O valor do contrato esta positivamente associado a probabilidade de fracasso", "variavel": "valor_log", "suportada": coef_table[3]["p_valor"] < 0.05},
    ],
}

with open(ARTIGO_DIR / "resultados_regressao.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print(f"  Resultados salvos: {ARTIGO_DIR / 'resultados_regressao.json'}")

print("\n" + "=" * 60)
print("HIPOTESES TESTADAS")
print("=" * 60)
for h in resultados["hipoteses"]:
    status = "SUPORTADA" if h["suportada"] else "NAO SUPORTADA"
    print(f"  {h['id']}: {h['enunciado']}")
    print(f"    Status: {status}")

print("\nCONCLUIDO: Regressao estimada com sucesso.")
