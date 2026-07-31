"""
Monta a tese unificada com conteudo completo dos artigos.
"""
import re

thesis_path = r"C:\Users\Renato\Documents\Doutorado\Tese\tese_draft.html"
art01_path = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\01-Artigo-Cientifico-Diagnostico\artigo_01_diagnostico.html"
art02_path = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\02-Artigo-Tecnologico-Copiloto\artigo_02_tecnologico.html"

with open(thesis_path, "r", encoding="utf-8") as f:
    thesis = f.read()

with open(art01_path, "r", encoding="utf-8") as f:
    art01 = f.read()
with open(art02_path, "r", encoding="utf-8") as f:
    art02 = f.read()

# Extract body from articles
art01_body = art01.split("<body>")[1].split("</body>")[0]
art02_body = art02.split("<body>")[1].split("</body>")[0]

# Remove control panels, abstracts, page-footers
for body in [art01_body, art02_body]:
    body = re.sub(r'<div class="control-panel[^>]*>.*?</div>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="abstract-box">.*?</div>', '', body, flags=re.DOTALL)

art01_body = re.sub(r'<div class="control-panel[^>]*>.*?</div>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<h1 class="paper-title">.*?</h1>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<p class="author-info">.*?</p>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<div class="page-footer">.*?</div>', '', art01_body)

art02_body = re.sub(r'<div class="control-panel[^>]*>.*?</div>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<h1 class="paper-title">.*?</h1>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<p class="author-info">.*?</p>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<div class="page-footer">.*?</div>', '', art02_body)

# Remove section/page wrappers from articles (thesis has its own)
art01_body = art01_body.replace('<section class="paper-page">', '').replace('</section>', '')
art01_body = art01_body.replace('<div class="page-content">', '').replace('</div>', '')
art02_body = art02_body.replace('<section class="paper-page">', '').replace('</section>', '')
art02_body = art02_body.replace('<div class="page-content">', '').replace('</div>', '')

# Chapter header for Article 01
ch2 = '<section class="paper-page">\n<div class="page-content">\n<h2>2 DIAGNOSTICO EMPIRICO DAS COMPRAS COMPLEXAS</h2>\n<p style="text-align:center;font-size:10pt;color:#555;">Capitulo baseado no Artigo 1</p>\n'
ch3 = '<section class="paper-page">\n<div class="page-content">\n<h2>3 COPILOTO ALGORITMICO: DESENVOLVIMENTO E VALIDACAO</h2>\n<p style="text-align:center;font-size:10pt;color:#555;">Capitulo baseado no Artigo 2</p>\n'

ch4 = '''<section class="paper-page">
<div class="page-content">
<h2>4 O PRODUTO: COPILOTO ALGORITMICO</h2>
<p style="text-align:center;font-size:10pt;color:#555;">Entregavel 3: Artefato Tecnologico Implementado</p>
<p>O Copiloto Algoritmico e uma aplicacao web servida integralmente no Firebase (Hosting + Cloud Functions + Firestore + Authentication), com codigo-fonte aberto sob licenca MIT disponivel em repositorio GitHub. A ferramenta integra os modelos de Aprendizado de Maquina descritos no Capitulo 3 em uma interface acessivel a gestores publicos nao-especialistas, operando com dois modulos principais: Avaliacao de Minutas e Geracao de Editais, este ultimo apoiado por IA generativa (NVIDIA llama-3.3-70b) com fallback para templates.</p>
<p>A arquitetura do sistema utiliza cache singleton para carregamento dos modelos serializados, assegurando que o carregamento ocorra uma unica vez por cold start. O pipeline de inferencia completo (TF-IDF + Isolation Forest + Random Forest + SHAP) e executado pela Cloud Function <em>analisar_minuta</em> (Python 3.11, 512 MB, timeout 120s). O sistema implementa 16 padroes de expressao regular para deteccao de clausulas contratuais e contrafactuais normativos para clausulas ausentes.</p>
<p>O Modulo de Avaliacao permite que o usuario submeta o texto de uma minuta e receba analise completa integrando os tres motores do sistema: deteccao de clausulas por regex, identificacao de lacunas contratuais com score de criticidade, calculo de score de conformidade, predicao de risco pelo Random Forest integrado (com campo para valor estimado e vigencia prevista informados pelo usuario), deteccao de padroes textuais atipicos pelo Isolation Forest, e atribuicao de importancia via SHAP com contrafactuais juridicos. O Modulo de Geracao permite a criacao de minutas completas a partir de formulario estruturado com tres abas: Dados Basicos, Clausulas Juridicas e Revisao Final. As clausulas geradas sao acompanhadas de justificativas baseadas em XAI, referenciando a fundamentacao legal (Lei 14.133/2021, LGPD, LC 182/2021) e teorica (Williamson, Jensen, Akerlof). O sistema oferece exportacao da minuta completa.</p>
<p>O deploy e realizado via Firebase (Hosting + Cloud Functions) a partir do repositorio GitHub. Os modelos em producao apresentam as metricas do modelo pos-remediacao (Acuracia 93,36%, AUC-ROC 90,83%, F1-Score 26,39%), carregadas do arquivo metricas.json, com nota explicita sobre o desbalanceamento da classe (1,99% de positivos). Testes unitarios (20 casos) cobrem os modulos criticos. Para documentacao detalhada, consulte <em>Tese/03-Produto-Copiloto/docs/</em> e o repositorio GitHub.</p>
</div>
<div class="page-footer">5</div>
</section>
'''

