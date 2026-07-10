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
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import shap

warnings.filterwarnings("ignore")

SAVED_DIR = Path(__file__).resolve().parent / "saved"
SAVED_DIR.mkdir(exist_ok=True)

DADOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados\processed")
COMPRAS_COMPLEXAS = DADOS_DIR / "pncp_compras_complexas.csv"
CONTRATOS_FULL = DADOS_DIR / "pncp_contratos_full.csv"

SAMPLE_SIZE = 50000
RANDOM_SEED = 42

print("=" * 60)
print("TREINAMENTO DOS MODELOS DO COPILOTO")
print("=" * 60)

print("\n[1/6] Carregando dados do PNCP...")
use_full = CONTRATOS_FULL.exists()
data_path = CONTRATOS_FULL if use_full else COMPRAS_COMPLEXAS

if use_full:
    df = pd.read_csv(data_path, nrows=SAMPLE_SIZE)
    print(f"  Fonte: {CONTRATOS_FULL.name} (amostra de {SAMPLE_SIZE})")
else:
    df = pd.read_csv(data_path)
    print(f"  Fonte: {COMPRAS_COMPLEXAS.name} ({len(df)} registros)")

df["objeto"] = df["objeto"].fillna("").astype(str)
df["valor_global"] = pd.to_numeric(df["valor_global"], errors="coerce").fillna(0)
print(f"  Registros carregados: {len(df):,}")

print("\n[2/6] Engenharia de features...")
df["objeto_len"] = df["objeto"].str.len()
df["objeto_palavras"] = df["objeto"].str.split().str.len()
df["objeto_palavras_unicas"] = df["objeto"].apply(
    lambda x: len(set(x.lower().split()))
)
df["complexidade_lexica"] = df["objeto_palavras_unicas"] / df["objeto_palavras"].clip(lower=1)

KW_TECNICAS = [
    "tecnologia", "software", "sistema", "inovacao", "inovação", "p&d",
    "inteligência artificial", "inteligencia artificial", "startup",
    "sustentável", "sustentavel", "esg", "eficiência energética",
    "eficiencia energetica", "logística reversa", "logistica reversa",
]
df["score_tecnico"] = df["objeto"].str.lower().apply(
    lambda x: sum(1 for kw in KW_TECNICAS if kw in x)
)
df["valor_log"] = np.log1p(df["valor_global"])

le_uf = LabelEncoder()
df["uf_encoded"] = le_uf.fit_transform(df["uf"].fillna("ND"))
le_tipo = LabelEncoder()
df["tipo_encoded"] = le_tipo.fit_transform(df["tipo_contrato"].fillna("ND"))

# Target: risk proxy (outlier value + high complexity + contract type)
valor_zscore = np.abs(
    (df["valor_log"] - df["valor_log"].mean()) / df["valor_log"].std()
)
df["risk_score"] = (
    0.4 * valor_zscore.clip(0, 3) / 3
    + 0.3 * (df["score_tecnico"] / max(1, df["score_tecnico"].max()))
    + 0.3 * (df["complexidade_lexica"].clip(0, 1))
)
df["target_risco"] = (df["risk_score"] > df["risk_score"].median()).astype(int)

print(f"  Features criadas: objeto_len, objeto_palavras, complexidade_lexica, score_tecnico")
print(f"  Target 'target_risco': {df['target_risco'].mean()*100:.1f}% positivos")

print("\n[3/6] TF-IDF + Isolation Forest...")
vectorizer = TfidfVectorizer(
    max_features=500,
    stop_words=None,
    ngram_range=(1, 2),
    min_df=2,
)
objetos_sample = df["objeto"].sample(min(15000, len(df)), random_state=RANDOM_SEED)
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

print("\n[4/6] Random Forest Classifier...")
feature_cols = [
    "objeto_len",
    "objeto_palavras",
    "complexidade_lexica",
    "score_tecnico",
    "valor_log",
    "uf_encoded",
    "tipo_encoded",
]
X = df[feature_cols].fillna(0)
y = df["target_risco"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
)

rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=10,
    random_state=RANDOM_SEED,
    n_jobs=-1,
    class_weight="balanced",
)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

acc = (y_pred == y_test).mean()
auc = roc_auc_score(y_test, y_proba)
cv_scores = cross_val_score(rf, X_train, y_train, cv=5, scoring="accuracy")

print(f"  Acuracia: {acc*100:.2f}%")
print(f"  AUC-ROC:  {auc*100:.2f}%")
print(f"  CV 5-fold: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
print(f"\n{classification_report(y_test, y_pred)}")

feature_importance = dict(zip(feature_cols, rf.feature_importances_))
for k, v in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v*100:.2f}%")

print("\n[5/6] Computando SHAP values...")
X_background = X_train.sample(min(500, len(X_train)), random_state=RANDOM_SEED)
X_explain = X_test.sample(min(300, len(X_test)), random_state=RANDOM_SEED)
explainer = shap.TreeExplainer(rf, X_background)
shap_values_sample = explainer.shap_values(X_explain)
if isinstance(shap_values_sample, list):
    shap_matrix = shap_values_sample[1]
else:
    shap_matrix = shap_values_sample
print(f"  SHAP matriz: {shap_matrix.shape}")

print("\n[6/6] Salvando modelos...")

with open(SAVED_DIR / "tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open(SAVED_DIR / "isolation_forest.pkl", "wb") as f:
    pickle.dump(isolation, f)

with open(SAVED_DIR / "random_forest.pkl", "wb") as f:
    pickle.dump(rf, f)

with open(SAVED_DIR / "label_encoder_uf.pkl", "wb") as f:
    pickle.dump(le_uf, f)

with open(SAVED_DIR / "label_encoder_tipo.pkl", "wb") as f:
    pickle.dump(le_tipo, f)

with open(SAVED_DIR / "feature_columns.pkl", "wb") as f:
    pickle.dump(feature_cols, f)

with open(SAVED_DIR / "shap_explainer.pkl", "wb") as f:
    pickle.dump(explainer, f)

with open(SAVED_DIR / "shap_background.pkl", "wb") as f:
    pickle.dump(X_background, f)

with open(SAVED_DIR / "shap_values_sample.pkl", "wb") as f:
    pickle.dump(shap_matrix, f)

metricas = {
    "data_treinamento": datetime.now().isoformat(),
    "registros_treino": int(len(df)),
    "acuracia": round(acc, 4),
    "auc_roc": round(auc, 4),
    "cv_mean": round(cv_scores.mean(), 4),
    "cv_std": round(cv_scores.std(), 4),
    "feature_importance": {k: round(float(v), 4) for k, v in feature_importance.items()},
    "tfidf_max_features": 500,
    "isolation_contamination": 0.1,
    "random_forest_n_estimators": 150,
}
with open(SAVED_DIR / "metricas.json", "w", encoding="utf-8") as f:
    json.dump(metricas, f, indent=2, ensure_ascii=False)

print(f"\nModelos salvos em: {SAVED_DIR}")
print("  tfidf_vectorizer.pkl")
print("  isolation_forest.pkl")
print("  random_forest.pkl")
print("  label_encoder_uf.pkl")
print("  label_encoder_tipo.pkl")
print("  feature_columns.pkl")
print("  metricas.json")
print("\nTREINAMENTO CONCLUIDO!")
