"""
Preprocessamento de texto e engenharia de features para o Copiloto Algoritmico.

Este modulo fornece funcoes para limpeza de texto, extracao de clausulas por regex,
deteccao de lacunas contratuais, calculo de score de conformidade e vetorizacao TF-IDF.

Os padroes de regex foram calibrados sobre 572.045 contratos do PNCP (2021-2024)
e cobrem 16 tipos de clausulas previstas na Lei 14.133/2021 e Lei Complementar 182/2021.

References:
    Williamson, O. E. (1985). The Economic Institutions of Capitalism.
    Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm.
    Lei 14.133/2021 - Nova Lei de Licitacoes.
    Lei Complementar 182/2021 - Marco Legal das Startups.
"""

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

SUGESTOES_REESCRITA = {
    "garantia": (
        "DA GARANTIA CONTRATUAL\n"
        "4.1. A contratada devera apresentar garantia de 5% (cinco por cento) do valor "
        "do contrato em ate 10 (dez) dias uteis apos a assinatura.\n"
        "4.2. A garantia podera ser prestada em: I - dinheiro; II - fianca bancaria; "
        "III - seguro-garantia.\n"
        "4.3. A garantia sera liberada apos o cumprimento integral das obrigacoes contratuais."
    ),
    "confidencialidade": (
        "DA CONFIDENCIALIDADE E PROTEcaO DE DADOS\n"
        "6.1. A contratada se compromete a manter sigilo sobre todas as informacoes "
        "obtidas em razao do contrato, nos termos do art. 6 da Lei 13.709/2018 (LGPD).\n"
        "6.2. E vedado o compartilhamento de dados pessoais com terceiros sem previa "
        "autorizacao expressa da Administracao.\n"
        "6.3. O descumprimento implicara em rescisao motivada e apuracao de responsabilidade "
        "civil e administrativa."
    ),
    "rescisao": (
        "DA RESCISAO CONTRATUAL\n"
        "10.1. O contrato podera ser rescindido nos casos previstos no art. 137 da "
        "Lei 14.133/2021.\n"
        "10.2. A rescisao unilateral pela Administracao, nos casos de inadimplemento, "
        "assegurara a imediata ocupacao e utilizacao dos bens e servicos.\n"
        "10.3. A parte que der causa a rescisao respondera por perdas e danos comprovados."
    ),
    "sla": (
        "DOS NIVEIS DE SERVICO (SLA)\n"
        "7.1. O sistema devera atender aos seguintes indicadores minimos:\n"
        "a) Disponibilidade: 99,5% (maximo de 3,65 horas de indisponibilidade por mes);\n"
        "b) Tempo de resposta: inferior a 2 (dois) segundos para operacoes criticas;\n"
        "c) Tempo de recuperacao: inferior a 4 (quatro) horas apos incidente.\n"
        "7.2. O descumprimento dos SLAs acarretara aplicacao de glosas proporcionais "
        "conforme tabela do Anexo I."
    ),
    "propriedade_intelectual": (
        "DA PROPRIEDADE INTELECTUAL\n"
        "8.1. A propriedade do codigo-fonte, algoritmos e documentacao tecnica produzidos "
        "sera da Administracao Publica.\n"
        "8.2. A contratada podera utilizar componentes de terceiros mediante licenca "
        "valida e comprovada.\n"
        "8.3. Ao termino do contrato, todo o codigo e documentacao deverao ser transferidos "
        "em repositorio oficial da Administracao."
    ),
    "responsabilidade": (
        "DAS RESPONSABILIDADES DAS PARTES\n"
        "9.1. Responsabilidades da Contratada:\n"
        "a) Executar o objeto conforme especificacoes tecnicas;\n"
        "b) Manter equipe tecnica qualificada durante toda a vigencia;\n"
        "c) Responder por danos causados a Administracao ou a terceiros.\n"
        "9.2. Responsabilidades da Administracao:\n"
        "a) Disponibilizar acesso as instalacoes e informacoes necessarias;\n"
        "b) Efetuar pagamentos nos prazos estabelecidos;\n"
        "c) Fiscalizar a execucao contratual conforme Art. 117 da Lei 14.133/2021."
    ),
}


def limpar_texto(texto):
    """Remove maiusculas e normaliza espacos em branco.

    Args:
        texto: String com o texto da minuta ou edital.

    Returns:
        Texto normalizado em lowercase com espacos colapsados.
    """
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def extrair_clausulas(texto):
    """Extrai clausulas contratuais por regex do texto da minuta.

    Aplica 16 padroes de regex (PADROES_CLAUSULAS) calibrados sobre
    contratos do PNCP e na Lei 14.133/2021.

    Args:
        texto: String com o texto completo da minuta.

    Returns:
        Lista de strings com os nomes das clausulas encontradas.
        Ex: ['objeto', 'fundamentacao', 'criterio', ...]
    """
    texto = limpar_texto(texto)
    encontradas = []
    for nome, padrao in PADROES_CLAUSULAS.items():
        if re.search(padrao, texto):
            encontradas.append(nome)
    return encontradas


def detectar_lacunas(texto):
    """Detecta lacunas contratuais (clausulas ausentes) no texto.

    Compara as clausulas encontradas contra os 16 padroes esperados
    e retorna as ausentes com nivel de prioridade (alta/media/baixa).

    Args:
        texto: String com o texto completo da minuta.

    Returns:
        Lista de dicionarios com 'item', 'prioridade' e 'desc'.
    """
    texto = limpar_texto(texto)
    lacunas = []
    for chave, info in REGEX_LACUNAS.items():
        if chave not in PADROES_CLAUSULAS:
            continue
        if not re.search(PADROES_CLAUSULAS[chave], texto):
            lacunas.append(info)
    return lacunas


def calcular_score(clausulas_encontradas, lacunas):
    """Calcula score de conformidade contratual (0-100).

    O score parte de 100 e deduz pontos conforme a ausencia de clausulas
    essenciais. Clausulas com maior peso na Lei 14.133/2021 recebem
    pontuacao maior (ex: objeto=12, fundamentacao=10).

    Args:
        clausulas_encontradas: Lista de nomes de clausulas detectadas.
        lacunas: Lista de dicionarios de lacunas detectadas.

    Returns:
        Inteiro entre 0 e 100 representando o percentual de conformidade.
    """
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
    """Gera matriz TF-IDF a partir de um corpus de textos.

    Args:
        corpus_textos: Lista de strings (ex: objetos de contratos).

    Returns:
        Tupla (matriz numpy, TfidfVectorizer) onde a matriz tem shape
        (n_documentos, max_features) e o vectorizer pode ser reutilizado
        para transformar novos textos.
    """
    if not corpus_textos:
        return np.array([]), None
    vectorizer = TfidfVectorizer(max_features=500, stop_words=None, ngram_range=(1, 2))
    matriz = vectorizer.fit_transform(corpus_textos)
    return matriz.toarray(), vectorizer


def obter_sugestao_reescrita(nome_lacuna):
    """Retorna sugestao de reescrita para uma clausula ausente (Premium).

    Args:
        nome_lacuna: Nome da lacuna conforme chave de REGEX_LACUNAS.

    Returns:
        String com o texto sugerido para a clausula, ou None se nao houver.
    """
    return SUGESTOES_REESCRITA.get(nome_lacuna)
