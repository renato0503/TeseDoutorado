import sys
from pathlib import Path
PRODUTO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PRODUTO_DIR))

import pandas as pd
import numpy as np
import pickle
import json
import warnings
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
import shap

warnings.filterwarnings("ignore")

SAVED_DIR = Path(__file__).resolve().parent / "saved"
SAVED_DIR.mkdir(exist_ok=True)

DADOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados\processed")
TARGET_REAL = DADOS_DIR / "pncp_target_real.csv"
CONTRATOS_FULL = DADOS_DIR / "pncp_contratos_full.csv"

RANDOM_SEED = 42

print("=" * 60)
print("TREINAMENTO DOS MODELOS DO COPILOTO (v2 - target observavel)")
print("=" * 60)

print("\n[1/7] Carregando dados...")
df_target = pd.read_csv(TARGET_REAL)
print(f"  Alvo observavel: {len(df_target):,} registros, "
      f"{df_target['target_real'].mean()*100:.2f}% positivos")

df_full = pd.read_csv(CONTRATOS_FULL, nrows=100000)
df_full["objeto"] = df_full["objeto"].fillna("").astype(str)
print(f"  Contratos full (para TF-IDF/IF): {len(df_full):,} registros")

print("\n[2/7] Engenharia de features (alvo observavel)...")
df_target["objeto"] = df_target["objeto"].fillna("").astype(str)
df_target["valor_global"] = pd.to_numeric(df_target["valor_global"], errors="coerce").fillna(0)
df_target["vigencia_dias"] = pd.to_numeric(df_target["vigencia_dias"], errors="coerce").fillna(365)
df_target["vigencia_dias"] = df_target["vigencia_dias"].clip(lower=1)

df_target["objeto_palavras"] = df_target["objeto"].str.split().str.len()
df_target["objeto_palavras_unicas"] = df_target["objeto"].apply(
    lambda x: len(set(x.lower().split()))
)
df_target["complexidade_lexica"] = df_target["objeto_palavras_unicas"] / df_target["objeto_palavras"].clip(lower=1)

KW_TECNICAS = [
    "tecnologia", "software", "sistema", "inovacao", "inovação", "p&d",
    "inteligência artificial", "inteligencia artificial", "startup",
    "sustentável", "sustentavel", "esg", "eficiência energética",
    "eficiencia energetica", "logística reversa", "logistica reversa",
]
df_target["score_tecnico"] = df_target["objeto"].str.lower().apply(
    lambda x: sum(1 for kw in KW_TECNICAS if kw in x)
)
df_target["valor_log"] = np.log1p(df_target["valor_global"])
df_target["vigencia_log"] = np.log1p(df_target["vigencia_dias"])

oe_uf = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1, dtype=np.int32)
uf_values = df_target[["uf"]].fillna("ND").astype(str)
df_target["uf_encoded"] = oe_uf.fit_transform(uf_values).flatten()

oe_tipo = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1, dtype=np.int32)
tipo_values = df_target[["tipo_contrato"]].fillna("ND").astype(str)
df_target["tipo_encoded"] = oe_tipo.fit_transform(tipo_values).flatten()

df_target["target_real"] = (
    (df_target["aditivo_valor"] == 1) |
    (df_target["multiplas_retificacoes"] == 1)
).astype(int)

target = df_target["target_real"].values
print(f"  Target: {target.mean()*100:.2f}% positivos ({int(target.sum()):,} de {len(target):,})")

print("\n[3/7] TF-IDF + Isolation Forest...")
vectorizer = TfidfVectorizer(
    max_features=500,
    stop_words=None,
    ngram_range=(1, 2),
    min_df=2,
)
objetos_sample = df_full["objeto"].sample(min(15000, len(df_full)), random_state=RANDOM_SEED)
tfidf_matrix = vectorizer.fit_transform(objetos_sample)
print(f"  TF-IDF matriz: {tfidf_matrix.shape}")

isolation = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=RANDOM_SEED,
    n_jobs=-1,
)
isolation.fit(tfidf_matrix.toarray())
print(f"  Isolation Forest treinado com {len(objetos_sample)} objetos")

print("\n[4/7] Aplicando IF + interacoes no dataset alvo...")
objetos_alvo = vectorizer.transform(df_target["objeto"])
if_scores = isolation.score_samples(objetos_alvo.toarray())
if_preds = isolation.predict(objetos_alvo.toarray())

df_target["if_anomaly_score"] = 1.0 / (1.0 + np.exp(-if_scores))
df_target["if_anomaly_score"] = (df_target["if_anomaly_score"] * 2 - 1).clip(0, 1)
df_target["if_is_anomaly"] = (if_preds == -1).astype(int)
df_target["interacao_if_valor"] = df_target["if_anomaly_score"] * df_target["valor_log"]
df_target["interacao_if_vigencia"] = df_target["if_anomaly_score"] * df_target["vigencia_log"]

