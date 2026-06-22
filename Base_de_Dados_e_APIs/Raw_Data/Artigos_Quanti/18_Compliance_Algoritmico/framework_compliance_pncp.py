"""
===================================================================================
FRAMEWORK DE COMPLIANCE ALGORÍTMICO PARA COMPRAS PÚBLICAS DE INOVAÇÃO
===================================================================================

Artigo 18 - Doutorado em Ciências Contábeis e Administração
Fucape Business School

Este script implementa a análise quantitativa apresentada no artigo,
incluindo o tratamento da base de dados, construção do escore de risco
e comparação entre modelos preditivos.

REQUISITOS:
    pandas, numpy, matplotlib, seaborn, scikit-learn

===================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    confusion_matrix,
    cohen_kappa_score,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings

warnings.filterwarnings("ignore")
plt.style.use("seaborn-v0_8-whitegrid")

# ==================================================================================
# 1. CARREGAMENTO E TRATAMENTO DA BASE DE DADOS
# ==================================================================================

print("=" * 80)
print("ETAPA 1: CARREGAMENTO E TRATAMENTO DA BASE DE DADOS")
print("=" * 80)

df = pd.read_csv("dados_pncp_2024.csv")

print(f"Total de registros carregados: {len(df):,}")

# ==================================================================================
# 2. AUDITORIA E SANEAMENTO
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 2: AUDITORIA E SANEAMENTO")
print("=" * 80)

print("\n2.1 Verificação de dados brutos:")
print(f"    Valor estimado total: R$ {df['valor_estimado'].sum():,.2f}")
print(f"    Valor estimado médio: R$ {df['valor_estimado'].mean():,.2f}")
print(f"    Valor estimado máximo: R$ {df['valor_estimado'].max():,.2f}")

# Remoção de outliers (valores estimados > R$ 1 bilhão)
outliers_removed = len(df[df["valor_estimado"] > 1_000_000_000])
df = df[df["valor_estimado"] <= 1_000_000_000]
print(
    f"\n2.2 Remoção de outliers (valor > R$ 1 bi): {outliers_removed:,} registros removidos"
)

# Cálculo do desvio percentual
df["desvio_percentual"] = (
    (df["valor_homologado"] - df["valor_estimado"]) / df["valor_estimado"]
) * 100

print(f"\n2.3 Desvio percentual calculado:")
print(f"    Média: {df['desvio_percentual'].mean():.2f}%")
print(f"    Desvio padrão: {df['desvio_percentual'].std():.2f}%")

# Flag de contratação direta
df["flag_contratacao_direta"] = (
    df["modalidade"].isin(["Dispensa", "Inexigibilidade"]).astype(int)
)

print(f"\n2.4 Pós-saneamento:")
print(f"    Registros finais: {len(df):,}")
print(
    f"    Contratações diretas: {df['flag_contratacao_direta'].sum():,} "
    f"({df['flag_contratacao_direta'].mean() * 100:.1f}%)"
)
print(
    f"    Contratações com inovação: {df['flag_inovacao'].sum():,} "
    f"({df['flag_inovacao'].mean() * 100:.2f}%)"
)

# ==================================================================================
# 3. CONSTRUÇÃO DO ESCORE DE RISCO PROCESSUAL
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 3: CONSTRUÇÃO DO ESCORE DE RISCO PROCESSUAL")
print("=" * 80)


def construir_escore_risco(row):
    """
    Constrói o escore ordinal de risco processual (0-3).

    Regras de composição:
      - Escore 0 (Baixo): Nenhuma violação
      - Escore 1 (Médio): Contratação direta OU desvio moderado
      - Escore 2 (Alto): Contratação direta + desvio > 20%
      - Escore 3 (Crítico): Contratação direta + sobrepreço > 20% ou desconto < -20%
    """
    escore = 0

    if row["flag_contratacao_direta"] == 1:
        escore += 1

    if row["desvio_percentual"] > 20:
        escore += 1

    if row["desvio_percentual"] < -20:
        escore += 1

    return escore


df["escore_risco_regra"] = df.apply(construir_escore_risco, axis=1)

print("\n3.1 Distribuição do Escore de Risco Processual:")
dist_escore = df["escore_risco_regra"].value_counts().sort_index()

labels = {0: "Baixo", 1: "Médio", 2: "Alto", 3: "Crítico"}
for escore, count in dist_escore.items():
    pct = count / len(df) * 100
    print(f"    Escore {escore} ({labels[escore]}): {count:,} ({pct:.2f}%)")

print(f"\n3.2 Escore médio: {df['escore_risco_regra'].mean():.3f}")

# ==================================================================================
# 4. PREPARAÇÃO DOS DADOS PARA MODELAGEM
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 4: PREPARAÇÃO DOS DADOS PARA MODELAGEM")
print("=" * 80)

le_esfera = LabelEncoder()
le_modalidade = LabelEncoder()

df["esfera_encoded"] = le_esfera.fit_transform(df["esfera"])
df["modalidade_encoded"] = le_modalidade.fit_transform(df["modalidade"])

# Modelo A: todas as variáveis (incluindo as de construção da regra)
VARIAVEIS_MODELO_A = [
    "flag_contratacao_direta",
    "desvio_percentual",
    "esfera_encoded",
    "modalidade_encoded",
    "valor_estimado",
    "valor_homologado",
    "flag_inovacao",
]

# Modelo B: apenas variáveis observáveis (sem as de construção da regra)
VARIAVEIS_MODELO_B = [
    "esfera_encoded",
    "modalidade_encoded",
    "valor_estimado",
    "valor_homologado",
    "flag_inovacao",
]

scaler = StandardScaler()

X_A = df[VARIAVEIS_MODELO_A].copy()
X_B = df[VARIAVEIS_MODELO_B].copy()
y = df["escore_risco_regra"].values

X_A_scaled = X_A.copy()
X_B_scaled = X_B.copy()
X_A_scaled[["valor_estimado", "valor_homologado", "desvio_percentual"]] = (
    scaler.fit_transform(
        X_A[["valor_estimado", "valor_homologado", "desvio_percentual"]]
    )
)
X_B_scaled[["valor_estimado", "valor_homologado"]] = scaler.fit_transform(
    X_B[["valor_estimado", "valor_homologado"]]
)

print(f"\n4.1 Dimensões dos conjuntos de dados:")
print(f"    X_A (Modelo A): {X_A.shape}")
print(f"    X_B (Modelo B): {X_B.shape}")
print(f"    y (target): {y.shape}")

# Divisão treino/teste (70/30 estratificada)
X_A_train, X_A_test, y_train, y_test = train_test_split(
    X_A, y, test_size=0.30, random_state=42, stratify=y
)
X_A_train_s, X_A_test_s, _, _ = train_test_split(
    X_A_scaled, y, test_size=0.30, random_state=42, stratify=y
)
X_B_train, X_B_test, _, _ = train_test_split(
    X_B, y, test_size=0.30, random_state=42, stratify=y
)
X_B_train_s, X_B_test_s, _, _ = train_test_split(
    X_B_scaled, y, test_size=0.30, random_state=42, stratify=y
)

print(f"\n4.2 Divisão estratificada (70/30):")
print(f"    Treino: {len(X_A_train):,} registros")
print(f"    Teste: {len(X_A_test):,} registros")

# ==================================================================================
# 5. ESTIMAÇÃO DOS MODELOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 5: ESTIMAÇÃO DOS MODELOS")
print("=" * 80)


def calcular_metricas(y_true, y_pred, nome_modelo):
    """Calcula métricas de classificação."""
    return {
        "Modelo": nome_modelo,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Balanced Accuracy": balanced_accuracy_score(y_true, y_pred),
        "F1 Macro": f1_score(y_true, y_pred, average="macro"),
        "Kappa": cohen_kappa_score(y_true, y_pred),
    }


resultados = []

# Regressão Logística - Modelo A
print("\n5.1 Regressão Logística - Modelo A")
rl_a = LogisticRegression(max_iter=1000, random_state=42)
rl_a.fit(X_A_train_s, y_train)
y_pred_rl_a = rl_a.predict(X_A_test_s)
metricas_rl_a = calcular_metricas(y_test, y_pred_rl_a, "Regressão Logística A")
resultados.append(metricas_rl_a)
print(f"    Accuracy: {metricas_rl_a['Accuracy']:.4f}")
print(f"    F1 Macro: {metricas_rl_a['F1 Macro']:.4f}")

# Random Forest - Modelo A
print("\n5.2 Random Forest - Modelo A")
rf_a = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_a.fit(X_A_train, y_train)
y_pred_rf_a = rf_a.predict(X_A_test)
metricas_rf_a = calcular_metricas(y_test, y_pred_rf_a, "Random Forest A")
resultados.append(metricas_rf_a)
print(f"    Accuracy: {metricas_rf_a['Accuracy']:.4f}")
print(f"    F1 Macro: {metricas_rf_a['F1 Macro']:.4f}")

# Regressão Logística - Modelo B
print("\n5.3 Regressão Logística - Modelo B")
rl_b = LogisticRegression(max_iter=1000, random_state=42)
rl_b.fit(X_B_train_s, y_train)
y_pred_rl_b = rl_b.predict(X_B_test_s)
metricas_rl_b = calcular_metricas(y_test, y_pred_rl_b, "Regressão Logística B")
resultados.append(metricas_rl_b)
print(f"    Accuracy: {metricas_rl_b['Accuracy']:.4f}")
print(f"    F1 Macro: {metricas_rl_b['F1 Macro']:.4f}")

# Random Forest - Modelo B
print("\n5.4 Random Forest - Modelo B")
rf_b = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_b.fit(X_B_train, y_train)
y_pred_rf_b = rf_b.predict(X_B_test)
metricas_rf_b = calcular_metricas(y_test, y_pred_rf_b, "Random Forest B")
resultados.append(metricas_rf_b)
print(f"    Accuracy: {metricas_rf_b['Accuracy']:.4f}")
print(f"    F1 Macro: {metricas_rf_b['F1 Macro']:.4f}")

# ==================================================================================
# 6. MATRIZ DE CONFUSÃO
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 6: MATRIZ DE CONFUSÃO")
print("=" * 80)

cm_rf_a = confusion_matrix(y_test, y_pred_rf_a)

print("\nMatriz de Confusão - Random Forest Modelo A:")
print("              Predito")
print("          0      1      2      3")
print(
    f"Obs 0  {cm_rf_a[0, 0]:6,} {cm_rf_a[0, 1]:6,} {cm_rf_a[0, 2]:6,} {cm_rf_a[0, 3]:6,}"
)
print(
    f"Obs 1  {cm_rf_a[1, 0]:6,} {cm_rf_a[1, 1]:6,} {cm_rf_a[1, 2]:6,} {cm_rf_a[1, 3]:6,}"
)
print(
    f"Obs 2  {cm_rf_a[2, 0]:6,} {cm_rf_a[2, 1]:6,} {cm_rf_a[2, 2]:6,} {cm_rf_a[2, 3]:6,}"
)
print(
    f"Obs 3  {cm_rf_a[3, 0]:6,} {cm_rf_a[3, 1]:6,} {cm_rf_a[3, 2]:6,} {cm_rf_a[3, 3]:6,}"
)

# ==================================================================================
# 7. FEATURE IMPORTANCE
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 7: FEATURE IMPORTANCE")
print("=" * 80)

importancia_a = pd.DataFrame(
    {"feature": VARIAVEIS_MODELO_A, "importancia": rf_a.feature_importances_}
).sort_values("importancia", ascending=False)

print("\nFeature Importance - Random Forest Modelo A:")
for _, row in importancia_a.iterrows():
    bar = "█" * int(row["importancia"] * 50)
    print(f"    {row['feature']:<30} {row['importancia']:.4f} {bar}")

# ==================================================================================
# 8. RESULTADOS CONSOLIDADOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 8: RESULTADOS CONSOLIDADOS")
print("=" * 80)

df_resultados = pd.DataFrame(resultados)
print("\n" + df_resultados.to_string(index=False))

# ==================================================================================
# 9. GERAÇÃO DE GRÁFICOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 9: GERAÇÃO DE GRÁFICOS")
print("=" * 80)

# Figura 1: Distribuição do Escore
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax1 = axes[0, 0]
cores = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
labels_plot = ["0 - Baixo", "1 - Médio", "2 - Alto", "3 - Crítico"]
dist = df["escore_risco_regra"].value_counts().sort_index()
bars = ax1.bar(labels_plot, dist.values, color=cores, edgecolor="black", linewidth=0.5)
ax1.set_title(
    "Distribuição do Escore de Risco Processual", fontsize=12, fontweight="bold"
)
ax1.set_xlabel("Escore de Risco")
ax1.set_ylabel("Frequência")

ax2 = axes[0, 1]
modalidade_counts = df.groupby("modalidade")["escore_risco_regra"].mean().sort_values()
modalidade_counts.plot(
    kind="barh", ax=ax2, color=sns.color_palette("husl", len(modalidade_counts))
)
ax2.set_title("Escore Médio de Risco por Modalidade", fontsize=12, fontweight="bold")
ax2.set_xlabel("Escore Médio de Risco")

ax3 = axes[1, 0]
esfera_counts = df.groupby("esfera")["escore_risco_regra"].mean().sort_values()
esfera_counts.plot(
    kind="barh", ax=ax3, color=sns.color_palette("husl", len(esfera_counts))
)
ax3.set_title("Escore Médio de Risco por Esfera", fontsize=12, fontweight="bold")
ax3.set_xlabel("Escore Médio de Risco")

ax4 = axes[1, 1]
sns.heatmap(
    cm_rf_a,
    annot=True,
    fmt="d",
    cmap="Blues",
    ax=ax4,
    xticklabels=["0", "1", "2", "3"],
    yticklabels=["0", "1", "2", "3"],
)
ax4.set_title("Matriz de Confusão - Random Forest A", fontsize=12, fontweight="bold")
ax4.set_xlabel("Classe Predita")
ax4.set_ylabel("Classe Real")

plt.tight_layout()
plt.savefig("figura_01_distribuicao_risco.png", dpi=300, bbox_inches="tight")
print("    Figura 1 salva: figura_01_distribuicao_risco.png")

# Figura 2: Feature Importance
fig, ax = plt.subplots(figsize=(10, 6))
importancia_sorted = importancia_a.sort_values("importancia", ascending=True)
ax.barh(
    importancia_sorted["feature"],
    importancia_sorted["importancia"],
    color=sns.color_palette("viridis", len(importancia_sorted)),
)
ax.set_title(
    "Feature Importance - Random Forest Modelo A", fontsize=14, fontweight="bold"
)
ax.set_xlabel("Importância (Gini)")
plt.tight_layout()
plt.savefig("figura_02_feature_importance.png", dpi=300, bbox_inches="tight")
print("    Figura 2 salva: figura_02_feature_importance.png")

# Figura 3: Comparação de Desempenho
fig, ax = plt.subplots(figsize=(10, 6))
df_plot = df_resultados.melt(id_vars="Modelo", var_name="Métrica", value_name="Valor")
sns.barplot(data=df_plot, x="Métrica", y="Valor", hue="Modelo", ax=ax)
ax.set_title("Comparação de Desempenho dos Modelos", fontsize=14, fontweight="bold")
ax.set_ylabel("Valor")
ax.set_ylim(0, 1.1)
plt.legend(title="Modelo", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("figura_03_comparacao_modelos.png", dpi=300, bbox_inches="tight")
print("    Figura 3 salva: figura_03_comparacao_modelos.png")

# ==================================================================================
# 10. SALVAR RESULTADOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 10: SALVAR RESULTADOS")
print("=" * 80)

df.to_csv("dados_saneados.csv", index=False)
print("    Dados saneados salvos: dados_saneados.csv")

df_resultados.to_csv("resultados_modelos.csv", index=False)
print("    Resultados salvos: resultados_modelos.csv")

pd.DataFrame(
    cm_rf_a,
    index=["Obs_0", "Obs_1", "Obs_2", "Obs_3"],
    columns=["Pred_0", "Pred_1", "Pred_2", "Pred_3"],
).to_csv("matriz_confusao_rf_a.csv")
print("    Matriz de confusão salva: matriz_confusao_rf_a.csv")

importancia_a.to_csv("feature_importance_rf_a.csv", index=False)
print("    Feature importance salva: feature_importance_rf_a.csv")

# ==================================================================================
# FIM
# ==================================================================================

print("\n" + "=" * 80)
print("ANÁLISE CONCLUÍDA")
print("=" * 80)
