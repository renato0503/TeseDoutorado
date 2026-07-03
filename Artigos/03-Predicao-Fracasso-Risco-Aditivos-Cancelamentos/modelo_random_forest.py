import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib
matplotlib.use('Agg')

dir_base = os.path.dirname(__file__)
dir_dados = os.path.join(dir_base, "dados")
arquivo_csv = os.path.join(dir_dados, "pncp_amostra_real.csv")

if not os.path.exists(arquivo_csv):
    print("CSV real do PNCP não encontrado.")
    exit(1)

df = pd.read_csv(arquivo_csv)

# 1. Definindo o Target (Fracasso)
# Na vida real, licitações 'Anuladas' ou 'Revogadas' são os fracassos.
df['situacaoCompraNome'] = df['situacaoCompraNome'].astype(str)
df['Fracasso_Real'] = df['situacaoCompraNome'].apply(lambda x: 1 if 'Anulad' in x or 'Revogad' in x or 'Suspens' in x else 0)

# 2. Features Reais do PNCP
df['valorTotalEstimado'] = pd.to_numeric(df['valorTotalEstimado'], errors='coerce').fillna(0)
df['log_valor'] = np.log1p(df['valorTotalEstimado'])

# Dummy variables para Modalidade
df['modalidade_Dispensa'] = df['modalidadeNome'].apply(lambda x: 1 if 'Dispensa' in str(x) else 0)
df['modalidade_Pregao'] = df['modalidadeNome'].apply(lambda x: 1 if 'Pregão' in str(x) else 0)

features = ['log_valor', 'modalidade_Dispensa', 'modalidade_Pregao']
X = df[features]
y = df['Fracasso_Real']

# Random Forest
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train, y_train)

y_prob = rf.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

# 3. Gerando Curva ROC (SVG)
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 6))

plt.plot(fpr, tpr, color='#2c3e50', lw=2, label=f'Random Forest ROC (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='#e74c3c', lw=2, linestyle='--', label='Acaso (Baseline)')

plt.title('Curva ROC: Predição de Fracasso de Licitações (PNCP Real)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Taxa de Falsos Positivos', fontsize=12)
plt.ylabel('Taxa de Verdadeiros Positivos', fontsize=12)
plt.legend(loc="lower right")

plt.figtext(0.5, -0.05, 'Fonte: Dados primários extraídos via Web Scraping do PNCP (2026).', ha='center', fontsize=10, style='italic')

plt.tight_layout()
out_dir = os.path.join(dir_base, "graficos")
os.makedirs(out_dir, exist_ok=True)
plt.savefig(os.path.join(out_dir, "figura3_curva_roc.svg"), format='svg', bbox_inches='tight')
plt.close()

print("✅ Artigo 03: Random Forest processado com dados reais do PNCP.")
