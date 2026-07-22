"""
Script oficial de treinamento completo dos modelos do Copiloto Algorítmico.

Realiza o retreinamento sob o novo target ex-post (sem vigência curta)
e treina dois modelos finais de forma comparativa:
- Modelo A: Sem vigência (foco 100% ex-ante/estrutural)
- Modelo B: Com vigência (com vigência + termo de interação)
"""

import sys
from pathlib import Path

PRODUTO_DIR = Path(__file__).resolve().parent.parent / "Tese" / "artigos_tese" / "03-Produto-Copiloto"
sys.path.insert(0, str(PRODUTO_DIR))

import pandas as pd
import numpy as np
import pickle
import json
import warnings
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
import shap

warnings.filterwarnings("ignore")

RANDOM_SEED = 42
SAVED_DIR = PRODUTO_DIR / "models" / "saved"
SAVED_DIR.mkdir(exist_ok=True)

DADOS_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\dados\processed")
TARGET_CSV = DADOS_DIR / "pncp_target_real.csv"

print("=" * 60)
print("RETREINAMENTO FINAL — MODELOS COMPATIVEL COM DSR")
print("=" * 60)

# 1. Carregar dados
print("\n[1/8] Carregando dados do PNCP...")
if TARGET_CSV.exists():
    df = pd.read_csv(TARGET_CSV)
    print(f"  Fonte: {TARGET_CSV.name}")
else:
    print("  ERRO: pncp_target_real.csv nao encontrado.")
    sys.exit(1)

df["objeto"] = df["objeto"].fillna("").astype(str)
df["valor_global"] = pd.to_numeric(df["valor_global"], errors="coerce").fillna(0)
df["uf"] = df["uf"].fillna("ND")

# Novo target ex-post sem a vigência curta (tautologia)
df["target_real"] = ((df["aditivo_valor"] == 1) | (df["multiplas_retificacoes"] == 1)).astype(int)

print(f"  Registros carregados: {len(df):,}")
print(f"  Target ex-post positivo: {df['target_real'].sum():,} ({df['target_real'].mean()*100:.2f}%)")

# 2. Engenharia de features básicas
print("\n[2/8] Engenharia de features estruturais...")
df["objeto_palavras"] = df["objeto"].str.split().str.len()
df["objeto_palavras_unicas"] = df["objeto"].apply(lambda x: len(set(x.lower().split())))
df["complexidade_lexica"] = df["objeto_palavras_unicas"] / df["objeto_palavras"].clip(lower=1)

KW_TECNICAS = [
    "tecnologia", "software", "sistema", "inovacao", "inovação",
    "inteligencia artificial", "inteligência artificial",
    "startup", "sustentavel", "sustentável", "esg",
    "p&d", "pesquisa e desenvolvimento", "govtech",
]
df["score_tecnico"] = df["objeto"].str.lower().apply(lambda x: sum(1 for kw in KW_TECNICAS if kw in x))
df["valor_log"] = np.log1p(df["valor_global"])

le_uf = LabelEncoder()
df["uf_encoded"] = le_uf.fit_transform(df["uf"])
le_tipo = LabelEncoder()
df["tipo_encoded"] = le_tipo.fit_transform(df["tipo_contrato"].fillna("ND"))

df["vigencia_dias"] = pd.to_numeric(df["vigencia_dias"], errors="coerce").fillna(0).clip(lower=1)
df["vigencia_log"] = np.log1p(df["vigencia_dias"])

# 3. TF-IDF + Isolation Forest (NLP)
print("\n[3/8] TF-IDF + Isolation Forest (Processamento Semântico)...")
vectorizer = TfidfVectorizer(max_features=500, stop_words=None, ngram_range=(1, 2), min_df=2)
df_sample_nlp = df.sample(min(15000, len(df)), random_state=RANDOM_SEED)
vectorizer.fit(df_sample_nlp["objeto"])

tfidf_full = vectorizer.transform(df["objeto"])
isolation = IsolationForest(n_estimators=100, contamination=0.1, random_state=RANDOM_SEED, n_jobs=-1)
isolation.fit(vectorizer.transform(df_sample_nlp["objeto"]).toarray())

