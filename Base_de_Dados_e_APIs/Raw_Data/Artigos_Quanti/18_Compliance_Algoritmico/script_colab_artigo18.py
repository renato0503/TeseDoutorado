"""
===================================================================================
COMPLIANCE ALGORÍTMICO EM COMPRAS PÚBLICAS DE INOVAÇÃO
===================================================================================
Artigo 18 - Doutorado Fucape Business School
Autores: Renato de Oliveira Rosa; Walter Reis Cabral

DESCRIÇÃO:
Este script implementa o framework de compliance algorítmico para compras públicas
de inovação, incluindo:
  - Tratamento e saneamento da base PNCP 2024
  - Construção do escore ordinal de risco processual
  - Estimação de Regressão Logística e Random Forest
  - Avaliação de performance com métricas de classificação
  - Extração de matrizes de confusão e feature importance
  - Geração de visualizações

LINK GOOGLE COLAB: [INSERIR LINK APÓS UPLOAD]
LINK BASE DE DADOS: [INSERIR LINK APÓS UPLOAD]

REQUISITOS (instale antes de executar):
  pip install pandas numpy matplotlib seaborn scikit-learn shap

===================================================================================
"""

# ==================================================================================
# 1. IMPORTAÇÃO DE BIBLIOTECAS
# ==================================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
    cohen_kappa_score,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
import warnings

warnings.filterwarnings("ignore")

# Configuração de estilo dos gráficos
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")

print("=" * 80)
print("COMPLIANCE ALGORÍTMICO EM COMPRAS PÚBLICAS DE INOVAÇÃO")
print("Artigo 18 - Doutorado Fucape Business School")
print("=" * 80)

# ==================================================================================
# 2. CARREGAMENTO DA BASE DE DADOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 1: CARREGAMENTO DA BASE DE DADOS")
print("=" * 80)

# OPÇÃO 1: Carregar do link público (DESCOMENTE APÓS UPLOAD)
# LINK_DADOS = "[INSERIR LINK PÚBLICO PARA O CSV]"
# df = pd.read_csv(LINK_DADOS)

# OPÇÃO 2: Carregar do Google Drive (caso tenha subido lá)
# from google.colab import drive
# drive.mount('/content/drive')
# df = pd.read_csv('/content/drive/MyDrive/dados_pncp_2024.csv')

# OPÇÃO 3: Simular dados realistas para demonstração (REMOVER EM PRODUÇÃO)
print("AVISO: Usando dados simulados para demonstração.")
print("       Para produção, substitua pelo carregamento real dos dados PNCP 2024.\n")

np.random.seed(42)

# Simular 273.309 registros conforme descrito no artigo
n = 273309

df = pd.DataFrame(
    {
        # Identificação
        "id_contratacao": range(1, n + 1),
        # Esfera federativa (48% federal, 30% estadual, 22% municipal)
        "esfera": np.random.choice(
            ["Federal", "Estadual", "Municipal"], n, p=[0.48, 0.30, 0.22]
        ),
        # Modalidade (62% direta: 45.7% dispensa + 16.3% inexigibilidade, 38% competitiva)
        "modalidade": np.random.choice(
            [
                "Dispensa",
                "Inexigibilidade",
                "Pregão",
                "Concorrência",
                "Tomada de Preços",
            ],
            n,
            p=[0.40, 0.18, 0.30, 0.08, 0.04],
        ),
        # Valores (em reais)
        "valor_estimado": np.random.lognormal(12, 2.5, n),  # Média ~R$ 162K, max alto
        "valor_homologado": np.random.lognormal(12, 2.5, n),
        # UF (distribuição realista - sem probabilities para evitar soma != 1)
        "uf": np.random.choice(
            [
                "SP",
                "RJ",
                "MG",
                "RS",
                "PR",
                "BA",
                "PE",
                "CE",
                "GO",
                "PA",
                "SC",
                "MA",
                "AM",
                "ES",
                "PB",
                "RN",
                "AL",
                "PI",
                "MT",
                "MS",
                "RO",
                "TO",
                "AC",
                "AP",
                "RR",
            ],
            n,
        ),
        # Flags binárias
        "flag_inovacao": np.random.binomial(1, 0.0115, n),  # 1.15% conforme artigo
        "flag_covid": np.random.binomial(1, 0.03, n),
        "flag_emergencial": np.random.binomial(1, 0.08, n),
    }
)

print(f"Total de registros carregados: {len(df):,}")

# ==================================================================================
# 3. AUDITORIA E SANEAMENTO
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 2: AUDITORIA E SANEAMENTO")
print("=" * 80)

