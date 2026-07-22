"""
Reconstroi a tese mantendo a estrutura HTML intacta dos artigos.
Insere apenas chapter headers antes de cada artigo, sem modificar o conteudo.
"""
import re, sys
sys.path.insert(0, r"C:\Users\Renato\Documents\Doutorado\scripts")
from reacentuar_artigo import MAPA_ACENTOS

THESIS = r"C:\Users\Renato\Documents\Doutorado\Tese\tese_draft.html"
ART01 = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\01-Artigo-Cientifico-Diagnostico\artigo_01_diagnostico.html"
ART02 = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\02-Artigo-Tecnologico-Copiloto\artigo_02_tecnologico.html"

# Read pre-textual part (capa through sumario) from current thesis
with open(THESIS, "r", encoding="utf-8") as f:
    old_thesis = f.read()

# Extract pre-textual: everything up to Chapter 1
ch1_marker = '<h2>1 INTRODUÇÃO GERAL</h2>'
pre_end = old_thesis.find(ch1_marker)
pre = old_thesis[:pre_end] if pre_end > 0 else ""

# Extract Chapter 1 content and Chapters 4-5 from old thesis
ch1_start = old_thesis.find(ch1_marker)
ch4_marker = '<h2>4 O PRODUTO: COPILOTO ALGORITMICO</h2>'
ch4_start = old_thesis.find(ch4_marker)
if ch4_start < 0:
    ch4_marker = '<h2>4 O PRODUTO: COPILOTO ALGORÍTMICO</h2>'
    ch4_start = old_thesis.find(ch4_marker)

ch1_content = old_thesis[ch1_start:ch4_start] if ch4_start > ch1_start else ""

# Extract Chapters 4-5-Refs
ch4_plus = old_thesis[ch4_start:] if ch4_start > 0 else ""

# Remove </body></html> from pre and ch4_plus
pre = re.sub(r'</body>\s*</html>', '', pre)
ch4_plus = re.sub(r'</body>\s*</html>', '', ch4_plus)

# Read articles
with open(ART01, "r", encoding="utf-8") as f:
    art01 = f.read()
with open(ART02, "r", encoding="utf-8") as f:
    art02 = f.read()

# Extract body from articles (keep structure INTACT)
art01_body = art01.split("<body>")[1].split("</body>")[0]
art02_body = art02.split("<body>")[1].split("</body>")[0]

# Remove ONLY the control panel from articles (floating button, not content)
art01_body = re.sub(r'<div class="control-panel no-print">.*?</div>', '', art01_body, flags=re.DOTALL)
art02_body = re.sub(r'<div class="control-panel no-print">.*?</div>', '', art02_body, flags=re.DOTALL)

# Remove abstract boxes from articles (thesis has its own)
art01_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art01_body, flags=re.DOTALL)  # 2nd one (EN)
art02_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<div class="abstract-box">.*?</div>', '', art02_body, flags=re.DOTALL)

# Remove h1 title and author info from articles
art01_body = re.sub(r'<h1 class="paper-title">.*?</h1>', '', art01_body, flags=re.DOTALL)
art01_body = re.sub(r'<p class="author-info">.*?</p>', '', art01_body, flags=re.DOTALL)
art02_body = re.sub(r'<h1 class="paper-title">.*?</h1>', '', art02_body, flags=re.DOTALL)
art02_body = re.sub(r'<p class="author-info">.*?</p>', '', art02_body, flags=re.DOTALL)

# Remove article-level REFERENCIAS section (thesis has consolidated)
art01_body = re.sub(r'<section class="paper-page">\s*<div class="page-content">\s*<h2>REFERÊNCIAS</h2>.*?</section>', '', art01_body, flags=re.DOTALL)
art02_body = re.sub(r'<section class="paper-page">\s*<div class="page-content">\s*<h2>REFERÊNCIAS</h2>.*?</section>', '', art02_body, flags=re.DOTALL)

