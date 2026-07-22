# Contexto do Projeto - Tese de Doutorado

**Última atualização:** 19 de Julho de 2026 07h

---

## Visão Geral do Projeto

**Tema:** Copiloto Algorítmico para Compras Públicas Complexas: Um Artefato de Apoio à Decisão para Redução de Assimetrias na Contratação de Inovação e Sustentabilidade

**Pesquisador:** Renato de Oliveira Rosa
**Orientador:** Prof. Dr. Olavo Venturim Caldas
**Programa:** Fucape Business School - Doutorado em Contabilidade
**Metodologia:** Design Science Research (DSR)

---

## Modelo Fucape de 3 Entregáveis

A tese foi pivotada do modelo original de 25 artigos para o **Modelo Fucape de 3 Entregáveis**:

| # | Entregável | Estado (19/07/2026) |
|---|------------|---------------------|
| 1 | **Artigo 1 — Diagnóstico Empírico** (PNCP) | ✅ **100% PRONTO** para submissão Qualis A |
| 2 | **Artigo 2 — Artigo Tecnológico** (Copiloto) | ✅ FINALIZADO (18/07/2026) |
| 3 | **Produto — MVP Funcional** (Firebase) | ⚠️ Front-end online, back-end em deploy |

---

## Artigo 1: Determinantes do Sucesso e Fracasso em Compras Públicas Complexas

**Arquivo:** `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/artigo_01_diagnostico.html`
**Tamanho:** 71,8 KB, 334 linhas
**Subseções:** 18 (2.1-2.7, 3.1-3.6, 4.1-4.5)
**Referências:** 44 (incluindo Williamson 1979, Simon 1947, Mazzucato 2018)

### 5 Problemas Críticos Resolvidos

| # | Problema | Solução |
|---|----------|---------|
| 1 | OVB (Variável Omitida) | Modelos sequenciais 1-2-3 com GLMM + LR test |
| 2 | Ilusão n=26 fornecedores | CNPJs truncados 7-8 dígitos documentados |
| 3 | Tautologia da VD | VD ex-post pura + Cox + PSM + GLMM |
| 4 | Validação NLP | Protocolo 200+200 + métricas P/R/F1 |
| 5 | Conclusão prematura | Termo interação + Racionalidade Limitada (Simon, 1947) |

### Dados Reais Integrados (n=73.201 pós-filtro)

| Estatística | Valor Real |
|------------|------------|
| OR is_complexa | **1,708** (IC: 1,55-1,88) |
| OR vigencia_log | **1,482** (IC: 1,40-1,57) |
| OR valor_log | **1,201** (IC: 1,18-1,22) |
| HR Cox (is_complexa) | **1,850** |
| Taxa base complexas | **4,48%** |
| Taxa base normais | **1,93%** |
| OR bruto | **2,382** |
| ATT PSM | **+0,90 pp** |
| Pseudo R² | 0,062 |
| AUC-ROC | 0,697 |

### 15 Elementos Visuais (Numerados 1-7)

- 1 Quadro sintético (Quadro 1)
- 7 Tabelas (T1-T7)
- 7 Figuras SVG (Fig 1-7)

---

## Artigo 2: Artigo Tecnológico (Copiloto)

**Status:** FINALIZADO (18/07/2026)
- Acurácia: 93,36% | AUC-ROC: 90,83% | F1-Score: 26,39%
- 412+ linhas, métricas remediadas, contrafactuais normativos

---

## Produto (Copiloto Algorítmico)

**URL Pública:** https://comprapublica.web.app

| Componente | Status | Detalhe |
|------------|--------|---------|
| Front-end (Hosting) | 🟢 Online | 3 páginas HTML + tema |
| Cloud Function `analisar_minuta` | ⚠️ **Em deploy** | Bloqueio: autorização interativa |
| API `/api/analisar` | ⚠️ 404 | Roteada para function inexistente |
| Modelos ML | 🟢 11 arquivos, 27,35 MB | Limpos em 19/07/2026 |

### 4 Tarefas de Qualidade Concluídas (19/07/2026 07h)

1. ✅ **Métricas honestas**: Acc + AUC + F1 com nota de desbalanceamento (1,99% positivos)
2. ✅ **CORS restrito**: Whitelist `comprapublica.web.app` (não mais `*`)
3. ✅ **Limpeza de modelos**: -12,17 MB removidos (4 arquivos duplicados)
4. ✅ **requirements.txt**: scikit-learn==1.9.0 fixado (evita InconsistentVersionWarning)

### Pendência Crítica

**Cloud Function `analisar_minuta` precisa ser deployada** no terminal do usuário:
```bash
cd C:\Users\Renato\Documents\Doutorado\PubliCopilot
firebase deploy --only functions --project publicopilot-aa662
```

---

## Arquivos-Chave (19/07/2026)

| Arquivo | Função |
|---------|--------|
| `novo.imp.md` | Controle geral de implementação |
| `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/artigo_01_diagnostico.html` | Artigo 1 (HTML) |
| `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/dados/figuras/fig[1-7]_*.svg` | 7 figuras SVG |
| `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/dados/resultados_reais.json` | Outputs da regressão real |
| `PubliCopilot/functions/main.py` | Cloud Function |
| `PubliCopilot/functions/models/saved/` | 11 modelos ML |
| `PubliCopilot/public/` | Front-end (deployado) |
| `PubliCopilot/limpar_modelos.py` | Script de limpeza (manutenção) |
| `erros_firebase.md` | Histórico de erros Firebase |
| `imp.produto.md` | Controle específico do Produto |

---

## Repositório Git

Renato de Oliveira Rosa — Fucape Business School
Documentação centralizada em `novo.imp.md` e `docs/`
