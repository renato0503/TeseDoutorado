"""
Templates de explicabilidade XAI com fundamentos academicos e juridicos.

Cada template associa uma clausula contratual a uma explicacao baseada em:
- Teoria economica (Williamson, Jensen & Meckling)
- Legislacao (Lei 14.133/2021, LGPD, LC 182/2021)
- Evidencia empirica do PNCP (572.045 contratos)

References:
    Williamson, O. E. (1985). The Economic Institutions of Capitalism.
    Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm.
    Lei 14.133/2021. Nova Lei de Licitacoes e Contratos.
    Lei 13.709/2018. Lei Geral de Protecao de Dados (LGPD).
    Lei Complementar 182/2021. Marco Legal das Startups.
"""

import json as _json
from pathlib import Path

_COUNTERFACTUAL_TEMPLATES_PATH = Path(__file__).parent / "saved" / "counterfactual_templates.json"

try:
    with open(_COUNTERFACTUAL_TEMPLATES_PATH, "r", encoding="utf-8") as _f:
        _COUNTERFACTUAL_TEMPLATES = _json.load(_f)
except Exception:
    _COUNTERFACTUAL_TEMPLATES = {}

XAI_TEMPLATES = {
    "objeto": {
        "titulo": "DO OBJETO",
        "explicacao": "A descricao detalhada do objeto reduz assimetrias informacionais e impede "
                      "interpretacoes divergentes entre Administracao e fornecedores, conforme "
                      "Economia dos Custos de Transacao (Williamson, 1985).",
    },
    "fundamentacao": {
        "titulo": "DA FUNDAMENTACAO LEGAL",
        "explicacao": "A correta fundamentacao legal (Lei 14.133/2021) garante seguranca juridica "
                      "e reduz o risco de nulidade do processo licitatorio.",
    },
    "criterio": {
        "titulo": "DO CRITERIO DE JULGAMENTO",
        "explicacao": "A definicao explicita do criterio de julgamento reduz o espaco de "
                      "discricionariedade do agente publico (Teoria da Agencia).",
    },
    "vigencia": {
        "titulo": "DO PRAZO DE VIGENCIA",
        "explicacao": "Prazos superiores a 12 meses devem ser justificados tecnicamente. "
                      "Contratos longos aumentam exposicao a risco de lock-in.",
    },
    "pagamento": {
        "titulo": "DAS CONDICOES DE PAGAMENTO",
        "explicacao": "A definicao de prazos e condicoes de pagamento reduz o custo de transacao "
                      "ex-post. A latencia media de pagamento no PNCP e de 45 dias.",
    },
    "garantia": {
        "titulo": "DA GARANTIA CONTRATUAL",
        "explicacao": "A exigencia de garantia (ate 5%) protege o erario contra inadimplemento "
                      "e comportamento oportunista do contratado (hold-up).",
    },
    "sancoes": {
        "titulo": "DAS SANCOES ADMINISTRATIVAS",
        "explicacao": "Sancoes proporcionais e graduadas incentivam o cumprimento contratual e "
                      "desestimulam o comportamento oportunista ex-post.",
    },
    "confidencialidade": {
        "titulo": "DA CONFIDENCIALIDADE",
        "explicacao": "Conforme Art. 6 da LGPD, a protecao de dados pessoais e mandatoria. "
                      "O descumprimento pode gerar multas de ate 2% do faturamento.",
    },
    "sla": {
        "titulo": "DOS NIVEIS DE SERVICO (SLA)",
        "explicacao": "KPIs mensuraveis (disponibilidade, tempo de resposta) reduzem o custo "
                      "de monitoramento e alinham incentivos entre agente e principal.",
    },
    "propriedade_intelectual": {
        "titulo": "DA PROPRIEDADE INTELECTUAL",
        "explicacao": "Definir a titularidade do codigo-fonte ao termino do contrato evita "
                      "lock-in tecnologico (Martins & Gomes, 2022).",
    },
    "sustentabilidade": {
        "titulo": "DOS CRITERIOS DE SUSTENTABILIDADE",
        "explicacao": "Compras publicas sustentaveis sao diretriz da ONU (ODS 12) e estao "
                      "previstas no Art. 5 da Lei 14.133/2021.",
    },
    "inovacao": {
        "titulo": "DA INOVACAO TECNOLOGICA",
        "explicacao": "Contratacoes de inovacao devem seguir o Marco Legal das Startups "
                      "(LC 182/2021), permitindo modalidades especiais como encomenda "
                      "tecnologica e contrato publico para solucao inovadora (CPSI).",
    },
    "rescisao": {
        "titulo": "DA RESCISAO CONTRATUAL",
        "explicacao": "A previsao de hipoteses de rescisao (Art. 137, Lei 14.133/2021) "
                      "reduz custos de saida e protege a Administracao contra abandono "
                      "contratual pelo fornecedor.",
    },
    "habilitacao": {
        "titulo": "DA HABILITACAO",
        "explicacao": "Os requisitos de habilitacao (Art. 62-70, Lei 14.133/2021) garantem "
                      "que apenas fornecedores qualificados participem do certame, reduzindo "
                      "risco de selecao adversa (Akerlof, 1970).",
    },
    "recebimento": {
        "titulo": "DO RECEBIMENTO DO OBJETO",
        "explicacao": "A definicao de criterios de recebimento provisorio e definitivo (Art. 140) "
                      "reduz conflitos ex-post e estabelece marcos objetivos de aceitacao.",
    },
    "dotacao": {
        "titulo": "DA DOTACAO ORCAMENTARIA",
        "explicacao": "A indicacao da dotacao orcamentaria (Art. 150) garante que a despesa "
                      "esta previamente autorizada, evitando riscos fiscais e contingenciamento.",
    },
}