# Renumber sections within articles
# Article 01 h2: 1->2.1, 2->2.2, 3->2.3, 4->2.4, 5->2.5
for old, new in [('1 INTRODUÇÃO','2.1 Introdução'),('2 REFERENCIAL TEÓRICO','2.2 Referencial Teórico'),
    ('3 METODOLOGIA','2.3 Metodologia'),('4 RESULTADOS E DISCUSSÃO','2.4 Resultados e Discussão'),
    ('5 CONCLUSÃO','2.5 Conclusão')]:
    art01_body = art01_body.replace(f'<h2>{old}</h2>', f'<h2>{new}</h2>')

# Article 02 h2: 1->3.1, 2->3.2, 3->3.3, 4->3.4, 5->3.5
for old, new in [('1 INTRODUÇÃO','3.1 Introdução'),('2 METODOLOGIA DE DESENVOLVIMENTO','3.2 Metodologia de Desenvolvimento'),
    ('3 ARQUITETURA DO PRODUTO','3.3 Arquitetura do Produto'),('4 AVALIAÇÃO E TESTES DE DESEMPENHO','3.4 Avaliação e Testes de Desempenho'),
    ('5 CONCLUSÕES TECNOLÓGICAS','3.5 Conclusões Tecnológicas')]:
    art02_body = art02_body.replace(f'<h2>{old}</h2>', f'<h2>{new}</h2>')

# Renumber h3 in articles
for body, prefix in [(art01_body, '2.'), (art02_body, '3.')]:
    # 2.1 -> prefix+2.1,  3.1 -> prefix+3.1,  4.1 -> prefix+4.1
    pass  # Keep h3 as-is for now - they're already under the correct h2

# Add chapter header section before each article
ch2_header = '''
    <section class="paper-page">
        <div class="page-content">
            <h2>2 DIAGNÓSTICO EMPÍRICO DAS COMPRAS COMPLEXAS</h2>
            <p style="text-align:center;font-size:10pt;color:#555;margin-bottom:0.3cm;">Capítulo baseado no Artigo 1 — Determinantes do Sucesso e Fracasso em Compras Públicas Complexas</p>
        </div>
        <div class="page-footer">5</div>
    </section>
'''

ch3_header = '''
    <section class="paper-page">
        <div class="page-content">
            <h2>3 COPILOTO ALGORÍTMICO: DESENVOLVIMENTO E VALIDAÇÃO</h2>
            <p style="text-align:center;font-size:10pt;color:#555;margin-bottom:0.3cm;">Capítulo baseado no Artigo 2 — Desenvolvimento de um Copiloto Algorítmico Baseado em XAI</p>
        </div>
        <div class="page-footer">13</div>
    </section>
'''

# Assemble
full = pre + '\n' + ch1_content + '\n'
full += ch2_header + '\n' + art01_body + '\n'
full += ch3_header + '\n' + art02_body + '\n'
full += ch4_plus + '\n'

# Final cleanup
full = full.replace("&mdash;", "").replace("\u2014", "").replace("\u2013", "")
full = re.sub(r'</body>\s*</html>', '', full)
full += '\n</body>\n</html>'

# Re-acentuar
for ascii_word, accented_word in MAPA_ACENTOS.items():
    pattern = re.compile(r'\b' + re.escape(ascii_word) + r'\b', re.IGNORECASE)
    full = pattern.sub(accented_word, full)

with open(THESIS, "w", encoding="utf-8") as f:
    f.write(full)

# Verify HTML structure
import os
size = os.path.getsize(THESIS)
with open(THESIS, encoding="utf-8") as f:
    c = f.read()
sections = c.count("<section")
divs_open = c.count("<div")
divs_close = c.count("</div>")
dashes = c.count("\u2014") + c.count("&mdash;")
pages = c.count("page-footer")
tables = c.count("<table>")
refs = c.count("ref-entry")
h2_count = c.count("<h2>")
print(f"Tese: {size/1024:.0f}KB | {sections} sections | divs: {divs_open}/{divs_close} | {dashes} trav | {pages} pgs | {tables} tabs | {refs} refs | {h2_count} h2")
print(f"Div balance: {'OK' if abs(divs_open - divs_close) < 5 else 'UNBALANCED!'}")