df["if_anomaly_score"] = isolation.score_samples(tfidf_full.toarray())
df["if_is_anomaly"] = (isolation.predict(tfidf_full.toarray()) == -1).astype(int)

# 4. Termos de interação NLP (Solução 3)
print("\n[4/8] Criando termos de interação NLP...")
df["interacao_if_valor"] = df["if_anomaly_score"] * df["valor_log"]
df["interacao_if_vigencia"] = df["if_anomaly_score"] * df["vigencia_log"]

# Definição das colunas de features para os dois modelos
FEATURE_COLS_A = [
    "objeto_palavras", "complexidade_lexica", "score_tecnico", "valor_log",
    "uf_encoded", "tipo_encoded", "if_anomaly_score", "if_is_anomaly", "interacao_if_valor"
]

FEATURE_COLS_B = [
    "objeto_palavras", "complexidade_lexica", "score_tecnico", "valor_log",
    "uf_encoded", "tipo_encoded", "vigencia_log", "if_anomaly_score", "if_is_anomaly",
    "interacao_if_valor", "interacao_if_vigencia"
]

# Split e scaling do Modelo A
scaler_A = StandardScaler()
X_A = pd.DataFrame(scaler_A.fit_transform(df[FEATURE_COLS_A]), columns=FEATURE_COLS_A)
y = df["target_real"]
XA_train, XA_test, yA_train, yA_test = train_test_split(X_A, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y)

# Split e scaling do Modelo B
scaler_B = StandardScaler()
X_B = pd.DataFrame(scaler_B.fit_transform(df[FEATURE_COLS_B]), columns=FEATURE_COLS_B)
XB_train, XB_test, yB_train, yB_test = train_test_split(X_B, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y)

# 5. Treinamento do Modelo A (Sem Vigência)
print("\n[5/8] Treinando Modelo A: Sem Vigência...")
rf_A = RandomForestClassifier(
    n_estimators=100, max_depth=20, min_samples_leaf=10,
    random_state=RANDOM_SEED, n_jobs=-1, class_weight="balanced"
)
rf_A.fit(XA_train, yA_train)
yA_pred = rf_A.predict(XA_test)
yA_proba = rf_A.predict_proba(XA_test)[:, 1]

metrics_A = {
    "acuracia": round(accuracy_score(yA_test, yA_pred), 4),
    "precisao": round(precision_score(yA_test, yA_pred, zero_division=0), 4),
    "recall": round(recall_score(yA_test, yA_pred, zero_division=0), 4),
    "f1_score": round(f1_score(yA_test, yA_pred, zero_division=0), 4),
    "auc_roc": round(roc_auc_score(yA_test, yA_proba), 4)
}
print(f"  Modelo A - Acc: {metrics_A['acuracia']*100:.2f}% | F1: {metrics_A['f1_score']*100:.2f}% | AUC: {metrics_A['auc_roc']*100:.2f}%")

# 6. Treinamento do Modelo B (Com Vigência)
print("\n[6/8] Treinando Modelo B: Com Vigência...")
rf_B = RandomForestClassifier(
    n_estimators=100, max_depth=20, min_samples_leaf=10,
    random_state=RANDOM_SEED, n_jobs=-1, class_weight="balanced"
)
rf_B.fit(XB_train, yB_train)
yB_pred = rf_B.predict(XB_test)
yB_proba = rf_B.predict_proba(XB_test)[:, 1]

metrics_B = {
    "acuracia": round(accuracy_score(yB_test, yB_pred), 4),
    "precisao": round(precision_score(yB_test, yB_pred, zero_division=0), 4),
    "recall": round(recall_score(yB_test, yB_pred, zero_division=0), 4),
    "f1_score": round(f1_score(yB_test, yB_pred, zero_division=0), 4),
    "auc_roc": round(roc_auc_score(yB_test, yB_proba), 4)
}
print(f"  Modelo B - Acc: {metrics_B['acuracia']*100:.2f}% | F1: {metrics_B['f1_score']*100:.2f}% | AUC: {metrics_B['auc_roc']*100:.2f}%")

