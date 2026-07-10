import numpy as np
from models.model_loader import get_vectorizer, get_isolation_forest, modelos_disponiveis

TFIDF_CACHE = None
MODELO_CACHE = None


def _carregar():
    global TFIDF_CACHE, MODELO_CACHE
    if TFIDF_CACHE is None:
        TFIDF_CACHE = get_vectorizer()
        MODELO_CACHE = get_isolation_forest()


def detectar_anomalia(texto):
    _carregar()
    if TFIDF_CACHE is None or MODELO_CACHE is None:
        return _fallback(texto)

    try:
        vetor = TFIDF_CACHE.transform([texto]).toarray()
        pred = MODELO_CACHE.predict(vetor)[0]
        score = MODELO_CACHE.score_samples(vetor)[0]

        return {
            "is_anomalia": bool(pred == -1),
            "score_anomalia": round(float(score), 4),
            "mensagem": (
                "Texto apresenta padroes atipicos em relacao a base de 15.000 objetos do PNCP."
                if pred == -1
                else "Texto dentro dos padroes observados em objetos de contratos do PNCP."
            ),
        }
    except Exception:
        return _fallback(texto)


def _fallback(texto):
    palavras = texto.lower().split()
    features = [
        len(texto),
        len(palavras),
        sum(1 for p in palavras if len(p) > 10) / max(1, len(palavras)),
        sum(1 for p in palavras if p.isdigit()) / max(1, len(palavras)),
        sum(1 for p in palavras if any(c.isdigit() for c in p)) / max(1, len(palavras)),
    ]

    objetos_padrao = [
        "contratacao de servicos de tecnologia da informacao",
        "aquisicao de equipamentos de informatica",
        "servicos de manutencao preventiva e corretiva",
        "contratacao de solucao de inteligencia artificial",
        "prestacao de servicos de desenvolvimento e manutencao de sistemas",
    ]
    distancias = [abs(len(texto) - len(p)) for p in objetos_padrao]
    min_dist = min(distancias) if distancias else 0

    is_anomalia = any(f > 0.5 for f in features[2:]) or min_dist > 300

    return {
        "is_anomalia": is_anomalia,
        "score_anomalia": round(float(-min_dist / 100), 4),
        "mensagem": (
            "Texto apresenta padroes atipicos. Recomenda-se revisao manual."
            if is_anomalia
            else "Texto dentro dos padroes esperados."
        ),
    }


def status_modelo():
    disp = modelos_disponiveis()
    return {
        "tfidf_ok": disp.get("tfidf_vectorizer", False),
        "isolation_ok": disp.get("isolation_forest", False),
        "usando_modelo_treinado": disp.get("tfidf_vectorizer", False) and disp.get("isolation_forest", False),
    }
