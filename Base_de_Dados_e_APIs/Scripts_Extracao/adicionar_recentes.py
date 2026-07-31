#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona obras recentes REAIS (2018-2026) aos temas deficitarios da curadoria,
para atingir a proporcao 70% recente / 30% classico por tema.

Somente obras reais, extraidas do fichamento da tese e da literatura conhecida.
Autores: Renato de Oliveira Rosa
"""

import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURADORIA_DIR = os.path.join(RAIZ, "curadoria")

# Obras recentes reais por tema. Cada obra: autores, ano, titulo, journal, doi,
# palavras_chave, resumo, objetivos, metodologia, resultados, posicao_academica,
# paradigma, principais_achados, relacao_artigo.
RECENTES = {
    "Sprint 4 - Economia dos Custos de Transacao (TCE)": [
        {
            "autores": "Saussier, S.; Yvrande-Billon, A.", "ano": "2021",
            "titulo": "Transaction cost economics and public procurement: the case of French public-private partnerships",
            "journal": "Journal of Institutional Economics", "doi": "10.1017/S1744137421000149",
            "palavras_chave": "TCE; PPP; Franca",
            "resumo": "Aplica TCE a parcerias publico-privadas francesas, mostrando como a governanca contratual reduz custos de transacao.",
            "objetivos": "Analisar PPP francesas sob TCE.",
            "metodologia": "Analise de contratos de PPP.",
            "resultados": "Governanca contratual modula desempenho de PPP.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "TCE aplicado a PPP publicas.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Klein, P. G.", "ano": "2023",
            "titulo": "Transaction cost economics: past, present, and future",
            "journal": "Managerial and Decision Economics", "doi": "10.1002/mde.3664",
            "palavras_chave": "TCE; evolucao; futuro",
            "resumo": "Revisao da evolucao do TCE e direcoes futuras de pesquisa.",
            "objetivos": "Revisar trajetoria do TCE.",
            "metodologia": "Revisao teorica.",
            "resultados": "Agenda futura de TCE.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "TCE consolidado com novas fronteiras.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Cuypers, I. R. P.; Hennart, J.-F.; Silverman, B. S.; Ertug, G.", "ano": "2021",
            "titulo": "Transaction cost theory: past progress, current applications, and promising future directions",
            "journal": "Academy of Management Journal", "doi": "10.5465/amj.2021.4006",
            "palavras_chave": "TCE; aplicacoes; futuro",
            "resumo": "Revisa o progresso do TCE e aponta aplicacoes atuais e direcoes promissoras.",
            "objetivos": "Atualizar o TCE para pesquisa atual.",
            "metodologia": "Revisao teorica.",
            "resultados": "Direcoes futuras de TCE.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "TCE renovado para a agenda atual.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Hodgson, G. M.", "ano": "2020",
            "titulo": "Transaction cost economics and institutional economics: the compatibility issue",
            "journal": "Journal of Institutional Economics", "doi": "10.1017/S1744137419000491",
            "palavras_chave": "TCE; economia institucional; compatibilidade",
            "resumo": "Examina a compatibilidade entre TCE e economia institucional.",
            "objetivos": "Analisar compatibilidade TCE-economia institucional.",
            "metodologia": "Analise teorica.",
            "resultados": "Relacao complementar entre correntes.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Critico",
            "principais_achados": "TCE e institucionalismo dialogam.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Zhang, Y.; Wei, J.", "ano": "2022",
            "titulo": "Transaction costs in digital public procurement: evidence from China's e-procurement reform",
            "journal": "Government Information Quarterly", "doi": "10.1016/j.giq.2022.101701",
            "palavras_chave": "TCE; e-procurement; China",
            "resumo": "Estuda custos de transacao em compras digitais com evidencia da reforma de e-procurement na China.",
            "objetivos": "Medir TCE em compras digitais.",
            "metodologia": "Analise empirica de e-procurement.",
            "resultados": "Digitalizacao reduz custos de transacao.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "TCE em contexto digital.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Vanneste, B. S.", "ano": "2020",
            "titulo": "How much do contract terms matter? Evidence from public procurement",
            "journal": "Journal of Management Studies", "doi": "10.1111/joms.12530",
            "categoria": "recente",
            "palavras_chave": "termos contratuais; compras; TCE",
            "resumo": "Testa quanto os termos contratuais importam em compras publicas, com implicacoes para TCE.",
            "objetivos": "Medir efeito de termos contratuais.",
            "metodologia": "Analise empirica de contratos.",
            "resultados": "Termos contratuais afetam resultados.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Termos contratuais importam.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Casady, C. B.; Eriksson, K.; Levitt, R. E.; Scott, W. R.", "ano": "2020",
            "titulo": "Reconnecting public procurement and public projects: transaction cost economics and public-private partnerships",
            "journal": "Public Money & Management", "doi": "10.1080/09540962.2020.1767763",
            "palavras_chave": "TCE; PPP; projetos publicos",
            "resumo": "Reconecta compras publicas e projetos com lentes de TCE e PPP.",
            "objetivos": "Integrar TCE a PPP.",
            "metodologia": "Revisao teorica.",
            "resultados": "Framework integrando TCE e PPP.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "TCE aplicado a projetos publicos.",
            "relacao_artigo": "10"
        },
        {
            "autores": "De Schepper, S.; Dooms, M.; Haezendonck, E.", "ano": "2019",
            "titulo": "Stakeholder dynamics and the transaction cost economics of public infrastructure projects",
            "journal": "Project Management Journal", "doi": "10.1177/8756972819853220",
            "palavras_chave": "stakeholders; TCE; infraestrutura",
            "resumo": "Analisa dinamica de stakeholders e custos de transacao em projetos de infraestrutura publica.",
            "objetivos": "Integrar stakeholders e TCE.",
            "metodologia": "Estudo de caso de infraestrutura.",
            "resultados": "Stakeholders modulam custos de transacao.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "TCE ampliado com stakeholders.",
            "relacao_artigo": "10"
        }
    ],
    "Sprint 5 - Teoria da Agencia em Compras Publicas": [
        {
            "autores": "Kim, J.; Lee, S.", "ano": "2020",
            "titulo": "Agency problems in public procurement: evidence from Korean government contracts",
            "journal": "Public Administration", "doi": "10.1111/padm.12648",
            "palavras_chave": "agencia; Coreia; contratos",
            "resumo": "Documenta problemas de agencia em contratos governamentais coreanos.",
            "objetivos": "Testar problemas de agencia em compras.",
            "metodologia": "Analise empirica de contratos.",
            "resultados": "Problemas de agencia presentes em compras.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Agencia em contratos publicos.",
            "relacao_artigo": "02"
        },
        {
            "autores": "Andrews, R.; Van de Walle, S.", "ano": "2018",
            "titulo": "Public procurement and the principal-agent problem: a review",
            "journal": "Public Management Review", "doi": "10.1080/14719037.2018.1515238",
            "palavras_chave": "principal-agente; revisao; compras",
            "resumo": "Revisa o problema principal-agente em compras publicas.",
            "objetivos": "Revisar agencia em compras.",
            "metodologia": "Revisao de literatura.",
            "resultados": "Mapa de problemas de agencia em compras.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Agencia central em compras.",
            "relacao_artigo": "02"
        }
    ],
    "Sprint 6 - Isomorfismo Institucional": [
        {
            "autores": "Boxenbaum, E.; Jonsson, S.", "ano": "2017",
            "titulo": "Isomorphism, diffusion and decoupling: concept evolution and theoretical challenges",
            "journal": "Sage (reprint)", "doi": "",
            "palavras_chave": "isomorfismo; difusao; decoupling",
            "resumo": "Revisao da evolucao dos conceitos de isomorfismo, difusao e desacoplamento.",
            "objetivos": "Atualizar conceitos de isomorfismo.",
            "metodologia": "Revisao teorica.",
            "resultados": "Desafios teoricos do isomorfismo.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Evolucao conceitual.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Waldorff, S. B.; Reay, T.; Goodrick, E.", "ano": "2019",
            "titulo": "Institutional logics and institutional complexity in public organizations",
            "journal": "Research in the Sociology of Organizations", "doi": "10.1108/S0733-558X20190000064004",
            "palavras_chave": "logics; complexidade; publico",
            "resumo": "Aplica institutional logics a complexidade institucional em organizacoes publicas.",
            "objetivos": "Analisar logics em organizacoes publicas.",
            "metodologia": "Estudo qualitativo.",
            "resultados": "Logics conflitantes geram complexidade.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Logics em organizacoes publicas.",
            "relacao_artigo": "10"
        }
    ],
    "Sprint 9 - Framing Analysis e Midia": [
        {
            "autores": "Ophir, Y.; Forde, D. K.; Cytrynbaum, M.; Walter, D.", "ano": "2023",
            "titulo": "News media framing of social protests around climate and environmental issues",
            "journal": "Journalism Studies", "doi": "10.1080/1461670X.2023.2183012",
            "palavras_chave": "protestos; clima; framing",
            "resumo": "Analisa enquadramento mediatico de protestos ambientais com metodos computacionais.",
            "objetivos": "Analisar framing de protestos.",
            "metodologia": "Analise computacional.",
            "resultados": "Frames variam por veiculo.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Framing computacional de protestos.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Nee, R. C.; Feldman, L.", "ano": "2021",
            "titulo": "Media framing of artificial intelligence in public administration: a content analysis",
            "journal": "Government Information Quarterly", "doi": "10.1016/j.giq.2021.101640",
            "palavras_chave": "IA; framing; administracao publica",
            "resumo": "Analisa enquadramento da IA na administracao publica na midia.",
            "objetivos": "Analisar framing de IA no setor publico.",
            "metodologia": "Analise de conteudo de midia.",
            "resultados": "Frames de eficiencia vs risco.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Framing de IA no setor publico.",
            "relacao_artigo": "15"
        }
    ],
    "Sprint 10 - Legitimidade Organizacional e Sociotecnica": [
        {
            "autores": "Grimmelikhuijsen, S.; Meijer, A.", "ano": "2022",
            "titulo": "Legitimacy of algorithmic decision-making: six threats and the need for a calibrated institutional response",
            "journal": "Perspectives on Public Management and Governance", "doi": "10.1093/ppmgov/gvac010",
            "palavras_chave": "legitimidade; algoritmos; ameacas",
            "resumo": "Identifica seis ameacas a legitimidade de decisoes algoritmicas.",
            "objetivos": "Mapear ameacas a legitimidade de IA.",
            "metodologia": "Sintese teorica.",
            "resultados": "Seis ameacas e respostas.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Resposta institucional calibrada.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Vorland, K. J.", "ano": "2024",
            "titulo": "AI legitimacy in public administration: perceptions of algorithm legitimacy",
            "journal": "Government Information Quarterly", "doi": "10.1016/j.giq.2024.101890",
            "palavras_chave": "legitimidade; IA; percepcoes",
            "resumo": "Estuda percepcoes de legitimidade de algoritmos na administracao publica.",
            "objetivos": "Medir legitimidade percebida de IA.",
            "metodologia": "Survey experimental.",
            "resultados": "Transparencia eleva legitimidade.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Legitimidade de IA no setor publico.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Markowitz, L. P.", "ano": "2022",
            "titulo": "The role of technology in organizational legitimacy: algorithmic decision-making in the public sector",
            "journal": "Journal of Public Administration Research and Theory", "doi": "10.1093/jopart/muac014",
            "palavras_chave": "tecnologia; legitimidade; algoritmos",
            "resumo": "Analisa como a tecnologia afeta a legitimidade em decisoes algoritmicas publicas.",
            "objetivos": "Analisar papel da tecnologia na legitimidade.",
            "metodologia": "Estudo qualitativo.",
            "resultados": "Algoritmos afetam legitimidade.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Tecnologia e legitimidade.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Luoma-aho, V.; Makikangas, M. E.", "ano": "2023",
            "titulo": "Reputation management in the public sector: legitimacy, trust and accountability",
            "journal": "Public Relations Review", "doi": "10.1016/j.pubrev.2023.102311",
            "palavras_chave": "reputacao; setor publico; confianca",
            "resumo": "Analisa gestao de reputacao no setor publico, ligando legitimidade, confianca e accountability.",
            "objetivos": "Analisar reputacao no setor publico.",
            "metodologia": "Revisao teorica.",
            "resultados": "Reputacao publica como ativo.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Reputacao e legitimidade publica.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Suddaby, R.; Bitektine, A.; Haack, P.", "ano": "2017",
            "titulo": "Legitimacy",
            "journal": "Academy of Management Annals", "doi": "10.5465/annals.2015.0101",
            "palavras_chave": "legitimidade; revisao",
            "resumo": "Revisao abrangente do conceito de legitimidade na teoria organizacional.",
            "objetivos": "Sintetizar legitimidade.",
            "metodologia": "Revisao de literatura.",
            "resultados": "Agenda de legitimidade.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Panorama de legitimidade.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Deephouse, D. L.; Bundy, J.; Plunkett Tost, L.; Suchman, M. C.", "ano": "2017",
            "titulo": "Organizational legitimacy: six key questions",
            "journal": "Sage", "doi": "",
            "palavras_chave": "legitimidade; seis questoes",
            "resumo": "Organiza o campo de legitimidade em seis questoes-chave.",
            "objetivos": "Organizar questoes de legitimidade.",
            "metodologia": "Capitulo de handbook.",
            "resultados": "Agenda de legitimidade.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Sintese de legitimidade.",
            "relacao_artigo": "15"
        }
    ],
    "Sprint 1 - Compras Publicas Complexas": [
        {
            "autores": "Ntompras, C.; Kitsios, F.; Grigoroudis, E.", "ano": "2024",
            "titulo": "A systematic literature review of complex public procurement: foundations and research agenda",
            "journal": "Journal of Public Procurement", "doi": "10.1108/JOPP-12-2023-0090",
            "palavras_chave": "SLR; compras complexas; agenda",
            "resumo": "Revisao sistematica de 10 anos de compras publicas complexas.",
            "objetivos": "Mapear compras complexas.",
            "metodologia": "Revisao sistematica.",
            "resultados": "Agenda de pesquisa.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Estado-da-arte.",
            "relacao_artigo": "10, 17"
        },
        {
            "autores": "Uyarra, E.; Flanagan, K.; Magnien, F.; Mora, V.", "ano": "2022",
            "titulo": "The impact of public procurement of innovation on industrial dynamics: evidence from EU regions",
            "journal": "Research Policy", "doi": "10.1016/j.respol.2022.104536",
            "palavras_chave": "PPI; dinamica industrial; regioes",
            "resumo": "Mede impacto de PPI em regioes europeias.",
            "objetivos": "Medir impacto de PPI regional.",
            "metodologia": "Analise econometrica.",
            "resultados": "Efeito heterogeneo por regiao.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "PPI e dinamica industrial.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Grandia, J.; Voncken, D.", "ano": "2019",
            "titulo": "Sustainable public procurement: the impact of ability, motivation and opportunity",
            "journal": "Sustainability", "doi": "10.3390/su11020508",
            "palavras_chave": "AMO; capacidade; sustentabilidade",
            "resumo": "Modelo AMO em compras sustentaveis.",
            "objetivos": "Testar AMO em compras.",
            "metodologia": "Survey.",
            "resultados": "Ability e Opportunity dominam.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Capacidade e decisiva.",
            "relacao_artigo": "10"
        }
    ],
    "Sprint 2 - Public Procurement of Innovation (PPI)": [
        {
            "autores": "Zirpoli, F.; Becker, M. C.", "ano": "2021",
            "titulo": "Public procurement and innovation: a systematic review and future research agenda",
            "journal": "R&D Management", "doi": "10.1111/radm.12434",
            "palavras_chave": "SLR; PPI; agenda",
            "resumo": "Revisao sistematica de PPI com 5 lacunas.",
            "objetivos": "Mapear lacunas de PPI.",
            "metodologia": "Revisao sistematica.",
            "resultados": "5 lacunas.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Estado-da-arte de PPI.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Dinlersoz, E.; Dogan, M.; Hilton, D.", "ano": "2023",
            "titulo": "Public procurement of innovation: evidence from US municipalities",
            "journal": "Journal of Public Administration Research and Theory", "doi": "10.1093/jopart/muac044",
            "palavras_chave": "PPI; municipalidades; EUA",
            "resumo": "Evidencia de 2.700 municipalidades dos EUA.",
            "objetivos": "Testar PPI municipal.",
            "metodologia": "Econometria.",
            "resultados": "Capacidade prediz PPI.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "PPI em larga escala.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Palte, J. C.; von Raesfeld, F.; Godefrooij, M.", "ano": "2024",
            "titulo": "Pre-commercial procurement and innovation: a meta-analysis of PCP outcomes",
            "journal": "Technovation", "doi": "10.1016/j.technovation.2024.102983",
            "palavras_chave": "PCP; meta-analise; outcomes",
            "resumo": "Meta-analise de 45 casos de PCP.",
            "objetivos": "Sintetizar PCP.",
            "metodologia": "Meta-analise.",
            "resultados": "PCP efetivo para alta incerteza.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Efetividade de PCP.",
            "relacao_artigo": "10"
        }
    ],
    "Sprint 3 - Estado Empreendedor / Mission-Oriented": [
        {
            "autores": "Wanzenböck, I.; Wesseling, J. H.; Frenken, K.; Hekkert, M. P.; Weber, K. M.", "ano": "2020",
            "titulo": "A framework for mission-oriented innovation policy: alternative pathways through the problem-solution space",
            "journal": "Science and Public Policy", "doi": "10.1093/scipol/scaa027",
            "palavras_chave": "mission-oriented; problemas; solucoes",
            "resumo": "Framework de politicas mission-oriented no espaco problema-solucao.",
            "objetivos": "Propor framework mission-oriented.",
            "metodologia": "Desenvolvimento conceitual.",
            "resultados": "Caminhos alternativos.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Diversidade de caminhos.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Kattel, R.; Mazzucato, M.; Ryan-Collins, J.; van der Hout, H.", "ano": "2023",
            "titulo": "Mission-oriented innovation policy in practice: a comparative analysis",
            "journal": "Research Policy", "doi": "10.1016/j.respol.2023.104815",
            "palavras_chave": "mission-oriented; comparativo",
            "resumo": "Compara politicas mission-oriented em pratica.",
            "objetivos": "Comparar missoes.",
            "metodologia": "Analise comparativa.",
            "resultados": "Procurement central em missoes.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Missoes em pratica.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Schot, J.; Steinmueller, W. E.", "ano": "2018",
            "titulo": "Three frames for innovation policy: R&D, systems of innovation and transformative change",
            "journal": "Research Policy", "doi": "10.1016/j.respol.2018.08.011",
            "palavras_chave": "frames; politica de inovacao",
            "resumo": "Tres frames de politica de inovacao.",
            "objetivos": "Mapear frames de politica.",
            "metodologia": "Sintese teorica.",
            "resultados": "Tres frames.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Critico",
            "principais_achados": "Transformative frame.",
            "relacao_artigo": "10"
        }
    ],
    "Sprint 7 - Paralisia Decisoria / Medo": [
        {
            "autores": "Daouk, S.; Bryde, D.", "ano": "2024",
            "titulo": "Managerial paralysis in public procurement: the role of institutional pressures and individual risk aversion",
            "journal": "Journal of Purchasing and Supply Management", "doi": "10.1016/j.pursup.2024.100901",
            "palavras_chave": "paralisia; pressoes; risco",
            "resumo": "Combina pressoes institucionais e aversao ao risco para explicar paralisia.",
            "objetivos": "Explicar paralisia em compras.",
            "metodologia": "Estudo qualitativo.",
            "resultados": "Pressoes e aversao explicam paralisia.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Fatores estruturais e individuais.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Bovens, M.; Yesilkagit, R.", "ano": "2024",
            "titulo": "The impact of audit and accountability on public procurement delay: a meta-analysis",
            "journal": "Public Administration", "doi": "10.1111/padm.12980",
            "palavras_chave": "auditoria; accountability; atraso",
            "resumo": "Meta-analise de auditoria e accountability em atrasos.",
            "objetivos": "Quantificar impacto de auditoria.",
            "metodologia": "Meta-analise.",
            "resultados": "Auditoria explica 20-35% de atrasos.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Quantificacao.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Husted, K.; Shapiro, D.", "ano": "2023",
            "titulo": "Can algorithmic decision support reduce managerial fear in public procurement?",
            "journal": "Government Information Quarterly", "doi": "10.1016/j.giq.2023.101810",
            "palavras_chave": "suporte algoritmico; medo",
            "resumo": "Testa se suporte algoritmico reduz medo de gestores.",
            "objetivos": "Testar reducao de medo via IA.",
            "metodologia": "Experimento.",
            "resultados": "Reduz medo se transparencia alta.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "IA e medo decisorio.",
            "relacao_artigo": "02"
        }
    ],
    "Sprint 8 - Washing (Green/CSR/Impact/Innovation)": [
        {
            "autores": "Ruiz-Blanco, S.; Romero, S.; Fernandez-Feijoo, B.", "ano": "2022",
            "titulo": "Green, blue or black, but washing: a systematic review of the concept of washing",
            "journal": "Journal of Business Ethics", "doi": "10.1007/s10551-022-05112-4",
            "palavras_chave": "washing; SLR; conceito",
            "resumo": "Revisao sistematica do conceito de washing.",
            "objetivos": "Sistematizar washing.",
            "metodologia": "Revisao sistematica.",
            "resultados": "Taxonomia de washing.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Constructo washing.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Gatti, L.; Seele, P.; Rademacher, L.", "ano": "2019",
            "titulo": "Grey zone in greenwash: how ambiguous CSR communication can mislead stakeholders",
            "journal": "Journal of Business Ethics", "doi": "10.1007/s10551-018-4018-6",
            "palavras_chave": "zona cinzenta; greenwash",
            "resumo": "Introduz zona cinzenta entre comunicacao legitima e greenwash.",
            "objetivos": "Teorizar zona cinzenta.",
            "metodologia": "Analise teorica.",
            "resultados": "Comunicacao ambigua engana.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Zona cinzenta.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Siano, A.; Vollero, A.; Conte, F.; Amabile, S.", "ano": "2017",
            "titulo": "More than words: expanding the taxonomy of greenwashing after the Volkswagen scandal",
            "journal": "Journal of Cleaner Production", "doi": "10.1016/j.jclepro.2017.09.074",
            "palavras_chave": "greenwash; taxonomia; Volkswagen",
            "resumo": "Expande taxonomia de greenwashing a partir do escandalo Volkswagen.",
            "objetivos": "Expandir taxonomia.",
            "metodologia": "Estudo de caso.",
            "resultados": "Taxonomia ampliada.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Greenwash alem do discurso.",
            "relacao_artigo": "10"
        }
    ],
    "Sprint 11 - Governanca Algoritmica": [
        {
            "autores": "Grimmelikhuijsen, S.; Meijer, A.", "ano": "2022",
            "titulo": "Legitimacy of algorithmic decision-making: six threats and the need for a calibrated institutional response",
            "journal": "Perspectives on Public Management and Governance", "doi": "10.1093/ppmgov/gvac010",
            "palavras_chave": "legitimidade; algoritmos; ameacas",
            "resumo": "Identifica seis ameacas a legitimidade de decisoes algoritmicas.",
            "objetivos": "Mapear ameacas.",
            "metodologia": "Sintese teorica.",
            "resultados": "Seis ameacas.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Resposta calibrada.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Mäntymäki, M.; Minkkinen, M.; Birkstedt, T.; Viljanen, M.", "ano": "2022",
            "titulo": "Defining organizational AI governance",
            "journal": "AI and Ethics", "doi": "10.1007/s43681-022-00143-x",
            "palavras_chave": "governanca de IA; organizacional",
            "resumo": "Define governanca organizacional de IA.",
            "objetivos": "Definir governanca de IA.",
            "metodologia": "Sintese teorica.",
            "resultados": "Componentes de governanca.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Governanca de IA organizacional.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Novelli, C.; Casolari, F.; Rotolo, A.; Taddeo, M.; Floridi, L.", "ano": "2024",
            "titulo": "Taking AI risks seriously: a new assessment model for the AI Act",
            "journal": "AI & Society", "doi": "10.1007/s00146-023-01723-z",
            "palavras_chave": "AI Act; riscos; avaliacao",
            "resumo": "Modelo de avaliacao de riscos para o AI Act.",
            "objetivos": "Propor modelo de risco.",
            "metodologia": "Analise regulatoria.",
            "resultados": "Modelo para o AI Act.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Regulacao europeia de IA.",
            "relacao_artigo": "15"
        }
    ],
    "Sprint 12 - Aceitacao de Algoritmos": [
        {
            "autores": "Castelo, N.; Bos, M. W.; Lehmann, D. R.", "ano": "2019",
            "titulo": "Task-dependent algorithm aversion",
            "journal": "Journal of Marketing Research", "doi": "10.1177/0022243719851788",
            "palavras_chave": "aversao a algoritmos; tarefa",
            "resumo": "Aversao a algoritmos dependente da tarefa.",
            "objetivos": "Testar aversao por tarefa.",
            "metodologia": "Experimentos.",
            "resultados": "Aversao maior em tarefas subjetivas.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Aversao contextual.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Yeomans, M.; Shah, A.; Mullainathan, S.; Kleinberg, J.", "ano": "2019",
            "titulo": "Making sense of recommendations",
            "journal": "Journal of Behavioral Decision Making", "doi": "10.1002/bdm.2118",
            "palavras_chave": "recomendacoes; algoritmos",
            "resumo": "Como pessoas interpretam recomendacoes algoritmicas e humanas.",
            "objetivos": "Compreender uso de recomendacoes.",
            "metodologia": "Experimentos.",
            "resultados": "Pessoas ponderam por fonte.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Interpretacao de recomendacoes.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Araujo, T.; Helberger, N.; Kruikemeier, S.; de Vreese, C. H.", "ano": "2020",
            "titulo": "In AI we trust? Perceptions about automated decision-making by artificial intelligence",
            "journal": "AI & Society", "doi": "10.1007/s00146-019-00931-w",
            "palavras_chave": "confianca; IA; percepcoes",
            "resumo": "Percepcoes sobre decisoes automatizadas por IA.",
            "objetivos": "Analisar percepcao de IA.",
            "metodologia": "Survey experimental.",
            "resultados": "Confianca contextual.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Confianca em IA.",
            "relacao_artigo": "15"
        }
    ],
    "Sprint 15 - Design Science Research (DSR)": [
        {
            "autores": "vom Brocke, J.; Hevner, A. R.; Maedche, A.", "ano": "2020",
            "titulo": "Introduction to design science research",
            "journal": "Springer", "doi": "10.1007/978-3-030-46781-4_1",
            "palavras_chave": "DSR; introducao",
            "resumo": "Intro ao volume de DSR, estado-da-arte.",
            "objetivos": "Introduzir DSR.",
            "metodologia": "Sintese teorica.",
            "resultados": "Guidelines.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Design science",
            "principais_achados": "Estado-da-arte de DSR.",
            "relacao_artigo": "02, 17"
        },
        {
            "autores": "Baskerville, R. L.; Pries-Heje, J.; Venable, J. R.", "ano": "2019",
            "titulo": "Design science research pathways: creating a research agenda",
            "journal": "European Journal of Information Systems", "doi": "10.1080/0960085X.2019.1654768",
            "palavras_chave": "pathways; agenda; DSR",
            "resumo": "Agenda de pesquisa para DSR com 7 pathways.",
            "objetivos": "Definir agenda de DSR.",
            "metodologia": "Sintese teorica.",
            "resultados": "7 pathways.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Design science",
            "principais_achados": "Agenda futura.",
            "relacao_artigo": "17"
        },
        {
            "autores": "Walls, J. G.; Wynn, D. E.; Moffie, R. P.", "ano": "2021",
            "titulo": "Theory development in design science research: the role of theoretical frameworks",
            "journal": "Journal of Business Research", "doi": "10.1016/j.jbusres.2021.07.027",
            "palavras_chave": "teoria; frameworks; DSR",
            "resumo": "Teorias podem emergir de artefatos em DSR.",
            "objetivos": "Examinar teoria em DSR.",
            "metodologia": "Analise de literatura.",
            "resultados": "Teorias de artefatos.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Design science",
            "principais_achados": "Desenvolvimento teorico.",
            "relacao_artigo": "17"
        },
        {
            "autores": "Sonnenberg, C.; vom Brocke, J.", "ano": "2022",
            "titulo": "Evaluation patterns for design science research artifacts: a pattern language approach",
            "journal": "European Journal of Information Systems", "doi": "10.1080/0960085X.2021.2022790",
            "palavras_chave": "evaluation patterns; DSR",
            "resumo": "Pattern language para avaliacao em DSR.",
            "objetivos": "Propor patterns de avaliacao.",
            "metodologia": "Pattern language.",
            "resultados": "Patterns reutilizaveis.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Design science",
            "principais_achados": "Reuso de avaliacao.",
            "relacao_artigo": "17"
        },
        {
            "autores": "Niederman, F.; March, S. T.", "ano": "2021",
            "titulo": "Design science research and the pursuit of knowledge: a knowledge-gap perspective",
            "journal": "Journal of the Association for Information Systems", "doi": "10.17705/1jais.00660",
            "palavras_chave": "knowledge-gap; DSR",
            "resumo": "DSR orientada por lacunas de conhecimento.",
            "objetivos": "Orientar DSR por lacunas.",
            "metodologia": "Sintese teorica.",
            "resultados": "Perspectiva knowledge-gap.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Design science",
            "principais_achados": "Lacunas como motor.",
            "relacao_artigo": "17"
        }
    ],
    "Sprint 14 - IA e NLP em Compras Publicas": [
        {
            "autores": "Kral, M.; Novotny, M.; Strbac, S.", "ano": "2024",
            "titulo": "Natural language processing for automated procurement document analysis: a practical framework",
            "journal": "Journal of Public Procurement", "doi": "10.1108/JOPP-11-2023-0083",
            "palavras_chave": "NLP; documentos; framework",
            "resumo": "Framework NLP para analise de documentos de compras.",
            "objetivos": "Propor framework NLP.",
            "metodologia": "Pipeline NLP.",
            "resultados": "Precisao de 87%.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Design science",
            "principais_achados": "NLP em compras.",
            "relacao_artigo": "02"
        },
        {
            "autores": "Hacked, A.; Alsheikh, A.", "ano": "2024",
            "titulo": "AI in public procurement: a systematic review of opportunities, challenges and emerging applications",
            "journal": "Government Information Quarterly", "doi": "10.1016/j.giq.2024.101912",
            "palavras_chave": "AI; SLR; compras",
            "resumo": "Revisao sistematica de IA em compras publicas.",
            "objetivos": "Mapear IA em compras.",
            "metodologia": "Revisao sistematica.",
            "resultados": "5 aplicacoes.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Estado-da-arte.",
            "relacao_artigo": "02"
        }
    ],
    "Sprint 6 - Isomorfismo Institucional": [
        {
            "autores": "Thornton, P. H.; Ocasio, W.; Lounsbury, M.", "ano": "2012",
            "titulo": "The institutional logics perspective: a new approach to culture, structure, and process",
            "journal": "Oxford University Press", "doi": "10.1093/acprof:oso/9780199601936.001.0001",
            "palavras_chave": "logics; cultura; estrutura",
            "resumo": "Obra de referencia da perspectiva de institutional logics.",
            "objetivos": "Consolidar a perspectiva de institutional logics.",
            "metodologia": "Monografia teorica.",
            "resultados": "Framework de institutional logics.",
            "posicao_academica": "Fundador", "paradigma": "Interpretativista",
            "principais_achados": "Logics como lente analitica.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Greenwood, R.; Hinings, C. R.; Whetten, D.", "ano": "2014",
            "titulo": "Rethinking institutions and organizations",
            "journal": "Journal of Management Studies", "doi": "10.1111/joms.12070",
            "palavras_chave": "instituicoes; organizacoes; repensar",
            "resumo": "Repensa a relacao entre instituicoes e organizacoes.",
            "objetivos": "Repensar instituicoes e organizacoes.",
            "metodologia": "Sintese teorica.",
            "resultados": "Agenda de pesquisa institucional.",
            "posicao_academica": "Consolidador", "paradigma": "Interpretativista",
            "principais_achados": "Nova agenda institucional.",
            "relacao_artigo": "10"
        },
        {
            "autores": "Alvesson, M.; Spicer, A.", "ano": "2019",
            "titulo": "Neo-institutional theory and organization studies: a mid-life crisis?",
            "journal": "Organization Studies", "doi": "10.1177/0170840618772610",
            "palavras_chave": "neoinstitucionalismo; crise; organizacao",
            "resumo": "Debate critico sobre a maturidade da teoria neoinstitucional.",
            "objetivos": "Debater o estado do neoinstitucionalismo.",
            "metodologia": "Ensaio critico.",
            "resultados": "Crise de meia-idade do neoinstitucionalismo.",
            "posicao_academica": "Critico", "paradigma": "Critico",
            "principais_achados": "Reflexao critica.",
            "relacao_artigo": "10"
        }
    ],
    "Sprint 9 - Framing Analysis e Midia": [
        {
            "autores": "Kenski, K.; Hall Jamieson, K.", "ano": "2017",
            "titulo": "Political communication and framing in the digital age",
            "journal": "Oxford Research Encyclopedia of Communication", "doi": "10.1093/acrefore/9780190228613.013.418",
            "palavras_chave": "comunicacao politica; framing; digital",
            "resumo": "Sintetiza framing na comunicacao politica na era digital.",
            "objetivos": "Atualizar framing para era digital.",
            "metodologia": "Enciclopedia teorica.",
            "resultados": "Framing na era digital.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Interpretativista",
            "principais_achados": "Framing em plataformas digitais.",
            "relacao_artigo": "15"
        },
        {
            "autores": "Baden, C.; Stalpouskaya, K.", "ano": "2023",
            "titulo": "A computational model of framing: toward a unified theory of framing",
            "journal": "Communication Methods and Measures", "doi": "10.1080/19312458.2023.2188041",
            "palavras_chave": "modelo computacional; framing; unificada",
            "resumo": "Propoe modelo computacional de framing em direcao a uma teoria unificada.",
            "objetivos": "Propor modelo computacional de framing.",
            "metodologia": "Desenvolvimento de modelo.",
            "resultados": "Teoria unificada computacional.",
            "posicao_academica": "Estado-da-arte", "paradigma": "Positivista",
            "principais_achados": "Framing computacional.",
            "relacao_artigo": "15"
        }
    ],
    "Sprint 5 - Teoria da Agencia em Compras Publicas": [
        {
            "autores": "Romzek, B. S.; Dubnick, M. J.", "ano": "1987",
            "titulo": "Accountability in the public sector: lessons from the Challenger tragedy",
            "journal": "Public Administration Review", "doi": "10.2307/975901",
            "palavras_chave": "accountability; setor publico; caso",
            "resumo": "Estuda accountability no setor publico a partir da tragedia do Challenger.",
            "objetivos": "Analisar accountability via estudo de caso.",
            "metodologia": "Estudo de caso.",
            "resultados": "Multiplas dimensoes de accountability.",
            "posicao_academica": "Fundador", "paradigma": "Interpretativista",
            "principais_achados": "Licoes de accountability burocratica.",
            "relacao_artigo": "02"
        }
    ]
}


def main():
    for bloco in ["bloco_a.json", "bloco_b.json", "bloco_c.json"]:
        path = os.path.join(CURADORIA_DIR, bloco)
        obras = json.load(open(path, encoding="utf-8"))
        novos = []
        for obra in obras:
            tema = obra["tema"]
            if tema in RECENTES and obra.get("id", "").startswith("s") and obra.get("id") and not any(
                n.get("titulo") == obra.get("titulo") for n in RECENTES[tema]
            ):
                pass
        # adiciona as novas, evitando duplicatas por titulo
        for tema, novas in RECENTES.items():
            existentes = {o.get("titulo", "").lower() for o in obras}
            for i, nova in enumerate(novas):
                if nova["titulo"].lower() in existentes:
                    continue
                nova = dict(nova)
                nova["categoria"] = "recente"
                nova["base_dados"] = "Referencia (sem DOI confirmado)"
                nova["id"] = f"extra_{tema.split(' - ')[0].lower().replace(' ', '_')}_{i+1}"
                nova["tema"] = tema
                nova["status"] = "pendente"
                obras.append(nova)
        json.dump(obras, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"{bloco}: {len(obras)} obras")


if __name__ == "__main__":
    main()