# 7. Computar SHAP para o Modelo B (para visualização de referência)
print("\n[7/8] Computando SHAP para o Modelo B...")
X_background = XB_train.sample(min(500, len(XB_train)), random_state=RANDOM_SEED)
X_explain = XB_test.sample(min(300, len(XB_test)), random_state=RANDOM_SEED)
explainer = shap.TreeExplainer(rf_B, X_background)
shap_values_sample = explainer.shap_values(X_explain)

if isinstance(shap_values_sample, list):
    shap_matrix = shap_values_sample[1]
else:
    shap_matrix = shap_values_sample

shap_importance = {}
for i, col in enumerate(FEATURE_COLS_B):
    shap_importance[col] = round(float(np.abs(shap_matrix[:, i]).mean()), 6)
shap_total = sum(shap_importance.values())
shap_pct = {k: round(v / shap_total * 100, 2) if shap_total > 0 else 0 for k, v in shap_importance.items()}

# 8. Salvando os modelos oficiais
print("\n[8/8] Salvando modelos e pickles oficiais...")
with open(SAVED_DIR / "tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open(SAVED_DIR / "isolation_forest.pkl", "wb") as f:
    pickle.dump(isolation, f)

with open(SAVED_DIR / "random_forest.pkl", "wb") as f:
    pickle.dump(rf_B, f)

with open(SAVED_DIR / "random_forest_sem_vigencia.pkl", "wb") as f:
    pickle.dump(rf_A, f)

with open(SAVED_DIR / "label_encoder_uf.pkl", "wb") as f:
    pickle.dump(le_uf, f)

with open(SAVED_DIR / "label_encoder_tipo.pkl", "wb") as f:
    pickle.dump(le_tipo, f)

with open(SAVED_DIR / "scaler.pkl", "wb") as f:
    pickle.dump(scaler_B, f)

with open(SAVED_DIR / "scaler_sem_vigencia.pkl", "wb") as f:
    pickle.dump(scaler_A, f)

with open(SAVED_DIR / "feature_columns.pkl", "wb") as f:
    pickle.dump(FEATURE_COLS_B, f)

with open(SAVED_DIR / "feature_columns_sem_vigencia.pkl", "wb") as f:
    pickle.dump(FEATURE_COLS_A, f)

with open(SAVED_DIR / "shap_explainer.pkl", "wb") as f:
    pickle.dump(explainer, f)

with open(SAVED_DIR / "shap_background.pkl", "wb") as f:
    pickle.dump(X_background, f)

with open(SAVED_DIR / "shap_values_sample.pkl", "wb") as f:
    pickle.dump(shap_matrix, f)

# Metadados e métricas salvas em JSON
metricas = {
    "data_treinamento": datetime.now().isoformat(),
    "target_tipo": "observavel_ex_post",
    "registros_total": int(len(df)),
    "target_distribuicao": {
        "positivos": int(y.sum()),
        "negativos": int((~y.astype(bool)).sum()),
        "pct_positivos": round(y.mean() * 100, 2),
    },
    "modelo_A_sem_vigencia": {
        "features": FEATURE_COLS_A,
        "acuracia": metrics_A["acuracia"],
        "auc_roc": metrics_A["auc_roc"],
        "f1_score": metrics_A["f1_score"],
        "feature_importance_gini": {k: round(float(v), 4) for k, v in zip(FEATURE_COLS_A, rf_A.feature_importances_)}
    },
    "modelo_B_com_vigencia": {
        "features": FEATURE_COLS_B,
        "acuracia": metrics_B["acuracia"],
        "auc_roc": metrics_B["auc_roc"],
        "f1_score": metrics_B["f1_score"],
        "feature_importance_gini": {k: round(float(v), 4) for k, v in zip(FEATURE_COLS_B, rf_B.feature_importances_)},
        "feature_importance_shap": shap_pct
    }
}

with open(SAVED_DIR / "metricas.json", "w", encoding="utf-8") as f:
    json.dump(metricas, f, indent=2, ensure_ascii=False)

print("\nRetreinamento concluído e salvo com sucesso em:", SAVED_DIR)
