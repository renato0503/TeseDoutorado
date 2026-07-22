"""
Detector de anomalias contratuais usando Isolation Forest treinado em dados do PNCP.

Este modulo fornece deteccao de anomalias contratuais baseada em:
1. Modo treinado: TF-IDF + Isolation Forest (15.000 contratos PNCP)
2. Modo fallback: heuristicas lexicas (quando os modelos nao estao disponiveis)

O Isolation Forest identifica objetos de contratos que se desviam do padrao
do PNCP, sinalizando potenciais riscos de direcionamento ou redacao atipica.

References:
    Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest.
    PNCP - Portal Nacional de Contratacoes Publicas (572.045 contratos).
"""

import numpy as np
from models.model_loader import get_vectorizer, get_isolation_forest, modelos_disponiveis

TFIDF_CACHE = None
MODELO_CACHE = None


def _carregar():
    """Carrega modelos TF-IDF e Isolation Forest com lazy caching."""
    global TFIDF_CACHE, MODELO_CACHE
    if TFIDF_CACHE is None:
        TFIDF_CACHE = get_vectorizer()
        MODELO_CACHE = get_isolation_forest()


def _extrair_objeto(texto):
    """Extrai a secao do objeto do texto completo do edital.

    Sprint 5: Corrige o domain mismatch — o TF-IDF foi treinado em objetos
    de contratos (media de 15-30 palavras), nao em textos completos de editais.
    Esta funcao isola o trecho relevante antes de passar ao vetorizador.

    Args:
        texto: Texto completo da minuta ou edital.

    Returns:
        String com o trecho do objeto (primeiras 500 palavras se nao encontrar).
    """
    import re
    texto_lower = texto.lower()
    padrao = r"(?:do\s+objeto|objeto\s*:|objeto\s*da|objeto\s*do)(.*?)(?:da\s+fundamenta|do\s+prazo|da\s+vigencia|da\s+habilita|dos\s+criterios|das\s+condicoes|$)"
    match = re.search(padrao, texto_lower, re.DOTALL)
    if match:
        objeto = match.group(1).strip()
        if len(objeto.split()) >= 3:
            return objeto[:3000]
    palavras = texto.split()
    if len(palavras) > 500:
        return " ".join(palavras[:500])
    return texto


def detectar_anomalia(texto):
    """Detecta se um texto de edital contem padroes anomalos.

    SPRINT 2.3: O score de anomalia agora alimenta o Random Forest
    como feature adicional (if_anomaly_score, if_is_anomaly).

    SPRINT 5: O texto completo e reduzido a secao do objeto antes
    da vetorizacao TF-IDF, corrigindo o domain mismatch entre
    treinamento (objetos de 15-30 palavras) e inferencia (editais completos).

    Args:
        texto: String com o texto do edital a ser analisado.

    Returns:
        Dicionario com is_anomalia, score_anomalia, score_raw, mensagem.
    """
    texto_objeto = _extrair_objeto(texto)

    _carregar()
    if TFIDF_CACHE is None or MODELO_CACHE is None:
        result = _fallback(texto_objeto)
        result["score_raw"] = result.get("score_anomalia", 0)
        return result

    try:
        vetor = TFIDF_CACHE.transform([texto_objeto]).toarray()
        pred = MODELO_CACHE.predict(vetor)[0]
        score_raw = MODELO_CACHE.score_samples(vetor)[0]
        score_norm = 1.0 / (1.0 + np.exp(-score_raw))
        score_norm = round(float(score_norm * 2 - 1), 4)

        return {
            "is_anomalia": bool(pred == -1),
            "score_anomalia": score_norm,
            "score_raw": round(float(score_raw), 4),
            "mensagem": (
                "Texto apresenta padroes atipicos em relacao a base de 15.000 objetos do PNCP. "
                "Recomenda-se revisao manual para verificar possivel direcionamento."
                if pred == -1
                else "Texto dentro dos padroes observados em objetos de contratos do PNCP."
            ),
        }
    except Exception:
        result = _fallback(texto_objeto)
        result["score_raw"] = result.get("score_anomalia", 0)
        return result


def _fallback(texto):
    """Modo fallback: heuristicas lexicas quando modelos nao estao disponiveis.

    Calcula features simples (tamanho, complexidade lexica, digitos)
    e compara com objetos padrao de contratos publicos.

    Args:
        texto: String com o texto a ser analisado.

    Returns:
        Dicionario com o mesmo formato de detectar_anomalia().
    """
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
    """Retorna o status de carregamento dos modelos de anomalia.

    Returns:
        Dicionario com:
            - tfidf_ok (bool): TF-IDF vetorizador carregado
            - isolation_ok (bool): Isolation Forest carregado
            - usando_modelo_treinado (bool): Ambos modelos disponiveis
    """
    disp = modelos_disponiveis()
    return {
        "tfidf_ok": disp.get("tfidf_vectorizer", False),
        "isolation_ok": disp.get("isolation_forest", False),
        "usando_modelo_treinado": disp.get("tfidf_vectorizer", False) and disp.get("isolation_forest", False),
    }
