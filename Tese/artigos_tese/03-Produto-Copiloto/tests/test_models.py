"""
Testes unitarios para os modulos do Copiloto Algoritmico.

Executar: python -m pytest tests/test_models.py -v
"""

import sys
from pathlib import Path

PRODUTO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PRODUTO_DIR))


class TestPreprocessor:
    """Testes do modulo preprocessor (NLP, regex, scoring)."""

    def test_limpar_texto(self):
        from models.preprocessor import limpar_texto
        assert limpar_texto("  OLÁ   MUNDO  ") == "olá mundo"
        assert limpar_texto("Texto\ncom\nquebras") == "texto com quebras"

    def test_extrair_clausulas(self):
        from models.preprocessor import extrair_clausulas
        texto = "OBJETO: Contratacao de software. Lei 14.133. Menor preco. 12 meses."
        clausulas = extrair_clausulas(texto)
        assert "objeto" in clausulas
        assert "fundamentacao" in clausulas
        assert "criterio" in clausulas
        assert "vigencia" in clausulas

    def test_extrair_clausulas_vazio(self):
        from models.preprocessor import extrair_clausulas
        assert extrair_clausulas("") == []

    def test_detectar_lacunas(self):
        from models.preprocessor import detectar_lacunas
        texto = "OBJETO: Compra de cadeiras."
        lacunas = detectar_lacunas(texto)
        assert len(lacunas) > 3
        prioridades = [l["prioridade"] for l in lacunas]
        assert "alta" in prioridades

    def test_calcular_score_perfeito(self):
        from models.preprocessor import calcular_score
        clausulas = ["objeto", "fundamentacao", "criterio", "vigencia",
                     "pagamento", "habilitacao", "sancoes", "garantia",
                     "recebimento", "propriedade_intelectual", "confidencialidade",
                     "sla", "rescisao"]
        lacunas = []
        score = calcular_score(clausulas, lacunas)
        assert score >= 70

    def test_calcular_score_baixo(self):
        from models.preprocessor import calcular_score
        score = calcular_score(["objeto"], [{"prioridade": "alta"}, {"prioridade": "media"}])
        assert score < 50

    def test_sugestao_reescrita(self):
        from models.preprocessor import obter_sugestao_reescrita
        sugestao = obter_sugestao_reescrita("garantia")
        assert sugestao is not None
        assert "GARANTIA" in sugestao
        assert "5%" in sugestao

    def test_sugestao_reescrita_inexistente(self):
        from models.preprocessor import obter_sugestao_reescrita
        assert obter_sugestao_reescrita("xpto_inexistente") is None


class TestXAI:
    """Testes do modulo xai_explainer."""

    def test_obter_explicacao_conhecida(self):
        from models.xai_explainer import obter_explicacao
        result = obter_explicacao("objeto")
        assert result["titulo"] == "DO OBJETO"
        assert "Williamson" in result["explicacao"]

    def test_obter_explicacao_desconhecida(self):
        from models.xai_explainer import obter_explicacao
        result = obter_explicacao("clausula_inexistente")
        assert "PNCP" in result["explicacao"]

    def test_obter_explicacao_garantia(self):
        from models.xai_explainer import obter_explicacao
        result = obter_explicacao("garantia")
        assert "hold-up" in result["explicacao"]

    def test_todas_clausulas_tem_template(self):
        from models.xai_explainer import obter_explicacao
        from models.preprocessor import PADROES_CLAUSULAS
        for nome in PADROES_CLAUSULAS:
            result = obter_explicacao(nome)
            assert result is not None
            assert "titulo" in result
            assert "explicacao" in result


class TestAnomalyDetector:
    """Testes do modulo anomaly_detector."""

    def test_fallback_funciona(self):
        from models.anomaly_detector import _fallback
        result = _fallback("contratacao de servicos de tecnologia da informacao")
        assert "is_anomalia" in result
        assert "score_anomalia" in result
        assert "mensagem" in result

    def test_status_modelo(self):
        from models.anomaly_detector import status_modelo
        status = status_modelo()
        assert "tfidf_ok" in status
        assert "isolation_ok" in status
        assert "usando_modelo_treinado" in status


class TestRiskEngine:
    """Testes do modulo risk_engine."""

    def test_analisar_basico(self):
        from models.risk_engine import analisar_risco_contratual
        texto = "OBJETO: Software. Lei 14.133. Menor preco. 12 meses. Pagamento 30 dias."
        result = analisar_risco_contratual(texto)
        assert "score" in result
        assert "classificacao" in result
        assert "clausulas_encontradas" in result
        assert "lacunas" in result
        assert "features_shap" in result
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100

    def test_gerar_recomendacoes(self):
        from models.risk_engine import gerar_recomendacoes
        lacunas = [
            {"item": "Clausula de Garantia", "prioridade": "alta", "desc": "..."},
            {"item": "Confidencialidade/LGPD", "prioridade": "alta", "desc": "..."},
        ]
        recs = gerar_recomendacoes(lacunas, ["objeto"])
        assert len(recs) >= 2

    def test_extrair_features_ml(self):
        from models.risk_engine import _extrair_features_ml
        feats = _extrair_features_ml("software tecnologia inovacao sistema")
        assert feats["objeto_palavras"] == 4
        assert feats["score_tecnico"] >= 3
        assert 0 <= feats["complexidade_lexica"] <= 1


class TestModelLoader:
    """Testes do modulo model_loader."""

    def test_metricas_carregam(self):
        from models.model_loader import get_metricas
        metricas = get_metricas()
        assert isinstance(metricas, dict)

    def test_modelos_disponiveis(self):
        from models.model_loader import modelos_disponiveis
        disp = modelos_disponiveis()
        assert "tfidf_vectorizer" in disp
        assert "random_forest" in disp
        assert "shap_explainer" in disp
        assert "metricas" in disp

    def test_limpar_cache(self):
        from models.model_loader import limpar_cache, get_metricas
        get_metricas()
        limpar_cache()
        metricas = get_metricas()
        assert isinstance(metricas, dict)