def obter_explicacao(clausula_nome):
    """Retorna o template XAI para uma clausula especifica.

    Args:
        clausula_nome: Nome da clausula (ex: 'objeto', 'garantia', 'sla').

    Returns:
        Dicionario com 'titulo' e 'explicacao'. Se a clausula nao tiver
        template especifico, retorna um template generico com referencia
        ao PNCP e a Lei 14.133/2021.
    """
    template = XAI_TEMPLATES.get(clausula_nome)
    if template:
        return template
    return {
        "titulo": clausula_nome.replace("_", " ").upper(),
        "explicacao": "Clausula identificada com base na analise de 572.045 contratos do PNCP "
                      "e na legislacao vigente (Lei 14.133/2021).",
    }


def gerar_explicacoes_clausulas(clausulas_encontradas):
    """Gera explicacoes XAI para uma lista de clausulas encontradas.

    Args:
        clausulas_encontradas: Lista de nomes de clausulas.

    Returns:
        Lista de dicionarios com 'titulo' e 'explicacao'.
    """
    explicacoes = []
    for nome in clausulas_encontradas:
        explicacoes.append(obter_explicacao(nome))
    return explicacoes


def gerar_resumo_shap(features):
    """Gera resumo textual das contribuicoes SHAP.

    Args:
        features: Lista de dicionarios com 'feature', 'peso' e 'explicacao'.

    Returns:
        Lista de strings formatadas com as top-5 features.
    """
    linhas = []
    for f in features[:5]:
        linhas.append(
            f"{f['feature']}: {f['peso'] * 100:.2f}% de impacto na predicao "
            f"de risco ({f['explicacao'][:80]}...)"
        )
    return linhas


def obter_template_counterfactual(feature_nome):
    """Retorna o template counterfactual para uma feature de modelo ML.

    Args:
        feature_nome: Nome tecnico da feature (ex: 'valor_log', 'vigencia_log').

    Returns:
        Dicionario com nome_traduzido, valor_medio, desvio_padrao e
        template_pergunta. None se a feature nao tiver template.
    """
    return _COUNTERFACTUAL_TEMPLATES.get(feature_nome)


def gerar_texto_legal_counterfactual(contrafactuais):
    """Gera caixas de texto juridico para os contrafactuais SHAP.

    Args:
        contrafactuais: Lista de dicionarios com 'feature', 'peso' e 'contrafactual'.

    Returns:
        Lista de dicionarios com 'feature', 'nome_legal', 'pergunta_legal',
        'peso' para renderizacao em UI.
    """
    resultados = []
    for cf in contrafactuais:
        feature = cf.get("feature", "")
        template = obter_template_counterfactual(feature)
        if template:
            resultados.append({
                "feature": feature,
                "nome_legal": template.get("nome_traduzido", feature),
                "pergunta_legal": template.get("template_pergunta", ""),
                "peso": cf.get("peso", 0),
            })
    return resultados