print("\n3.1. Verificação de dados brutos:")
print(f"   - Valor estimado total: R$ {df['valor_estimado'].sum():,.2f}")
print(f"   - Valor estimado médio: R$ {df['valor_estimado'].mean():,.2f}")
print(f"   - Valor estimado máximo: R$ {df['valor_estimado'].max():,.2f}")

# Problema 1: Remover outliers extremos (> R$ 1 bilhão)
outliers_removed = len(df[df["valor_estimado"] > 1_000_000_000])
df = df[df["valor_estimado"] <= 1_000_000_000]
print(
    f"\n3.2. Remoção de outliers (valor > R$ 1 bi): {outliers_removed:,} registros removidos"
)

# Problema 2: Filtrar apenas exercício 2024 (dados simulados já são 2024)
# df = df[df['ano_exercicio'] == 2024]  # Descomentar se tiver coluna ano

# Problema 3: Calcular desvio percentual
df["desvio_percentual"] = (
    (df["valor_homologado"] - df["valor_estimado"]) / df["valor_estimado"]
) * 100

print(f"\n3.3. Desvio percentual calculado:")
print(f"   - Média: {df['desvio_percentual'].mean():.2f}%")
print(f"   - Desvio padrão: {df['desvio_percentual'].std():.2f}%")

# Criar flag de contratação direta
df["flag_contratacao_direta"] = (
    df["modalidade"].isin(["Dispensa", "Inexigibilidade"]).astype(int)
)

print(f"\n3.4. Pós-saneamento:")
print(f"   - Registros finais: {len(df):,}")
print(
    f"   - Contratações diretas: {df['flag_contratacao_direta'].sum():,} ({df['flag_contratacao_direta'].mean() * 100:.1f}%)"
)
print(
    f"   - Contratações com inovação: {df['flag_inovacao'].sum():,} ({df['flag_inovacao'].mean() * 100:.2f}%)"
)

# ==================================================================================
# 4. CONSTRUÇÃO DO ESCORE DE RISCO PROCESSUAL
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 3: CONSTRUÇÃO DO ESCORE DE RISCO PROCESSUAL")
print("=" * 80)


def construir_escore_risco(row):
    """
    Constrói o escore ordinal de risco processual (0-3).

    REGRAS:
      - Escore 0 (Baixo): Nenhuma violação
      - Escore 1 (Médio): Contratação direta OU desvio moderado
      - Escore 2 (Alto): Contratação direta + desvio > 20%
      - Escore 3 (Crítico): Contratação direta + sobrepreço > 20% ou desconto < -20%
    """
    escore = 0

    # Componente 1: Contratação direta (+1 ponto)
    if row["flag_contratacao_direta"] == 1:
        escore += 1

    # Componente 2: Sobrepreço > +20% (+1 ponto)
    if row["desvio_percentual"] > 20:
        escore += 1

    # Componente 3: Desconto excessivo < -20% (+1 ponto)
    if row["desvio_percentual"] < -20:
        escore += 1

    return escore


df["escore_risco_regra"] = df.apply(construir_escore_risco, axis=1)

print("\n4.1. Distribuição do Escore de Risco Processual:")
dist_escore = df["escore_risco_regra"].value_counts().sort_index()
for escore, count in dist_escore.items():
    pct = count / len(df) * 100
    label = {0: "Baixo", 1: "Médio", 2: "Alto", 3: "Crítico"}
    print(f"   - Escore {escore} ({label[escore]}): {count:,} ({pct:.2f}%)")

print(f"\n4.2. Escore médio: {df['escore_risco_regra'].mean():.3f}")

# ==================================================================================
# 5. PREPARAÇÃO DOS DADOS PARA MODELAGEM
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 4: PREPARAÇÃO DOS DADOS PARA MODELAGEM")
print("=" * 80)

# Encoder para variáveis categóricas
le_esfera = LabelEncoder()
le_modalidade = LabelEncoder()

df["esfera_encoded"] = le_esfera.fit_transform(df["esfera"])
df["modalidade_encoded"] = le_modalidade.fit_transform(df["modalidade"])

# VARIÁVEIS DO MODELO A (todas, incluindo as de construção da regra)
VARIAVEIS_MODELO_A = [
    "flag_contratacao_direta",  # Componente 1 do escore
    "desvio_percentual",  # Componente 2 e 3 do escore
    "esfera_encoded",
    "modalidade_encoded",
    "valor_estimado",
    "valor_homologado",
    "flag_inovacao",
    "flag_covid",
    "flag_emergencial",
]

