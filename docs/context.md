# Contexto do Projeto - Tese de Doutorado

**Última atualização:** 25 de Julho de 2026 23h — v2.1: código 100% pronto. Cloud Function: build falha — compute SA sem permissão Artifact Registry. Pendente: `artifactregistry.reader` + redeploy.

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

| # | Entregável | Estado (23/07/2026) |
|---|------------|---------------------|
| 1 | **Artigo 1 — Diagnóstico Empírico** (PNCP) | ✅ **100% PRONTO** para submissão Qualis A |
| 2 | **Artigo 2 — Artigo Tecnológico** (Copiloto) | ✅ FINALIZADO (18/07/2026) |
| 3 | **Produto — MVP Funcional** (Firebase) | ⚠️ **v2.1** — Código 100% pronto. Cloud Function: build falha (Artifact Registry). Pendente: add permissão + redeploy |
| 4 | **Tese Completa** (`Tese/tese_draft.html`) | ✅ Estruturada com 3 artigos (23/07/2026) |

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
| Front-end (Hosting) | 🟢 Online | Módulos avaliação + geração + dashboard admin |
| Cloud Function `analisar_minuta` | 🟢 **v14 deployada** | NVIDIA_API_KEY configurada, 512MB/120s timeout |
| API `/api/analisar` | ❌ Build falha — sem deploy | Artifact Registry: compute SA sem `artifactregistry.repositories.downloadArtifacts` |
| NVIDIA IA | 🟢 Integrada | `meta/llama-3.3-70b-instruct` para geração de editais |
| Modelos ML | 🟢 11 arquivos, 27,35 MB | Random Forest + SHAP + Isolation Forest |
| XSS | 🟢 Sanitizado | 15 innerHTML → DOM methods |
| Rate limiting | 🟢 Implementado | 30 req/min por usuário |
| Segurança headers | 🟢 Configurados | X-Frame-Options, X-Content-Type-Options |

### 4 Tarefas de Qualidade Concluídas (19/07/2026 07h)

1. ✅ **Métricas honestas**: Acc + AUC + F1 com nota de desbalanceamento (1,99% positivos)
2. ✅ **CORS restrito**: Whitelist `comprapublica.web.app` (não mais `*`)
3. ✅ **Limpeza de modelos**: -12,17 MB removidos (4 arquivos duplicados)
4. ✅ **requirements.txt**: scikit-learn==1.9.0 fixado (evita InconsistentVersionWarning)

### Pendências Críticas

1. **Permissão Artifact Registry + redeploy** (rodar como `comercial@cerradofinancas.com.br`):
```powershell
cd C:\Users\Renato\Documents\Doutorado\PubliCopilot
gcloud config set account comercial@cerradofinancas.com.br
gcloud artifacts repositories add-iam-policy-binding gcf-artifacts --location=us-central1 --project=publicopilot --member=serviceAccount:432118179013-compute@developer.gserviceaccount.com --role=roles/artifactregistry.reader
gcloud functions deploy analisar_minuta --runtime python311 --trigger-http --allow-unauthenticated --project publicopilot --region us-central1 --source=functions --entry-point=analisar_minuta --memory=512MB --timeout=120s --set-env-vars NVIDIA_API_KEY=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
```

2. **Firebase hosting deploy:**
```powershell
firebase login
firebase deploy --only hosting
```

3. **Permissão IAM allUsers** para acesso direto à URL da função (se necessário)

4. **Permissão Storage Object Viewer** para o compute SA no bucket gcf-sources (se o passo 1 nao resolver):
```powershell
gsutil iam ch serviceAccount:432118179013-compute@developer.gserviceaccount.com:objectViewer gs://gcf-sources-432118179013-us-central1
```

3. **Expandir `tese_draft.html`** com conteúdo integral dos artigos

4. **Gerar PDF da tese** para submissão à banca

5. **Opicionais:** Testes unitários (D1/D2), reCAPTCHA v3 (B3), página de histórico (F2), relatório PDF (F4)

---

## Tese Completa (tese_draft.html)

**Arquivo:** `Tese/tese_draft.html`
**Tamanho:** 790 linhas, 61 KB
**Estrutura:** 6 capítulos + pre-textual + referências + apêndices
**Modelo:** Segue a estrutura do `Tese-Joao-Eudes-Bezerra.pdf` (tese Fucape com 3 artigos)

| Capítulo | Conteúdo |
|----------|----------|
| Pré-textual | Capa, Folha de Rosto, Aprovação, Epígrafe, Dedicatória, Resumo, Abstract, Listas, Sumário |
| 1 | Introdução Geral (contexto, problema, justificativa, objetivos, estrutura) |
| 2 | Fundamentação Teórica Geral (ECT, Estado Empreendedor, Transparência Algorítmica, DSR) |
| 3 | Artigo 1 — Diagnóstico Empírico (OR=1,71, Cox HR=1,85, Gini=0,89) |
| 4 | Artigo 2 — Copiloto Algorítmico XAI (AUC-ROC=90,83%, F1=26,39%) |
| 5 | Produto — PubliCopilot v1.3 (arquitetura Firebase, ML, segurança, roadmap) |
| 6 | Considerações Finais (contribuições, limitações, pesquisas futuras) |
| Pós-textual | Referências (21 obras) + Apêndices A (Protocolo TAM) e B (TCLE) |

## Arquivos-Chave (23/07/2026)

| Arquivo | Função |
|---------|--------|
| `novo.imp.md` | Controle geral de implementação |
| `Tese/tese_draft.html` | Tese completa com 3 artigos (790 linhas) |
| `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/artigo_01_diagnostico.html` | Artigo 1 (HTML) |
| `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/dados/figuras/fig[1-7]_*.svg` | 7 figuras SVG |
| `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/dados/resultados_reais.json` | Outputs da regressão real |
| `PubliCopilot/functions/main.py` | Cloud Function |
| `PubliCopilot/functions/models/saved/` | 11 modelos ML |
| `PubliCopilot/public/` | Front-end (deployado) |
| `PubliCopilot/functions/models/nvidia_client.py` | Cliente NVIDIA API (novo v2.1) |
| `PubliCopilot/public/data/counterfactual_templates.json` | Templates contrafactuais (asset estático) |
| `PubliCopilot/limpar_modelos.py` | Script de limpeza (manutenção) |
| `erros_firebase.md` | Histórico de erros Firebase |
| `imp.produto.md` | Controle específico do Produto |

---

## Repositório Git

Renato de Oliveira Rosa — Fucape Business School
Documentação centralizada em `novo.imp.md` e `docs/`
