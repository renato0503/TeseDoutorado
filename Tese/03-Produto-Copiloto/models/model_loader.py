import pickle
from pathlib import Path

SAVED_DIR = Path(__file__).resolve().parent / "saved"

_cache = {}


def _carregar_pickle(nome):
    if nome not in _cache:
        path = SAVED_DIR / nome
        if path.exists():
            with open(path, "rb") as f:
                _cache[nome] = pickle.load(f)
        else:
            _cache[nome] = None
    return _cache[nome]


def get_vectorizer():
    return _carregar_pickle("tfidf_vectorizer.pkl")


def get_isolation_forest():
    return _carregar_pickle("isolation_forest.pkl")


def get_random_forest():
    return _carregar_pickle("random_forest.pkl")


def get_label_encoder_uf():
    return _carregar_pickle("label_encoder_uf.pkl")


def get_label_encoder_tipo():
    return _carregar_pickle("label_encoder_tipo.pkl")


def get_feature_columns():
    return _carregar_pickle("feature_columns.pkl")


def get_shap_explainer():
    return _carregar_pickle("shap_explainer.pkl")


def get_shap_background():
    return _carregar_pickle("shap_background.pkl")


def get_shap_values_sample():
    return _carregar_pickle("shap_values_sample.pkl")


def get_metricas():
    import json
    path = SAVED_DIR / "metricas.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def modelos_disponiveis():
    return {
        "tfidf_vectorizer": (SAVED_DIR / "tfidf_vectorizer.pkl").exists(),
        "isolation_forest": (SAVED_DIR / "isolation_forest.pkl").exists(),
        "random_forest": (SAVED_DIR / "random_forest.pkl").exists(),
        "shap_explainer": (SAVED_DIR / "shap_explainer.pkl").exists(),
        "metricas": (SAVED_DIR / "metricas.json").exists(),
    }


def limpar_cache():
    _cache.clear()