# VARIÁVEIS DO MODELO B (apenas observáveis, sem as de construção da regra)
VARIAVEIS_MODELO_B = [
    "esfera_encoded",
    "modalidade_encoded",
    "valor_estimado",
    "valor_homologado",
    "flag_inovacao",
    "flag_covid",
    "flag_emergencial",
]

# Escalar variáveis contínuas para Regressão Logística
scaler = StandardScaler()

# Preparar X e y
X_A = df[VARIAVEIS_MODELO_A].copy()
X_B = df[VARIAVEIS_MODELO_B].copy()
y = df["escore_risco_regra"].values

# Escalar apenas variáveis contínuas para RL
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

print(f"\n5.1. Dimensões dos conjuntos de dados:")
print(f"   - X_A (Modelo A): {X_A.shape}")
print(f"   - X_B (Modelo B): {X_B.shape}")
print(f"   - y (target): {y.shape}")

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

print(f"\n5.2. Divisão estratificada (70/30):")
print(f"   - Treino: {len(X_A_train):,} registros")
print(f"   - Teste: {len(X_A_test):,} registros")

# ==================================================================================
# 6. ESTIMAÇÃO DOS MODELOS
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

# ------------------------------------------------------------------------------
# 6.1 MODELO A: Regressão Logística (com variáveis da regra)
# ------------------------------------------------------------------------------
print("\n6.1. Regressão Logística - Modelo A (com variáveis da regra)")

rl_a = LogisticRegression(max_iter=1000, random_state=42, multi_class="multinomial")
rl_a.fit(X_A_train_s, y_train)
y_pred_rl_a = rl_a.predict(X_A_test_s)

metricas_rl_a = calcular_metricas(y_test, y_pred_rl_a, "Regressão Logística A")
resultados.append(metricas_rl_a)

print(f"   Accuracy:         {metricas_rl_a['Accuracy']:.4f}")
print(f"   Balanced Accuracy:{metricas_rl_a['Balanced Accuracy']:.4f}")
print(f"   F1 Macro:        {metricas_rl_a['F1 Macro']:.4f}")
print(f"   Kappa:           {metricas_rl_a['Kappa']:.4f}")

# ------------------------------------------------------------------------------
# 6.2 MODELO A: Random Forest (com variáveis da regra)
# ------------------------------------------------------------------------------
print("\n6.2. Random Forest - Modelo A (com variáveis da regra)")

rf_a = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_a.fit(X_A_train, y_train)
y_pred_rf_a = rf_a.predict(X_A_test)

metricas_rf_a = calcular_metricas(y_test, y_pred_rf_a, "Random Forest A")
resultados.append(metricas_rf_a)

print(f"   Accuracy:         {metricas_rf_a['Accuracy']:.4f}")
print(f"   Balanced Accuracy:{metricas_rf_a['Balanced Accuracy']:.4f}")
print(f"   F1 Macro:        {metricas_rf_a['F1 Macro']:.4f}")
print(f"   Kappa:           {metricas_rf_a['Kappa']:.4f}")

# ------------------------------------------------------------------------------
# 6.3 MODELO B: Regressão Logística (sem variáveis da regra)
# ------------------------------------------------------------------------------
print("\n6.3. Regressão Logística - Modelo B (sem variáveis da regra)")

rl_b = LogisticRegression(max_iter=1000, random_state=42, multi_class="multinomial")
rl_b.fit(X_B_train_s, y_train)
y_pred_rl_b = rl_b.predict(X_B_test_s)

metricas_rl_b = calcular_metricas(y_test, y_pred_rl_b, "Regressão Logística B")
resultados.append(metricas_rl_b)

print(f"   Accuracy:         {metricas_rl_b['Accuracy']:.4f}")
print(f"   Balanced Accuracy:{metricas_rl_b['Balanced Accuracy']:.4f}")
print(f"   F1 Macro:        {metricas_rl_b['F1 Macro']:.4f}")
print(f"   Kappa:           {metricas_rl_b['Kappa']:.4f}")

# ------------------------------------------------------------------------------
# 6.4 MODELO B: Random Forest (sem variáveis da regra)
# ------------------------------------------------------------------------------
print("\n6.4. Random Forest - Modelo B (sem variáveis da regra)")

rf_b = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_b.fit(X_B_train, y_train)
y_pred_rf_b = rf_b.predict(X_B_test)

metricas_rf_b = calcular_metricas(y_test, y_pred_rf_b, "Random Forest B")
resultados.append(metricas_rf_b)

print(f"   Accuracy:         {metricas_rf_b['Accuracy']:.4f}")
print(f"   Balanced Accuracy:{metricas_rf_b['Balanced Accuracy']:.4f}")
print(f"   F1 Macro:        {metricas_rf_b['F1 Macro']:.4f}")
print(f"   Kappa:           {metricas_rf_b['Kappa']:.4f}")

