"""
Reconstroi tese do zero - sem duplicacoes, estrutura limpa.
"""
import re, os, sys
sys.path.insert(0, r"C:\Users\Renato\Documents\Doutorado\scripts")
from reacentuar_artigo import MAPA_ACENTOS

THESIS = r"C:\Users\Renato\Documents\Doutorado\Tese\tese_draft.html"
ART01 = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\01-Artigo-Cientifico-Diagnostico\artigo_01_diagnostico.html"
ART02 = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\02-Artigo-Tecnologico-Copiloto\artigo_02_tecnologico.html"

# Read pre-textual from current thesis
with open(THESIS, "r", encoding="utf-8") as f:
    old = f.read()

# Extract only pre-textual (pages i through x - capa through listas)
# Find the first chapter marker
ch1_marker = '<h2>1 INTRODUÇÃO GERAL</h2>'
ch1_idx = old.find(ch1_marker)
pre = old[:ch1_idx] if ch1_idx > 0 else ""

# Read clean articles
with open(ART01, "r", encoding="utf-8") as f:
    art01 = f.read()
with open(ART02, "r", encoding="utf-8") as f:
    art02 = f.read()

# Extract body from articles
art01_body = art01.split("<body>")[1].split("</body>")[0]
art02_body = art02.split("<body>")[1].split("</body>")[0]

# Remove ONLY control panel and abstract boxes (keep all other structure)
art01_body = re.sub(r'<div class="control-panel no-print">.*?</div>', '', art01_body, flags=re.DOTALL)
art02_body = re.sub(r'<div class="control-panel no-print">.*?</div>', '', art02_body, flags=re.DOTALL)

# Remove abstract box divs
art01_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art01_body, flags=re.DOTALL)
art02_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art02_body, flags=re.DOTALL)

# Remove h1 title and author info
art01_body = re.sub(r'<h1 class="paper-title">.*?</h1>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<p class="author-info">.*?</p>', '', art01_body, flags=re.DOTALL)
art02_body = re.sub(r'<h1 class="paper-title">.*?</h1>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<p class="author-info">.*?</p>', '', art02_body, flags=re.DOTALL)

# Remove reference sections from articles
art01_body = re.sub(r'<section class="paper-page">\s*<div class="page-content">\s*<h2>REFERÊNCIAS</h2>.*?</section>', '', art01_body, flags=re.DOTALL)
art02_body = re.sub(r'<section class="paper-page">\s*<div class="page-content">\s*<h2>REFERÊNCIAS</h2>.*?</section>', '', art02_body, flags=re.DOTALL)

# Renumber h2 in articles
art01_body = art01_body.replace('<h2>1 INTRODUÇÃO</h2>', '<h2>2.1 Introdução</h2>')
art01_body = art01_body.replace('<h2>2 REFERENCIAL TEÓRICO</h2>', '<h2>2.2 Referencial Teórico</h2>')
art01_body = art01_body.replace('<h2>3 METODOLOGIA</h2>', '<h2>2.3 Metodologia</h2>')
art01_body = art01_body.replace('<h2>4 RESULTADOS E DISCUSSÃO</h2>', '<h2>2.4 Resultados e Discussão</h2>')
art01_body = art01_body.replace('<h2>5 CONCLUSÃO</h2>', '<h2>2.5 Conclusão</h2>')

art02_body = art02_body.replace('<h2>1 INTRODUÇÃO</h2>', '<h2>3.1 Introdução</h2>')
art02_body = art02_body.replace('<h2>2 METODOLOGIA DE DESENVOLVIMENTO</h2>', '<h2>3.2 Metodologia de Desenvolvimento</h2>')
art02_body = art02_body.replace('<h2>3 ARQUITETURA DO PRODUTO</h2>', '<h2>3.3 Arquitetura do Produto</h2>')
art02_body = art02_body.replace('<h2>4 AVALIAÇÃO E TESTES DE DESEMPENHO</h2>', '<h2>3.4 Avaliação e Testes de Desempenho</h2>')
art02_body = art02_body.replace('<h2>5 CONCLUSÕES TECNOLÓGICAS</h2>', '<h2>3.5 Conclusões Tecnológicas</h2>')

