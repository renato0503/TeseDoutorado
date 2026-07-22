"""
Embed figures as base64 data URIs in the article HTML.
Solves: file:// security origin blocking cross-directory image loading.
"""
import base64
import re
from pathlib import Path

ARTIGO = Path("C:/Users/Renato/Documents/Doutorado/Tese/artigos_tese/02-Artigo-Tecnologico-Copiloto/artigo_02_tecnologico.html")
html = ARTIGO.read_text(encoding="utf-8")

def path_to_data_uri(fig_path: Path) -> str:
    ext = fig_path.suffix.lower().lstrip(".")
    mime = f"image/{ext}"
    data = fig_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"

count = 0
def fig_replacer(m):
    global count
    rel = m.group(1)
    fig_path = Path("C:/Users/Renato/Documents/Doutorado/docs/figuras") / Path(rel).name
    if not fig_path.exists():
        print(f"  ⚠️ NOT FOUND: {fig_path}")
        return m.group(0)
    uri = path_to_data_uri(fig_path)
    count += 1
    print(f"  ✅ [{count}] {fig_path.name} ({len(uri):,} chars)")
    return f'<img src="{uri}"'

html_new = re.sub(r'<img src="([^"]+)"', fig_replacer, html)
ARTIGO.write_text(html_new, encoding="utf-8")
print(f"\n✅ Article saved with {count} embedded images.")
