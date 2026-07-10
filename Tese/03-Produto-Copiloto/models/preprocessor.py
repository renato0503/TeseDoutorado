import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

PADROES_CLAUSULAS = {
    "objeto": r"(objeto|contrata[çc].o|servi.o|produto|solu[çc].o)",
    "fundamentacao": r"(fundamenta[çc].o|legal|lei\s*(14\.?133|8\.?666|10\.?520))",
    "criterio": r"(crit.rio|menor pre.o|melhor t.cnica|julgamento)",
    "vigencia": r"(vig.ncia|prazo|meses|anos)",
    "pagamento": r"(pagamento|remunera[çc].o|fatura|nota fiscal)",
    "habilitacao": r"(habilita[çc].o|certid.es|regularidade|qualifica[çc].o)",
    "sancoes": r"(multa|penalidade|san[çc].o|advert.ncia|inidoneidade)",
    "garantia": r"(garantia|fian.a|seguro|cau[çc].o)",
    "dotacao": r"(dota[çc].o|or.ament.ria|recurso|cr.dito)",
    "recebimento": r"(recebimento|ateste|aceite|provis.rio|definitivo)",
    "propriedade_intelectual": r"(propriedade intelectual|direitos autorais|software|patente|c.digo.fonte)",
    "confidencialidade": r"(sigilo|confidencial|lgpd|dados pessoais|seguran.a)",
    "sla": r"(n.vel de servi.o|sla|acordo de n.vel|disponibilidade|uptime|kpi)",
    "rescisao": r"(rescis.o|distrato|encerramento|inexecu[çc].o)",
    "sustentabilidade": r"(sustentabilidade|ambiental|reciclagem|esg|log.stica reversa)",
    "inovacao": r"(inova[çc].o|p&d|pesquisa e desenvolvimento|startup|govtech)",
}

REGEX_LACUNAS = {
    "garantia": {"item": "Clausula de Garantia", "prioridade": "alta",
                 "desc": "Ausencia de garantia contratual gera riscos para a Administracao"},
    "responsabilidade": {"item": "Responsabilidades", "prioridade": "alta",
                          "desc": "Falta delimitacao de responsabilidades entre as partes"},
    "propriedade_intelectual": {"item": "Propriedade Intelectual", "prioridade": "media",
                                 "desc": "Questoes de IP/software nao estao regulamentadas"},
    "confidencialidade": {"item": "Confidencialidade/LGPD", "prioridade": "alta",
                           "desc": "Ausencia de clausula de sigilo expoe dados sensiveis"},
    "sla": {"item": "Niveis de Servico (SLA)", "prioridade": "media",
            "desc": "Indicadores de desempenho nao estao especificados"},
    "rescisao": {"item": "Rescisao Contratual", "prioridade": "alta",
                 "desc": "Condicoes de rescisao nao detalhadas"},
    "inovacao": {"item": "Inovacao/Marco Startups", "prioridade": "media",
                  "desc": "Articulacao com Marco Legal das Startups nao identificada"},
    "sustentabilidade": {"item": "Sustentabilidade", "prioridade": "baixa",
                          "desc": "Criterios de sustentabilidade nao incorporados"},
}


def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def extrair_clausulas(texto):
    texto = limpar_texto(texto)
    encontradas = []
    for nome, padrao in PADROES_CLAUSULAS.items():
        if re.search(padrao, texto):
            encontradas.append(nome)
    return encontradas


def detectar_lacunas(texto):
    texto = limpar_texto(texto)
    lacunas = []
    for chave, info in REGEX_LACUNAS.items():
        if chave not in PADROES_CLAUSULAS:
            continue
        if not re.search(PADROES_CLAUSULAS[chave], texto):
            lacunas.append(info)
    return lacunas


def calcular_score(clausulas_encontradas, lacunas):
    pesos_clausulas = {
        "objeto": 12, "fundamentacao": 10, "criterio": 8,
        "vigencia": 8, "pagamento": 8, "habilitacao": 8,
        "sancoes": 10, "garantia": 8, "dotacao": 6,
        "recebimento": 6, "propriedade_intelectual": 4,
        "confidencialidade": 4, "sla": 4, "rescisao": 2,
        "sustentabilidade": 1, "inovacao": 1,
    }
    score_base = sum(pesos_clausulas.get(c, 0) for c in clausulas_encontradas)
    deducao = sum(
        15 if l["prioridade"] == "alta" else (8 if l["prioridade"] == "media" else 3)
        for l in lacunas
    )
    return max(0, min(100, score_base - deducao))


def gerar_tfidf(corpus_textos):
    if not corpus_textos:
        return np.array([]), None
    vectorizer = TfidfVectorizer(max_features=500, stop_words=None, ngram_range=(1, 2))
    matriz = vectorizer.fit_transform(corpus_textos)
    return matriz.toarray(), vectorizer