# Build Chapter 4 (Product), Chapter 5 (Conclusion), and References
ch4_5_refs = r'''
    <section class="paper-page">
        <div class="page-content">
            <h2>4 O PRODUTO: COPILOTO ALGORITMICO</h2>
            <p style="text-align:center;font-size:10pt;color:#555;">Entregavel 3: Artefato Tecnologico Implementado</p>
            <p>O Copiloto Algoritmico e uma aplicacao web desenvolvida em Streamlit (Python 3.11+), implantada em ambiente de nuvem gratuita (Streamlit Cloud), com codigo-fonte aberto sob licenca MIT disponivel em repositorio GitHub (github.com/renato0503/TeseDoutorado). A ferramenta integra os modelos de Aprendizado de Maquina descritos no Capitulo 3 em uma interface acessivel a gestores publicos nao-especialistas, operando com dois modulos principais: Avaliacao de Minutas e Geracao de Editais. A arquitetura do sistema utiliza cache singleton para carregamento dos modelos serializados (11 arquivos Pickle, aproximadamente 18 MB), assegurando que o carregamento ocorra uma unica vez por sessao. O pipeline de inferencia completo (TF-IDF + Isolation Forest + Random Forest + SHAP) e executado com latencia inferior a 2 segundos no ambiente de producao (1 GB RAM, 1 vCPU).</p>
            <p>O Modulo de Avaliacao permite que o usuario submeta o texto de uma minuta de edital e receba analise completa integrando os tres motores do sistema: deteccao de clausulas por regex (16 padroes), identificacao de lacunas contratuais com score de criticidade, calculo de score de conformidade (0-100%), predicao de risco pelo Random Forest integrado (com campos para valor estimado e vigencia prevista informados pelo usuario), deteccao de padroes textuais atipicos pelo Isolation Forest, e atribuicao de importancia via SHAP com grafico de barras e analise de sensibilidade simulando o efeito de alteracoes nas principais variaveis. O Modulo de Geracao permite a criacao de minutas completas a partir de formulario estruturado com tres abas (Dados Basicos, Clausulas Juridicas e Revisao Final), com justificativas baseadas em XAI referenciando a fundamentacao legal (Lei 14.133/2021, LGPD, LC 182/2021) e teorica (Williamson, Jensen, Akerlof). O sistema implementa 20 testes unitarios cobrindo os modulos criticos e oferece documentacao integrada. Para informacoes detalhadas sobre a arquitetura, os modulos e as metricas de producao, consulte os arquivos em <em>Tese/03-Produto-Copiloto/docs/</em> e o repositorio GitHub do projeto.</p>
        </div>
        <div class="page-footer">20</div>
    </section>

    <section class="paper-page">
        <div class="page-content">
            <h2>5 CONCLUSÃO GERAL</h2>
            <p>A presente tese investigou o fenomeno das compras publicas complexas no Brasil sob a lente da Economia dos Custos de Transacao e da Assimetria Informacional, adotando o paradigma da Design Science Research para conceber, desenvolver e validar um artefato de suporte a decisao baseado em Inteligencia Artificial Explicavel. Os tres entregaveis que compoem a tese articulam-se em uma arquitetura coerente que percorre as seis etapas do processo de DSR de Peffers et al. (2007), desde a identificacao do problema ate a comunicacao dos resultados.</p>
            <p>O diagnostico empirico (Capitulo 2) revelou um mercado de compras complexas altamente concentrado (Gini = 0,89), no qual 10 orgaos respondem por 80,9% do volume financeiro e 10 fornecedores capturam 43,9% do valor. A regressao logistica demonstrou que, controlando por vigencia e valor, compras complexas estao associadas a um aumento de 46% na odds de eventos adversos (OR = 1,46), e que a vigencia contratual e o preditor de maior magnitude (OR = 0,60). Estes achados oferecem uma reinterpretacao do fenomeno do apagao das canetas: a paralisia decisoria tem raizes estruturais que nao serao resolvidas por punicao de gestores, mas por investimentos em capacitacao e em ferramentas de suporte a decisao.</p>
            <p>O desenvolvimento do Copiloto Algoritmico (Capitulo 3) demonstrou a viabilidade tecnica e a defesa juridica de implementar Aprendizado de Maquina avancado no setor publico. O artefato integra Isolation Forest e Random Forest com atribuicao de importancia via SHAP, oferecendo ao gestor uma trilha de auditoria que atende aos requisitos de motivacao da Lei 14.133/2021 e ao direito a explicacao da LGPD. As metricas de desempenho obtidas (Acuracia 98,27%, AUC-ROC 98,97%, F1-Score 95,22%) superam cinco modelos de referencia. Cinco principios de design para XAI no setor publico foram extraidos como contribuicao teorica. O produto implementado (Capitulo 4) materializa os achados em uma aplicacao web funcional, com codigo aberto, deploy em nuvem e documentacao completa.</p>
            <p>Como contribuicao teorica, a tese oferece evidencias empiricas que corroboram a predicao da Economia dos Custos de Transacao e qualificam a aplicacao da Teoria da Agencia ao contexto brasileiro. Os cinco principios de design extraidos constituem uma contribuicao para a literatura de Sistemas de Informacao. Como contribuicao pratica, a tese entrega um artefato funcional que pode ser utilizado por gestores publicos para auditoria de minutas de editais, reduzindo a assimetria informacional na fase pre-contratual. Como limitacoes, reconhece-se que a variavel dependente e uma proxy, a classificacao NLP carece de validacao contra anotacao manual, e o artefato nao foi submetido a avaliacao com usuarios reais. A agenda de pesquisa futura inclui: validacao do dicionario NLP com metricas de Precisao e Revocacao; incorporacao de controles institucionais aos modelos; construcao de variaveis dependentes a partir de desfechos diretamente observados; e conducao de experimentos controlados com gestores publicos.</p>
        </div>
        <div class="page-footer">21</div>
    </section>

    <section class="paper-page">
        <div class="page-content">
            <h2>REFERENCIAS CONSOLIDADAS</h2>
            <p class="ref-entry">Akerlof, G. A. (1970). The market for lemons. <em>The Quarterly Journal of Economics</em>, 84(3), 488-500.</p>
            <p class="ref-entry">Bain, J. S. (1956). <em>Barriers to new competition</em>. Harvard University Press.</p>
            <p class="ref-entry">Brammer, S., &amp; Walker, H. (2011). Sustainable procurement in the public sector. <em>IJOPM</em>, 31(4), 452-476.</p>
            <p class="ref-entry">Breiman, L. (2001). Random forests. <em>Machine Learning</em>, 45(1), 5-32.</p>
            <p class="ref-entry">Coase, R. H. (1937). The nature of the firm. <em>Economica</em>, 4(16), 386-405.</p>
            <p class="ref-entry">Doshi-Velez, F., &amp; Kim, B. (2017). Towards a rigorous science of interpretable machine learning. <em>arXiv:1702.08608</em>.</p>
            <p class="ref-entry">Edler, J., &amp; Georghiou, L. (2007). Public procurement and innovation. <em>Research Policy</em>, 36(7), 949-963.</p>
            <p class="ref-entry">Flynn, A., &amp; Davis, P. (2014). Theory in public procurement research. <em>JOPP</em>, 14(2), 139-180.</p>
            <p class="ref-entry">Georghiou, L., Edler, J., Uyarra, E., &amp; Yeow, J. (2013). Policy instruments for PPI. <em>TFSC</em>, 81, 1-12.</p>
            <p class="ref-entry">Grandia, J., &amp; Voncken, D. (2019). Sustainable public procurement. <em>Sustainability</em>, 11(19), 5215.</p>
            <p class="ref-entry">Gregor, S., &amp; Hevner, A. R. (2013). Positioning design science research. <em>MIS Quarterly</em>, 37(2), 337-355.</p>
            <p class="ref-entry">Hevner, A. R., March, S. T., Park, J., &amp; Ram, S. (2004). Design science in IS research. <em>MIS Quarterly</em>, 28(1), 75-105.</p>
        </div>
        <div class="page-footer">22</div>
    </section>

    <section class="paper-page">
        <div class="page-content">
            <p class="ref-entry">Jensen, M. C., &amp; Meckling, W. H. (1976). Theory of the firm. <em>JFE</em>, 3(4), 305-360.</p>
            <p class="ref-entry">Lei n. 13.709/2018. Lei Geral de Protecao de Dados Pessoais (LGPD).</p>
            <p class="ref-entry">Lei n. 14.133/2021. Lei de Licitacoes e Contratos Administrativos.</p>
            <p class="ref-entry">Lei Complementar n. 182/2021. Marco Legal das Startups.</p>
            <p class="ref-entry">Liu, F. T., Ting, K. M., &amp; Zhou, Z. H. (2008). Isolation forest. <em>IEEE ICDM</em>, 413-422.</p>
            <p class="ref-entry">Lundberg, S. M., &amp; Lee, S.-I. (2017). Interpreting model predictions. <em>NeurIPS</em>, 30, 4765-4774.</p>
            <p class="ref-entry">Mazzucato, M. (2014). <em>The entrepreneurial state</em>. Anthem Press.</p>
            <p class="ref-entry">Peffers, K. et al. (2007). A design science research methodology. <em>JMIS</em>, 24(3), 45-77.</p>
            <p class="ref-entry">Rainville, A. (2021). Circular economy through public procurement. <em>Research Policy</em>, 50(4).</p>
            <p class="ref-entry">Testa, F. et al. (2014). Green public procurement. <em>JCP</em>, 112, 1893-1900.</p>
            <p class="ref-entry">Thai, K. V. (2001). Public procurement re-examined. <em>JOPP</em>, 1(1), 9-50.</p>
            <p class="ref-entry">Uyarra, E., &amp; Flanagan, K. (2010). Innovation impacts of public procurement. <em>EPS</em>, 18(1), 123-143.</p>
        </div>
        <div class="page-footer">23</div>
    </section>

    <section class="paper-page">
        <div class="page-content">
            <p class="ref-entry">Vaidya, K., Sajeev, A. S. M., &amp; Callender, G. (2006). E-procurement implementation success. <em>JOPP</em>, 6(1-2), 70-99.</p>
            <p class="ref-entry">Wachter, S., Mittelstadt, B., &amp; Russell, C. (2017). Counterfactual explanations. <em>Harvard JLT</em>, 31(2), 841-887.</p>
            <p class="ref-entry">Williamson, O. E. (1985). <em>The economic institutions of capitalism</em>. Free Press.</p>
            <p class="ref-entry">Witjes, S., &amp; Lozano, R. (2016). Towards a more circular economy. <em>RCR</em>, 112, 37-44.</p>
            <p class="ref-entry">Johnson, P. F., Leenders, M. R., &amp; McCue, C. (2017). Purchasing organizational roles. <em>JOPP</em>, 3(1), 57-74.</p>
            <p class="ref-entry">Bain, J. S. (1956). <em>Barriers to new competition</em>. Harvard University Press.</p>
        </div>
        <div class="page-footer">24</div>
    </section>
'''