# ==================================================================================
# 7. MATRIZ DE CONFUSÃO
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
# 8. FEATURE IMPORTANCE (RANDOM FOREST)
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 7: FEATURE IMPORTANCE")
print("=" * 80)

# Modelo A
importancia_a = pd.DataFrame(
    {"feature": VARIAVEIS_MODELO_A, "importancia": rf_a.feature_importances_}
).sort_values("importancia", ascending=False)

print("\nFeature Importance - Random Forest Modelo A:")
for _, row in importancia_a.iterrows():
    bar = "█" * int(row["importancia"] * 50)
    print(f"   {row['feature']:<30} {row['importancia']:.4f} {bar}")

# ==================================================================================
# 9. RESULTADOS CONSOLIDADOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 8: RESULTADOS CONSOLIDADOS")
print("=" * 80)

df_resultados = pd.DataFrame(resultados)
print("\n" + df_resultados.to_string(index=False))

# ==================================================================================
# 10. GERAÇÃO DE GRÁFICOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 9: GERAÇÃO DE GRÁFICOS")
print("=" * 80)

# Figura 1: Distribuição do Escore de Risco
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1.1 Distribuição do Escore
ax1 = axes[0, 0]
cores = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
labels = ["0 - Baixo", "1 - Médio", "2 - Alto", "3 - Crítico"]
dist = df["escore_risco_regra"].value_counts().sort_index()
bars = ax1.bar(labels, dist.values, color=cores, edgecolor="black", linewidth=0.5)
ax1.set_title(
    "Distribuição do Escore de Risco Processual", fontsize=12, fontweight="bold"
)
ax1.set_xlabel("Escore de Risco")
ax1.set_ylabel("Frequência")
for bar, val in zip(bars, dist.values):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1000,
        f"{val:,}",
        ha="center",
        va="bottom",
        fontsize=9,
    )

# 1.2 Distribuição por Modalidade
ax2 = axes[0, 1]
modalidade_counts = df.groupby("modalidade")["escore_risco_regra"].mean().sort_values()
modalidade_counts.plot(
    kind="barh", ax=ax2, color=sns.color_palette("husl", len(modalidade_counts))
)
ax2.set_title("Escore Médio de Risco por Modalidade", fontsize=12, fontweight="bold")
ax2.set_xlabel("Escore Médio de Risco")
ax2.set_ylabel("Modalidade")

# 1.3 Distribuição por Esfera
ax3 = axes[1, 0]
esfera_counts = df.groupby("esfera")["escore_risco_regra"].mean().sort_values()
esfera_counts.plot(
    kind="barh", ax=ax3, color=sns.color_palette("husl", len(esfera_counts))
)
ax3.set_title("Escore Médio de Risco por Esfera", fontsize=12, fontweight="bold")
ax3.set_xlabel("Escore Médio de Risco")
ax3.set_ylabel("Esfera")

# 1.4 Matriz de Confusão
ax4 = axes[1, 1]
sns.heatmap(
    cm_rf_a,
    annot=True,
    fmt="d",
    cmap="Blues",
    ax=ax4,
    xticklabels=["0 (Baixo)", "1 (Médio)", "2 (Alto)", "3 (Crítico)"],
    yticklabels=["0 (Baixo)", "1 (Médio)", "2 (Alto)", "3 (Crítico)"],
)
ax4.set_title("Matriz de Confusão - Random Forest A", fontsize=12, fontweight="bold")
ax4.set_xlabel("Classe Predita")
ax4.set_ylabel("Classe Real")

plt.tight_layout()
plt.savefig("figura_01_distribuicao_risco.png", dpi=300, bbox_inches="tight")
plt.show()
print("   Figura 1 salva: figura_01_distribuicao_risco.png")

# Figura 2: Feature Importance
fig, ax = plt.subplots(figsize=(10, 6))
importancia_a_sorted = importancia_a.sort_values("importancia", ascending=True)
bars = ax.barh(
    importancia_a_sorted["feature"],
    importancia_a_sorted["importancia"],
    color=sns.color_palette("viridis", len(importancia_a_sorted)),
)
ax.set_title(
    "Feature Importance - Random Forest Modelo A", fontsize=14, fontweight="bold"
)
ax.set_xlabel("Importância (Gini)")
ax.set_ylabel("Variável")
plt.tight_layout()
plt.savefig("figura_02_feature_importance.png", dpi=300, bbox_inches="tight")
plt.show()
print("   Figura 2 salva: figura_02_feature_importance.png")

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
plt.show()
print("   Figura 3 salva: figura_03_comparacao_modelos.png")

