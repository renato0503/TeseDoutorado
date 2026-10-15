# Cerrado Tech - PubliCopilot Landing Page

Esta branch (`gh-pages`) serve a landing page institucional da Cerrado Tech.

- URL publica: https://renato0503.github.io/TeseDoutorado/
- Codigo-fonte: `index.html` (CSS + JS + SVGs embutidos, sem build step)
- Stack: HTML5 + CSS3 + JavaScript vanilla, GitHub Pages

Desenvolvido por **Renato de Oliveira Rosa** (Fucape Business School).

## Estrutura

- `index.html` - landing page completa (hero, modulos, metricas, consultoria, processo, CTA, footer)
- `.nojekyll` - desativa processamento Jekyll do GitHub Pages
- `README.md` - este arquivo

A branch `main` contem o codigo-fonte original em `landing/index.html`. Esta branch
(`gh-pages`) e regenerada manualmente a cada atualizacao:

```bash
git switch main
git switch --orphan gh-pages
git clean -fdx
git show main:landing/index.html > index.html
git add .
git commit -m "Atualiza landing"
git push -u origin gh-pages --force
git switch main
```