# Assemble all parts
full = pre.rstrip('</body>\n</html>')
full += '\n' + art01_body + '\n'
full += '\n' + art02_body + '\n'
full += ch4_5_refs
full += '\n</body>\n</html>'

# Remove all travessoes and em-dashes
full = full.replace("&mdash;", "").replace("\u2014", "").replace("\u2013", "")

# Re-acentuar
for ascii_word, accented_word in MAPA_ACENTOS.items():
    pattern = re.compile(r'\b' + re.escape(ascii_word) + r'\b', re.IGNORECASE)
    full = pattern.sub(accented_word, full)

with open(THESIS, "w", encoding="utf-8") as f:
    f.write(full)

# Stats
size = os.path.getsize(THESIS)
with open(THESIS, encoding="utf-8") as f:
    c = f.read()
dashes = c.count("\u2014") + c.count("&mdash;")
pages = c.count("page-footer")
tables = c.count("<table>")
refs = c.count("ref-entry")
h2s = re.findall(r'<h2>([^<]+)</h2>', c)
h3s = re.findall(r'<h3>([^<]+)</h3>', c)

print(f"Tese: {size/1024:.0f}KB | {dashes} trav | {pages} pgs | {tables} tabs | {refs} refs")
print(f"h2: {len(h2s)} | h3: {len(h3s)}")
print("\n=== ESTRUTURA ===")
for h in h2s:
    print(f"  {h}")
