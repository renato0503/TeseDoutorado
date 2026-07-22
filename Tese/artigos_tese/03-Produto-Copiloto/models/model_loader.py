"""
Carregador de modelos com lazy loading e cache singleton.

Este modulo gerencia o carregamento dos modelos treinados (.pkl) do diretorio
models/saved/, utilizando cache em memoria para evitar recarregamentos.
Os modelos sao carregados sob demanda (lazy loading) na primeira chamada.

Modelos gerenciados:
    - TF-IDF Vectorizer (500 features)
    - Isolation Forest (deteccao de anomalias)
    - Random Forest Classifier (predicao de risco, 100 arvores)
    - SHAP TreeExplainer (explicabilidade)
    - Label Encoders (UF e tipo de contrato)
    - Metricas de treinamento (JSON)

Uso:
    from models.model_loader import get_random_forest, get_metricas
    rf = get_random_forest()
    metricas = get_metricas()
"""

import pickle
from pathlib import Path

SAVED_DIR = Path(__file__).resolve().parent / "saved"

_cache = {}


def _carregar_pickle(nome):
    """Carrega um arquivo pickle do diretorio saved/ com cache.

    Args:
        nome: Nome do arquivo pickle (ex: 'random_forest.pkl').

    Returns:
        Objeto Python desserializado, ou None se o arquivo nao existir.
    """
    if nome not in _cache:
        path = SAVED_DIR / nome
        if path.exists():
            with open(path, "rb") as f:
                _cache[nome] = pickle.load(f)
        else:
            _cache[nome] = None
    return _cache[nome]


def get_vectorizer():
    """Retorna o TfidfVectorizer treinado (500 features, 15.000 objetos PNCP)."""
    return _carregar_pickle("tfidf_vectorizer.pkl")


def get_isolation_forest():
    """Retorna o IsolationForest treinado (100 arvores, contamination=0.1)."""
    return _carregar_pickle("isolation_forest.pkl")


def get_random_forest():
    """Retorna o RandomForestClassifier treinado (100 arvores, 11 features, 100k contratos).

    Metricas: acuracia 93.36%, AUC-ROC 90.83%, F1 26.39%.
    """
    return _carregar_pickle("random_forest.pkl")


def get_label_encoder_uf():
    """Retorna o LabelEncoder para UF do fornecedor/orgao."""
    return _carregar_pickle("label_encoder_uf.pkl")


def get_label_encoder_tipo():
    """Retorna o LabelEncoder para tipo de contrato."""
    return _carregar_pickle("label_encoder_tipo.pkl")


def get_feature_columns():
    """Retorna a lista de nomes das 11 features usadas no Random Forest (Modelo B).

    Colunas: objeto_palavras, complexidade_lexica, score_tecnico, valor_log,
             uf_encoded, tipo_encoded, vigencia_log, if_anomaly_score,
             if_is_anomaly, interacao_if_valor, interacao_if_vigencia.
    """
    return _carregar_pickle("feature_columns.pkl")


def get_shap_explainer():
    """Retorna o SHAP TreeExplainer treinado sobre o Random Forest."""
    return _carregar_pickle("shap_explainer.pkl")


def get_shap_background():
    """Retorna o dataset de background usado para calcular SHAP values."""
    return _carregar_pickle("shap_background.pkl")


def get_shap_values_sample():
    """Retorna matriz SHAP de exemplo (300 amostras x 7 features)."""
    return _carregar_pickle("shap_values_sample.pkl")


def get_metricas():
    """Retorna metricas de treinamento como dicionario.

    Inclui: acuracia, auc_roc, cv_mean, cv_std, feature_importance,
            data_treinamento, parametros dos modelos.
    """
    import json
    path = SAVED_DIR / "metricas.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_scaler():
    """Retorna o StandardScaler usado para normalizar features (Sprint 2)."""
    return _carregar_pickle("scaler.pkl")


def modelos_disponiveis():
    """Verifica quais modelos estao disponiveis no diretorio saved/.

    Returns:
        Dicionario com booleanos para cada modelo:
        tfidf_vectorizer, isolation_forest, random_forest,
        shap_explainer, metricas.
    """
    return {
        "tfidf_vectorizer": (SAVED_DIR / "tfidf_vectorizer.pkl").exists(),
        "isolation_forest": (SAVED_DIR / "isolation_forest.pkl").exists(),
        "random_forest": (SAVED_DIR / "random_forest.pkl").exists(),
        "shap_explainer": (SAVED_DIR / "shap_explainer.pkl").exists(),
        "metricas": (SAVED_DIR / "metricas.json").exists(),
    }


def limpar_cache():
    """Limpa o cache de modelos, forcando recarregamento na proxima chamada."""
    _cache.clear()