print(f"  IF anomalias detectadas: {df_target['if_is_anomaly'].mean()*100:.1f}%")

print("\n[5/7] Random Forest Classifier (11 features)...")
feature_cols = [
    "objeto_palavras",
    "complexidade_lexica",
    "score_tecnico",
    "valor_log",
    "uf_encoded",
    "tipo_encoded",
    "vigencia_log",
    "if_anomaly_score",
    "if_is_anomaly",
    "interacao_if_valor",
    "interacao_if_vigencia",
]

X = df_target[feature_cols].fillna(0)
y = target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=10,
    random_state=RANDOM_SEED,
    n_jobs=-1,
    class_weight="balanced",
)
rf.fit(X_train_scaled, y_train)
y_pred = rf.predict(X_test_scaled)
y_proba = rf.predict_proba(X_test_scaled)[:, 1]

acc = (y_pred == y_test).mean()
auc = roc_auc_score(y_test, y_proba)
f1 = f1_score(y_test, y_pred)
cv_scores = cross_val_score(rf, X_train_scaled, y_train, cv=5, scoring="accuracy")

print(f"  Acuracia:  {acc*100:.2f}%")
print(f"  AUC-ROC:   {auc*100:.2f}%")
print(f"  F1-Score:  {f1*100:.2f}%")
print(f"  CV 5-fold: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
print(f"\n{classification_report(y_test, y_pred)}")

feature_importance = dict(zip(feature_cols, rf.feature_importances_))
for k, v in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v*100:.2f}%")

print("\n[6/7] Computando SHAP values...")
X_background = X_train_scaled[:500]
X_explain = X_test_scaled[:300]
explainer = shap.TreeExplainer(rf, X_background)
shap_values_sample = explainer.shap_values(X_explain)
if isinstance(shap_values_sample, list):
    shap_matrix = shap_values_sample[1]
else:
    shap_matrix = shap_values_sample
print(f"  SHAP matriz: {shap_matrix.shape}")

print("\n[7/7] Salvando modelos...")
with open(SAVED_DIR / "tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open(SAVED_DIR / "isolation_forest.pkl", "wb") as f:
    pickle.dump(isolation, f)

with open(SAVED_DIR / "random_forest.pkl", "wb") as f:
    pickle.dump(rf, f)

with open(SAVED_DIR / "encoder_uf.pkl", "wb") as f:
    pickle.dump(oe_uf, f)

with open(SAVED_DIR / "encoder_tipo.pkl", "wb") as f:
    pickle.dump(oe_tipo, f)

with open(SAVED_DIR / "feature_columns.pkl", "wb") as f:
    pickle.dump(feature_cols, f)

with open(SAVED_DIR / "shap_explainer.pkl", "wb") as f:
    pickle.dump(explainer, f)

with open(SAVED_DIR / "shap_background.pkl", "wb") as f:
    pickle.dump(pd.DataFrame(X_background, columns=feature_cols), f)

with open(SAVED_DIR / "scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

n_pos = int(y.sum())
n_neg = int(len(y) - y.sum())
metricas = {
    "data_treinamento": datetime.now().isoformat(),
    "target_tipo": "observavel_ex_post",
    "registros_total": int(len(df_target)),
    "_nota_interpretativa": (
        "Métricas reportadas academicamente. Acurácia isolada é enganosa em problemas "
        f"com classes desbalanceadas ({n_pos/len(y)*100:.2f}% positivos vs. {n_neg/len(y)*100:.2f}% negativos)."
    ),
    "alerta_desbalanceamento": (
        f"Classe positiva (evento adverso) = {n_pos/len(y)*100:.2f}%. "
        "F1-Score baixo é esperado e reflete dificuldade de prever eventos raros."
    ),
    "target_distribuicao": {
        "positivos": n_pos,
        "negativos": n_neg,
        "pct_positivos": round(n_pos / len(y) * 100, 2),
        "pct_negativos": round(n_neg / len(y) * 100, 2),
    },
    "modelo_em_producao": True,
    "features": feature_cols,
    "acuracia": round(acc, 4),
    "auc_roc": round(auc, 4),
    "f1_score": round(f1, 4),
    "cv_mean": round(cv_scores.mean(), 4),
    "cv_std": round(cv_scores.std(), 4),
    "feature_importance_gini": {k: round(float(v), 4) for k, v in feature_importance.items()},
}

with open(SAVED_DIR / "metricas.json", "w", encoding="utf-8") as f:
    json.dump(metricas, f, indent=2, ensure_ascii=False)

print(f"\nModelos salvos em: {SAVED_DIR}")
print("  tfidf_vectorizer.pkl")
print("  isolation_forest.pkl")
print("  random_forest.pkl")
print("  encoder_uf.pkl")
print("  encoder_tipo.pkl")
print("  feature_columns.pkl")
print("  scaler.pkl")
print("  shap_explainer.pkl")
print("  metricas.json")
print("\nTREINAMENTO CONCLUIDO!")
