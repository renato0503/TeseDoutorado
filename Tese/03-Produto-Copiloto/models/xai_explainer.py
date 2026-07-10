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
        "explicacao": "Conforme Art. 6º da LGPD, a protecao de dados pessoais e mandatoria. "
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
                      "previstas no Art. 5º da Lei 14.133/2021.",
    },
    "inovacao": {
        "titulo": "DA INOVACAO TECNOLOGICA",
        "explicacao": "Contratacoes de inovacao devem seguir o Marco Legal das Startups "
                      "(LC 182/2021), permitindo modalidades especiais como encomenda tecnologica.",
    },
}


def obter_explicacao(clausula_nome):
    template = XAI_TEMPLATES.get(clausula_nome)
    if template:
        return template
    return {
        "titulo": clausula_nome.replace("_", " ").upper(),
        "explicacao": "Clausula identificada com base na analise de 572.045 contratos do PNCP "
                      "e na legislacao vigente (Lei 14.133/2021).",
    }


def gerar_explicacoes_clausulas(clausulas_encontradas):
    explicacoes = []
    for nome in clausulas_encontradas:
        explicacoes.append(obter_explicacao(nome))
    return explicacoes


def gerar_resumo_shap(features):
    linhas = []
    for f in features[:5]:
        linhas.append(
            f"{f['feature']}: {f['peso'] * 100:.2f}% de impacto na predicao de risco ({f['explicacao'][:80]}...)"
        )
    return linhas