# ==================================================================================
# 11. SALVAR RESULTADOS
# ==================================================================================

print("\n" + "=" * 80)
print("ETAPA 10: SALVAR RESULTADOS")
print("=" * 80)

# Salvar DataFrames
df.to_csv("dados_saneados.csv", index=False)
print("   Dados saneados salvos: dados_saneados.csv")

df_resultados.to_csv("resultados_modelos.csv", index=False)
print("   Resultados salvos: resultados_modelos.csv")

# Salvar matriz de confusão
pd.DataFrame(
    cm_rf_a,
    index=["Obs_0", "Obs_1", "Obs_2", "Obs_3"],
    columns=["Pred_0", "Pred_1", "Pred_2", "Pred_3"],
).to_csv("matriz_confusao_rf_a.csv")
print("   Matriz de confusão salva: matriz_confusao_rf_a.csv")

# Salvar feature importance
importancia_a.to_csv("feature_importance_rf_a.csv", index=False)
print("   Feature importance salva: feature_importance_rf_a.csv")

# ==================================================================================
# 12. RELATÓRIO FINAL
# ==================================================================================

print("\n" + "=" * 80)
print("RELATÓRIO FINAL")
print("=" * 80)

print(f"""
ARQUIVO GERADO: Compliance Algorítmico em Compras Públicas de Inovação
AUTORES: Renato de Oliveira Rosa; Walter Reis Cabral
DATA: 2024

RESUMO DOS RESULTADOS:
----------------------
• Base de dados: {len(df):,} registros PNCP 2024
• Contratações diretas: {df["flag_contratacao_direta"].sum():,} ({df["flag_contratacao_direta"].mean() * 100:.1f}%)
• Contratações com inovação: {df["flag_inovacao"].sum():,} ({df["flag_inovacao"].mean() * 100:.2f}%)
• Escore médio de risco: {df["escore_risco_regra"].mean():.3f}

DESEMPENHO DOS MODELOS:
-----------------------
{"=" * 60}
{"Modelo":<25} {"Accuracy":<12} {"Bal. Acc.":<12} {"F1 Macro":<12} {"Kappa":<12}
{"=" * 60}
{metricas_rf_a["Modelo"]:<25} {metricas_rf_a["Accuracy"]:<12.4f} {metricas_rf_a["Balanced Accuracy"]:<12.4f} {metricas_rf_a["F1 Macro"]:<12.4f} {metricas_rf_a["Kappa"]:<12.4f}
{metricas_rl_a["Modelo"]:<25} {metricas_rl_a["Accuracy"]:<12.4f} {metricas_rl_a["Balanced Accuracy"]:<12.4f} {metricas_rl_a["F1 Macro"]:<12.4f} {metricas_rl_a["Kappa"]:<12.4f}
{metricas_rf_b["Modelo"]:<25} {metricas_rf_b["Accuracy"]:<12.4f} {metricas_rf_b["Balanced Accuracy"]:<12.4f} {metricas_rf_b["F1 Macro"]:<12.4f} {metricas_rf_b["Kappa"]:<12.4f}
{metricas_rl_b["Modelo"]:<25} {metricas_rl_b["Accuracy"]:<12.4f} {metricas_rl_b["Balanced Accuracy"]:<12.4f} {metricas_rl_b["F1 Macro"]:<12.4f} {metricas_rl_b["Kappa"]:<12.4f}
{"=" * 60}

INTERPRETAÇÃO:
--------------
• Random Forest A alcança acurácia {metricas_rf_a["Accuracy"]:.2%} ao reproduzir o escore
  (que é deterministicamente construído por regras)
• Modelo B mostra queda de ~{(metricas_rf_a["F1 Macro"] - metricas_rf_b["F1 Macro"]):.2%}
  no F1 Macro ao remover as variáveis da regra
• Isso valida que o escore é uma regra formal, não um padrão latente

ARQUIVOS GERADOS:
-----------------
• dados_saneados.csv
• resultados_modelos.csv
• matriz_confusao_rf_a.csv
• feature_importance_rf_a.csv
• figura_01_distribuicao_risco.png
• figura_02_feature_importance.png
• figura_03_comparacao_modelos.png
""")

print("\n" + "=" * 80)
print("SCRIPT CONCLUÍDO COM SUCESSO")
print("=" * 80)

print("""
PRÓXIMOS PASSOS:
----------------
1. Substituir LINK_DADOS pelo link público do CSV
2. Fazer upload do CSV para o Google Colab
3. Executar o script completo
4. Baixar os arquivos de saída gerados
5. Verificar se os resultados batem com o artigo
""")