ch5 = '''<section class="paper-page">
<div class="page-content">
<h2>5 CONCLUSAO GERAL</h2>
<p>A presente tese investigou o fenomeno das compras publicas complexas no Brasil sob a lente da Economia dos Custos de Transacao e da Assimetria Informacional, adotando o paradigma da Design Science Research para conceber, desenvolver e validar um artefato de suporte a decisao baseado em Inteligencia Artificial Explicavel. Os tres entregaveis que compoem a tese — diagnostico empirico, artigo tecnologico e produto implementado — articulam-se em uma arquitetura coerente que percorre as seis etapas do processo de DSR de Peffers et al. (2007), desde a identificacao do problema ate a comunicacao dos resultados.</p>
<p>O diagnostico empirico (Capitulo 2) revelou um mercado de compras complexas altamente concentrado (Gini = 0,89), no qual 10 orgaos respondem por 80,9% do volume financeiro e 10 fornecedores capturam 43,9% do valor. A regressao logistica demonstrou que, controlando por vigencia e valor, compras complexas estao associadas a um aumento de 71% na odds de eventos adversos (OR = 1,71), e que a vigencia contratual atua como fator de exposicao cumulativa ao risco (OR = 1,48; HR = 1,85 no modelo de Cox). Estes achados oferecem uma reinterpretacao do fenomeno do apagao das canetas: a paralisia decisoria tem raizes estruturais que nao serao resolvidas por punicao de gestores.</p>
<p>O desenvolvimento do Copiloto Algoritmico (Capitulo 3) demonstrou a viabilidade tecnica e a defesa juridica de implementar Aprendizado de Maquina avancado no setor publico. O artefato integra Isolation Forest e Random Forest com atribuicao de importancia via SHAP, oferecendo ao gestor uma trilha de auditoria que atende aos requisitos de motivacao da Lei 14.133/2021 e ao direito a explicacao da LGPD. As metricas de desempenho obtidas (Acuracia 93,36%, AUC-ROC 90,83%, F1-Score 26,39%) superam cinco modelos de referencia, com nota explicita sobre o desbalanceamento da classe. Cinco principios de design para XAI no setor publico foram extraidos como contribuicao teorica.</p>
<p>O produto implementado (Capitulo 4) materializa os achados dos capitulos anteriores em uma aplicacao web funcional, com codigo aberto, deploy em nuvem e documentacao completa. A ferramenta opera como agente recomendante, preservando a autonomia decisoria do gestor e demonstrando que a modernizacao tecnologica das compras publicas e compativel com a preservacao dos principios constitucionais da administracao publica.</p>
<p>Como contribuicao teorica, a tese oferece evidencias empiricas que corroboram a predicao da Economia dos Custos de Transacao e qualificam a aplicacao da Teoria da Agencia ao contexto brasileiro. Os cinco principios de design extraidos do processo de construcao do artefato constituem uma contribuicao para a literatura de Sistemas de Informacao. Como contribuicao pratica, a tese entrega um artefato funcional que pode ser utilizado por gestores publicos para auditoria de minutas de editais.</p>
<p>Como limitacoes, reconhece-se que a variavel dependente e uma proxy de eventos adversos, nao uma medida direta de fracasso contratual. A classificacao NLP carece de validacao contra anotacao manual. O artefato nao foi submetido a avaliacao com usuarios reais. Como agenda de pesquisa futura, destacam-se: validacao do dicionario NLP; incorporacao de controles institucionais aos modelos; construcao de variaveis dependentes a partir de desfechos diretamente observados; e conducao de experimentos controlados com gestores publicos para avaliar utilidade, compreensibilidade e impacto do Copiloto sobre a qualidade dos editais.</p>
</div>
<div class="page-footer">6</div>
</section>
'''

refs = '''<section class="paper-page">
<div class="page-content">
<h2>REFERENCIAS CONSOLIDADAS</h2>
<p class="ref-entry">Akerlof, G. A. (1970). The market for "lemons": Quality uncertainty and the market mechanism. <em>The Quarterly Journal of Economics</em>, <em>84</em>(3), 488-500. https://doi.org/10.2307/1879431</p>
<p class="ref-entry">Bain, J. S. (1956). <em>Barriers to new competition</em>. Harvard University Press.</p>
<p class="ref-entry">Brammer, S., & Walker, H. (2011). Sustainable procurement in the public sector. <em>International Journal of Operations & Production Management</em>, <em>31</em>(4), 452-476.</p>
<p class="ref-entry">Breiman, L. (2001). Random forests. <em>Machine Learning</em>, <em>45</em>(1), 5-32.</p>
<p class="ref-entry">Coase, R. H. (1937). The nature of the firm. <em>Economica</em>, <em>4</em>(16), 386-405.</p>
<p class="ref-entry">Doshi-Velez, F., & Kim, B. (2017). Towards a rigorous science of interpretable machine learning. <em>arXiv:1702.08608</em>.</p>
<p class="ref-entry">Edler, J., & Georghiou, L. (2007). Public procurement and innovation. <em>Research Policy</em>, <em>36</em>(7), 949-963.</p>
<p class="ref-entry">Flynn, A., & Davis, P. (2014). Theory in public procurement research. <em>Journal of Public Procurement</em>, <em>14</em>(2), 139-180.</p>
</div>
<div class="page-footer">7</div>
</section>
'''

# Remove closing tags from thesis
thesis = re.sub(r'</body>\s*</html>', '', thesis)

# Assemble
full = thesis + ch2 + art01_body + '\n</div>\n</section>\n'
full += ch3 + art02_body + '\n</div>\n</section>\n'
full += ch4 + ch5 + refs
full += '\n</body>\n</html>'

with open(thesis_path, "w", encoding="utf-8") as f:
    f.write(full)

print("Tese montada com sucesso.")
