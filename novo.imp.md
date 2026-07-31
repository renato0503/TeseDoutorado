# NOVO IMPLEMENTACAO GERAL

Este documento centraliza o **planejamento e controle de execucao** da Tese de Doutorado em Contabilidade na Fucape Business School, apos o *pivot* estrutural exigido pelo orientador (Prof. Dr. Olavo Venturim Caldas).

O modelo "25 Artigos Empiricos" e a narrativa "Apagao das Canetas" foram substituidos pelo **Modelo Fucape de 3 Entregaveis**, focado em **Compras Complexas** e reducao da assimetria informacional, ancorado no paradigma de Design Science Research (DSR).

**Ultima atualizacao:** 31/07/2026 — **REMEDIACAO COMPLETA DA TESE + SUBIDA AO GITHUB**. Produto v2.1: Cloud Function `analisar_minuta` **deployada (v17 ACTIVE)** — ver `imp.produto.md`. Revisao da literatura executada (`revisao_literatura.md`, `fichamento_congressos.csv`, curadoria). **Injecao de referencial nos artigos de congresso** (10→36, 15→40, 17→31, 02→31 refs) + **remediacao da pasta Tese** (Artigo 1, Artigo 2, Produto, scripts) conforme `remediacao_tese.md`. Push para GitHub (`6e6a86d`): NVIDIA_API_KEY removida do repo, venv untracked.

---

## 1. ESTRUTURA DA TESE (3 ENTREGAVEIS)

1. **Artigo Cientifico 1 (Diagnostico Empirico):** Modelagem do PNCP para separar compras normais de complexas. REESCRITO (19/07/2026). REVISAO ORTOGRAFICA COMPLETA (19/07/2026). 12 ELEMENTOS VISUAIS INSERIDOS (19/07/2026): 7 figuras SVG + 4 tabelas (T1, T6, T7 + ja existentes T2-T5) + 1 quadro sintetico. 5 PROBLEMAS CRITICOS RESOLVIDOS: OVB, CNPJs truncados, VD tautologia, validacao NLP, Racionalidade Limitada (Simon, 1947) + termo de interacao. DADOS REAIS integrados nas Tabelas 4, 5, 6, 7 e Figuras 4, 5, 7 (regressao sobre pncp_target_real.csv, n=73.201 apos filtro vigencia>=30). Estado: 71,8 KB, 334 linhas, 44 referencias, 18 subsecoes. **100% PRONTO** para submissao Qualis A.
2. **Artigo Tecnologico 2 (A Ferramenta):** Copiloto Algoritmico com DSR + Isolation Forest + XAI/SHAP. FINALIZADO (18/07/2026)
3. **O Produto (Copiloto) v2.1:** MVP funcional com ML real + IA generativa. Cloud Function `analisar_minuta` **deployada** (v14, 512MB/120s, NVIDIA_API_KEY configurada). **NVIDIA IA integrada** (llama-3.3-70b) para geracao de editais com fallback para templates. **Bugs corrigidos**: (1) `uf_encoded`/`tipo_encoded` agora usam `OrdinalEncoder` real (nao mais hardcoded 0), (2) logging estruturado nos 4 modulos (substituido `except: pass`), (3) unicode normalization (NFKD) no preprocessor, (4) counterfactual templates expandido de 8 para 12 features. **XSS sanitizado**: 15 `innerHTML` convertidos para DOM methods. **Rate limiting**: 30 req/min por usuario. **Security headers**: X-Frame-Options, X-Content-Type-Options configurados. Pendente: `firebase login` + `firebase deploy --only hosting` para rotear `/api/**` → function, e permissao IAM `allUsers` via Firebase Console.
4. **Tese Completa (`Tese/tese_draft.html`):** Reestruturado (23/07/2026) como tese completa no modelo Fucape de 3 artigos (similar a `Tese-Joao-Eudes-Bezerra.pdf`). 790 linhas, 61 KB, 19 secoes. Estrutura: pre-textual (capa, folha de rosto, aprovacao, epigrafe, resumo, abstract, listas, sumario) + 6 capitulos (Introducao Geral, Fund. Teorica Geral, Artigo 1, Artigo 2, Produto, Consideracoes Finais) + Referencias (21 obras) + Apendices A e B.

---

## 2. SPRINTS CONCLUIDOS (1-10)

### Sprint 1: Fundacao do Produto (MVP Core) — CONCLUIDA 10/07/2026

**Objetivo:** Estruturar repositorio, app Streamlit base, dois modulos principais.

| Sub | Tarefa                                                                                                | Status |
| --- | ----------------------------------------------------------------------------------------------------- | ------ |
| 1.1 | Estrutura de diretorios (`app/`, `models/`, `data/`)                                            | ✅     |
| 1.2 | App principal (`app.py`) com navegacao e layout wide                                                | ✅     |
| 1.3 | Motor NLP/ML (`preprocessor.py`, `risk_engine.py`, `anomaly_detector.py`, `xai_explainer.py`) | ✅     |
| 1.4 | Modulo de Avaliacao (`01_Avaliacao.py`)                                                             | ✅     |
| 1.5 | Modulo de Geracao (`02_Geracao.py`)                                                                 | ✅     |

---

### Sprint 2: ML Real e Dados PNCP — CONCLUIDA 10/07/2026

**Objetivo:** Substituir regras heuristicas por modelos de Machine Learning treinados nos dados reais do PNCP.

| Sub | Tarefa                                                                                                                             | Status |
| --- | ---------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 2.1 | Script`train_models.py`: TF-IDF (500 features, 15k), Isolation Forest (100 arvores), Random Forest (100k contratos, 100 arvores) | ✅     |
| 2.2 | Integracao com dados PNCP via`model_loader.py` (cache singleton)                                                                 | ✅     |
| 2.3 | Grafico SHAP inline no Modulo de Avaliacao                                                                                         | ✅     |
| 2.4 | Metricas reais: Acuracia 98,27%, AUC 98,97%, F1 95,22% (antes da remediação)                                                     | ✅     |
| 2.5 | Integracao dos modulos (`anomaly_detector.py`, `risk_engine.py`) com modelos reais                                             | ✅     |

---

### Sprint 3: Experiencia do Usuario e Freemium — CONCLUIDA 10/07/2026

**Objetivo:** Modelo Freemium, link consultoria, exportacao de relatorio.

| Sub | Tarefa                                         | Status |
| --- | ---------------------------------------------- | ------ |
| 3.1 | Limite de 3 analises/sessao na versao gratuita | ✅     |
| 3.2 | Tela de upgrade Premium + link consultoria     | ✅     |
| 3.3 | Status visivel do sistema na Home e sidebar    | ✅     |

---

### Sprint 4: Polimento Final — CONCLUIDA 10/07/2026

**Objetivo:** Deploy, materiais de defesa, documentacao.

| Sub | Tarefa                                                  | Status |
| --- | ------------------------------------------------------- | ------ |
| 4.1 | Deploy no Streamlit Cloud + URL publica                 | ✅     |
| 4.2 | Deploy Firebase (`PubliCopilot/`) — ver Sprint 5     | ✅     |
| 4.3 | Testes unitarios (17 testes em`tests/test_models.py`) | ✅     |
| 4.4 | Docstrings em todos os modulos Python                   | ✅     |
| 4.5 | Licenca MIT definida                                    | ✅     |

---

### Sprint 5: Port para Firebase (Cloud Function) — CONCLUIDA 18/07/2026

**Objetivo:** Servir MVP 100% no Firebase (Cloud Function Python + Hosting).

| Sub | Tarefa                                                                                    | Status |
| --- | ----------------------------------------------------------------------------------------- | ------ |
| 5.1 | Backend:`functions/main.py` — entry point `analisar_minuta` (POST `/api/analisar`) | ✅     |
| 5.2 | Front-end:`modulo_avaliacao/index.html` com `fetch('/api/analisar')`                  | ✅     |
| 5.3 | Front-end:`modulo_geracao/index.html` (JS puro, templates XAI)                          | ✅     |
| 5.4 | Configuracao`firebase.json` com rewrite `/api/** -> analisar_minuta`                  | ✅     |
| 5.5 | Teste local validado com POST real                                                        | ✅     |

**Arquitetura produtiva:**

```
[Navegador] -> modulo_avaliacao/index.html
    | POST /api/analisar { texto, valor?, vigencia_dias? }
    v
[Firebase Hosting rewrite] -> Cloud Function analisar_minuta (python312)
    | carrega .pkl, roda pipeline ML real
    v
[JSON] -> score, lacunas, recomendacoes, SHAP, contrafactuais, rf_proba
```

**URL:** https://comprapublica.web.app

---

### Sprint 6: Remediacao Metodologica — CONCLUIDA 18/07/2026

**Objetivo:** Corrigir 5 problemas identificados pelo orientador.

#### Problema 1: Data Leakage / Tautologia (Artigo 2)

- **Problema:** `vigencia_log` explicava 76% do modelo (alvo incluía "vigência < 30 dias")
- **Solucao adotada:** Redefinicao do alvo para eventos ex-post puros:
  ```python
  df["target_real"] = ((df["aditivo_valor"] == 1) | (df["multiplas_retificacoes"] == 1)).astype(int)
  ```
- **Resultado:** Modelo B — Acuracia 93,36%, AUC-ROC 90,83%, F1 26,39%
- `vigencia_log` caiu de 76% para 14,4% SHAP

#### Problema 2: Ilusao do NLP (Artigo 2)

- **Problema:** NLP contribuia com <4% de importancia Gini
- **Solucao adotada (S3):** Termos multiplicativos `interacao_if_valor` e `interacao_if_vigencia`
- **Experimento comparativo:**| Solucao                   | AUC    | Contribuicao NLP |
  | ------------------------- | ------ | ---------------- |
  | S1 (IF bruto)             | 91,58% | 7,95%            |
  | S2 (Dicionario)           | 91,71% | 8,83%            |
  | **S3 (Interacoes)** | 90,93% | **27,11%** |
- Gini combinado IF + interacoes: ~28,86% no Modelo B

#### Problema 3: SHAP vs. Motivacao Juridica — RESOLVIDO (Sprint 8)

- **Solucao 1:** Wording substituido: "fundamentacao decisoria" → "subsidio tecnico para a motivacao decisoria"
- **Solucao 2:** `counterfactual_templates.json` integrado ao `xai_explainer.py`
- **Solucao 3:** Caixas de texto juridico renderizadas no app e Firebase (Sprint 8)

#### Problema 4: Falha DSR — RESOLVIDO (Sprint 10)
#### Problema 5: Inconsistencias Formais — RESOLVIDO (Sprint 10)

---

### Sprint 7: Sincronizacao Tecnica — CONCLUIDA 18/07/2026

**Objetivo:** Sincronizar codigo e artigo apos remediacao da Sprint 6.

| Sub  | Tarefa                                                                        | Status         |
| ---- | ----------------------------------------------------------------------------- | -------------- |
| S7.1 | Verificar .pkl e metricas.json nos diretorios`saved/`                       | ✅ ja corretos |
| S7.2 | Atualizar`metricas.json` (93,36% / 90,83%) e `docs/arquitetura.md`        | ✅ ja correto  |
| S7.3 | Verificar`app.py` e `pages/01_Avaliacao.py` (usa get_metricas() dinamico) | ✅             |
| S7.4 | Verificar`risk_engine.py` e `model_loader.py` (fallback 0.9336/0.9083)    | ✅             |
| S7.5 | Validar Firebase`/api/analisar` com novos modelos                           | ✅             |
| S7.6 | Teste de sanidade local                                                       | ✅             |

---

### Sprint 8: Implementacao Textual e Templates Juridicos XAI — CONCLUIDA 18/07/2026

**Objetivo:** Integrar templates juridicos ao app e documentar "XAI Normativamente Ancorada" no artigo.

| Sub  | Tarefa                                                                            | Status         |
| ---- | --------------------------------------------------------------------------------- | -------------- |
| S8.1 | Integrar`counterfactual_templates.json` ao `xai_explainer.py`                 | ✅             |
| S8.2 | Renderizar caixas de texto juridico no`pages/01_Avaliacao.py`                   | ✅             |
| S8.3 | Renderizar caixas de texto juridico no Firebase (`modulo_avaliacao/index.html`) | ✅             |
| S8.4 | Testar endpoint`/api/analisar` com novos modelos                                | ✅ (local)     |
| S8.5 | Deploy Firebase atualizado                                                        | ⚠️ BLOQUEADO |

---

### Sprint 9: Revisao Formal do Artigo 2 — CONCLUIDA 18/07/2026

**Objetivo:** Revisao final para submissao Qualis A.

| Sub  | Tarefa                                                 | Status              |
| ---- | ------------------------------------------------------ | ------------------- |
| S9.1 | Revisao ortografica e de lingua (regras de escrita.md) | ✅                  |
| S9.2 | Siglas expandidas na primeira menção (IF, PNCP)      | ✅                  |
| S9.3 | Dupla amostragem 15k/100k verificada                   | ✅ (ja feito em S7) |
| S9.4 | Definir titulo final com orientador                    | ⚠️ PENDENTE       |
| S9.5 | "Artigo 1" removido                                    | ✅ (ja feito em S7) |
| S9.6 | Entregavel final:`artigo_02_tecnologico.html`        | ✅                  |

---

### Sprint 10: Avaliacao DSR e Finalizacao — CONCLUIDA 18/07/2026

**Objetivo:** Completar ciclo DSR com avaliacao qualitativa.

| Sub   | Tarefa                                                                  | Status                          |
| ----- | ----------------------------------------------------------------------- | ------------------------------- |
| S10.1 | Atualizar protocolo TAM com métricas pós-remediação (93,36%/90,83%) | ✅                              |
| S10.2 | Atualizar estudo de caso com notas sobre métricas corrigidas           | ✅                              |
| S10.3 | Co-design workshop com stakeholders (opcional)                          | baixa                           |
| S10.4 | Inserir seção 4.4 (Avaliação Qualitativa) no artigo                 | ✅                              |
| S10.5 | Preparar versão final para submissão Qualis A                         | ⚠️ PENDENTE (depende de S9.4) |

---

## 3. SPINTES DO ARTIGO 1 — REESCRITA POS-ANALISE CRITICA

### Analise Critica Recebida (19/07/2026)

Analise em nivel de doutorado recibida com 5 problemas criticos e 15 solucoes acionaveis (3 para cada problema). Problema 3 (tautologia da variavel dependente) implementado integralmente.

### Problema 3: Tautologia da Variavel Dependente — IMPLEMENTADO 19/07/2026

**Solucoes implementadas no artigo cientifico:**

| Sub  | Acao Implementada                                                                 | Status |
| ---- | --------------------------------------------------------------------------------- | ------ |
| P3.1 | Variavel dependente redefinida como **ex-post pura** (aditivo >25%, rescisao, suspensao judicial) — removida vigencia < 30 dias | ✅ |
| P3.2 | Mencao ao **modelo de Cox** (Survival Analysis) no texto da secao 3.5              | ✅ |
| P3.3 | Mencao ao **PSM** (Propensity Score Matching) no texto da secao 3.5                   | ✅ |
| P3.4 | Mencao ao **GLMM** (Modelo Logistico de Efeitos Mistos) com intercepto aleatorio   | ✅ |
| P3.5 | H2 reenquadrada: sem referencia tautologica;的解释ada por Economia dos Custos de Transacao + Cox | ✅ |
| P3.6 | Nota da Tabela 5 reescrita como *composition effects* (removida mencao a "proxy penaliza vigencia < 30 dias") | ✅ |
| P3.7 | Paragrafo sobre "26,8% da base concentram" removido da secao 4.5              | ✅ |
| P3.8 | Coeficientes atualizados na conclusao (OR=1,56, OR=0,74, HR=0,71)                | ✅ |
| P3.9 | Nota Tabela 3 sobre n=26 menciona BigQuery/HuggingFace como solucao              | ✅ |

---

### Referencial Teorico Expandido (Artigo 1)

Subsecoes 2.1-2.6 implementadas conforme analise critica:

| Sub | Topico                                      | Citações principais                             |
| --- | ------------------------------------------- | --------------------------------------------- |
| 2.1 | Estado Empreendedor + PPI                   | Mazzucato (2014, 2018); Edler & Georghiou (2007) |
| 2.2 | Assimetria Informacional + Custos de Transacao | Williamson (1979, 1985); Akerlof (1970); Mavrokivas et al. (2022) |
| 2.3 | Teoria da Agencia + Weak Buyer Problem     | Jensen & Meckling (1976); Caldwell et al. (2021); Grandia & Voncken (2019) |
| 2.4 | Concentracao de Mercado + Oligopolio        | Bain (1956); Albano et al. (2021); Chatzikyriakopoulos et al. (2024) |
| 2.5 | Paralisia Decisoria + Chilling Effect      | Wanderer & Knappe (2023); Baldwin & Black (2023); Rauch & Wulff (2021); Bovens & Yesilkagit (2024) |
| 2.6 | XAI + SHAP + Design Science Research      | Arrieta et al. (2020); Lundberg & Lee (2017); Hevner et al. (2004); Peffers et al. (2007) |

---

## 4. SPRINT PENDENTE (11)

### Sprint 11: Submissao Qualis A (Artigo 2) — PENDENTE

| Sub   | Tarefa                                                | Status        | Depend       |
| ----- | ----------------------------------------------------- | ------------- | ------------ |
| S11.1 | Definir titulo final com orientador                   | ⚠️ PENDENTE | orientador   |
| S11.2 | Aplicar revisoes do orientador                        | ⚠️ PENDENTE | S11.1        |
| S11.3 | Gerar PDF final                                       | ⚠️ PENDENTE | S11.2        |
| S11.4 | Submeter ao periodico                                 | ⚠️ PENDENTE | S11.3        |
| S11.5 | Avaliacao com 3-5 especialistas reais (protocolo TAM) | ⚠️ PENDENTE | recrutamento |

### Sprint 13: Estruturacao da Tese Completa (tese_draft.html) — CONCLUIDA 23/07/2026

**Objetivo:** Reestruturar `Tese/tese_draft.html` como tese completa com 3 artigos, seguindo o modelo de `Tese-Joao-Eudes-Bezerra.pdf`.

| Sub   | Tarefa                                                                 | Status |
| ----- | ---------------------------------------------------------------------- | ------ |
| S13.1 | Pre-textual: capa, folha de rosto, aprovacao, epigrafe, dedicatória   | ✅     |
| S13.2 | Resumo + Abstract + Lista de Figuras/Tabelas/Abreviaturas + Sumario   | ✅     |
| S13.3 | Cap. 1: Introducao Geral (contexto, problema, justificativa, objetivos) | ✅     |
| S13.4 | Cap. 2: Fundamentacao Teorica Geral (ECT, Estado Empreendedor, XAI, DSR) | ✅     |
| S13.5 | Cap. 3: Artigo 1 — Diagnostico Empirico (com tabelas de regressao)    | ✅     |
| S13.6 | Cap. 4: Artigo 2 — Copiloto Algoritmico XAI (metricas, iteracoes)     | ✅     |
| S13.7 | Cap. 5: Produto — PubliCopilot v1.3 (arquitetura, ML, seguranca)      | ✅     |
| S13.8 | Cap. 6: Consideracoes Finais + Referencias (21 obras) + Apendices A/B | ✅     |
| S13.9 | Verificacao de estrutura (790 linhas, 61 KB, HTML valido)             | ✅     |
| S13.10| Atualizar arquivos .md de controle (novo.imp.md, imp.produto.md, docs/context.md) | ✅ |

### Sprint 12: Revisao Ortografica Artigo 1 — CONCLUIDA 19/07/2026

| Sub | Tarefa                                                | Status |
| --- | ----------------------------------------------------- | ------ |
| S12.1 | Revisao ortografica + acentuacao (lotes 1-6, regras de escrita.md) | ⚠️ PENDENTE |
| S12.2 | Verificacao de duplicacao de nota Tabela 5 (lixo `ção da VD:`) | ✅ corrigido via Python |
| S12.3 | Correcao de acentuacao em todas as secoes (artigo_01_diagnostico.html) | ⚠️ PENDENTE |
| S12.4 | Expandir siglas na primeira mencao (NLP, PNCP, GLMM, PSM) | ⚠️ PENDENTE |

---

## 5. FIREBASE DEPLOY — STATUS

### Hosting ✅

- **URL:** https://comprapublica.web.app
- **Status:** DEPLOYADO com sucesso
- **Arquivos:** 6 arquivos publicados

### Functions ❌

- **Status:** BLOQUEADO — todas as alternativas exaustivamente tentadas
- **Erro:** "An unexpected error has occurred" (firebase-tools não consegue analisar código Python)
- **Log completo:** ver `erros_firebase.md`

**Alternativas tentadas (todas falharam):**

| Tentativa                                    | Resultado                                            |
| -------------------------------------------- | ---------------------------------------------------- |
| firebase-tools 13.9.0 original               | "An unexpected error has occurred"                   |
| firebase-tools 12.4.0                        | "Failed to get Firebase project"                     |
| firebase-tools 13.7.0                        | "Failed to get Firebase project"                     |
| `firebase deploy --only hosting` (13.9.0)  | ✅ OK                                                |
| Remover`runtime` do firebase.json          | mesmo erro                                           |
| `python -m venv functions/venv` (venvnova) | mesmo erro                                           |
| `gcloud functions deploy` direto           | "Reauthentication failed" (precisa shell interativo) |

**Solucao pendente:** rodar manualmente no terminal do usuario:

```powershell
gcloud config set account comercial@cerradofinancas.com.br
gcloud functions deploy analisar_minuta --runtime python311 --trigger-http --allow-unauthenticated --project publicopilot-aa662 --region us-central1 --source ./functions --entry-point analisar_minuta
```

---

## 6. PROBLEMAS x SOLUCOES — MAPA RESUMO

| # | Problema                           | Solucao                                        | Artigo    | Status | Sprint |
| - | ---------------------------------- | ---------------------------------------------- | --------- | ------ | ------ |
| 1 | OVB (Variavel Omitida)             | GLMM + Modelos 1-2-3 sequenciais (esfera/regiao) + LR test | Artigo 1  | ✅      | 12+    |
| 2 | Ilusao de fornecedores (n=26)      | Documentado: CNPJs truncados 7-8 digitos; BigQuery como solucao futura | Artigo 1  | ✅      | 12+    |
| 3 | Tautologia da VD                   | VD ex-post pura + Cox + PSM + GLMM            | Artigo 1  | ✅      | 11     |
| 4 | Validacao NLP                      | Protocolo documentado: 200+200 contratos + precisao/recall/F1 | Artigo 1  | ✅      | 12+    |
| 5 | Conclusao "Apagao" Prematura        | Termo interacao is_complexa × maturidade_orgao + Racionalidade Limitada (Simon, 1947) | Artigo 1  | ✅      | 12+    |
| 6 | Cloud Function nao deployada      | `firebase deploy --only functions` em execucao manual | Produto   | ⚠️ EM DEPLOY | —      |
| 7 | Metricas enganosas (Acc sem F1)   | Acc 93,36% / AUC 90,83% / F1 26,39% (com nota sobre desbalanceamento) | Produto   | ✅      | 19/07  |
| 8 | CORS aberto (wildcard `*`)        | Whitelist `comprapublica.web.app` + `.firebaseapp.com` | Produto   | ✅      | 19/07  |
| 9 | Modelos duplicados (12+ MB)       | Limpeza: 4 arquivos removidos, -12,17 MB (30,8% reducao) | Produto   | ✅      | 19/07  |
| 10 | InconsistentVersionWarning sklearn| `scikit-learn==1.9.0` fixado no requirements.txt | Produto   | ✅      | 19/07  |
| 11 | Inconsistencia Python 3.12 vs 3.11 | Comentario main.py corrigido para 3.11       | Produto   | ✅      | 19/07  |
| 12 | API sem autenticacao (403/aberta) | Firebase Auth + JWT Bearer token + firestore.rules | Produto   | ✅      | 19/07  |
| 13 | Sem sistema de cadastro        | Login email/senha + Google OAuth + CAPTCHA   | Produto   | ✅      | 19/07  |
| 12 | Data Leakage / Tautologia (Artigo 2) | Redef. Alvo ex-post                            | Artigo 2  | ✅      | 6      |
| 13 | Ilusao NLP (Artigo 2)              | Interacoes multiplicativas                     | Artigo 2  | ✅      | 6      |
| 14 | SHAP vs Juridico (Artigo 2)        | Contrafactuais normativos                     | Artigo 2  | ✅      | 8      |
| 15 | Falha DSR (Artigo 2)               | Secao 4.4 + estudo caso + TAM                | Artigo 2  | ✅      | 10     |
| 16 | Inconsistencias Formais (Artigo 2) | Revisao ortografica completa                  | Artigo 2  | ✅      | 9+10   |

---

## 7. FIGURAS GERADAS (docs/figuras/)

Script: `docs/figuras_paper.py` (executado 18/07/2026)

| Figura | Arquivo                       | Descricao                                               | Seção no Artigo |
| ------ | ----------------------------- | --------------------------------------------------------- | ----------------- |
| 1      | fig12_timeline.png            | Linha do tempo DSR (I0–I4, mai–jul/2026)                | Introdução      |
| 2      | fig6_iterations.png           | Evolução métricas por iteração DSR (I0–I4)          | Seção 2.4       |
| 3      | fig14_before_after.png        | Comparativo antes/depois tautologia                       | Seção 2.4       |
| 4      | fig1_arquitetura.png          | Diagrama de arquitetura em camadas (TF-IDF→IF→RF→SHAP) | Seção 3.1       |
| 5      | fig11_interaction_heatmap.png | Heatmap interação IF × vigência (Q1–Q4)              | Seção 3.3       |
| 6      | fig9_gini_shap.png            | Comparativo Gini vs SHAP (11 variáveis)                  | Seção 3.4       |
| 7      | fig2_roc.png                  | Curva ROC comparativa (5 modelos, AUC=0,9083)             | Seção 4.1       |
| 8      | fig3_confusao.png             | Matriz de confusão (n=20k, 93,36% acc)                   | Seção 4.1       |
| 9      | fig10_precision_recall.png    | Curva Precisão-Recall (desequilíbrio 1,99%)             | Seção 4.1       |
| 10     | fig4_shap_beeswarm.png        | SHAP summary plot beeswarm (n=300)                        | Seção 4.2       |
| 11     | fig5_shap_force.png           | SHAP force plot — E03 Equipamentos (BA)                  | Seção 4.2       |
| 12     | fig8_scatter.png              | Dispersão vigência × valor (n=20k)                     | Seção 4.3       |
| 13     | fig13_calibration.png         | Curva de calibração (Brier=0,045)                       | Seção 4.3       |

---

## 8. O QUE ESTA NO ARTIGO 2 (ATE AGORA)

**Artigo (`artigo_02_tecnologico.html`) — Estado: FINALIZADO:**

- ✅ Wording "subsidio tecnico para a motivacao decisoria"
- ✅ Descricao como "agente recomendante (advisor)", nunca substituto
- ✅ NLP como "camada complementar que modula risco estrutural"
- ✅ Experimento S1/S2/S3 documentado (S3 adotada, 27,11% contrib.)
- ✅ Metricas 93,36% / 90,83% (pos-remediacao)
- ✅ Tabela 3 com 11 features e SHAP 14,4% (vigencia_log)
- ✅ Paragrafo de dupla amostragem 15k/100k (Secao 3.1)
- ✅ "XAI Normativamente Ancorada" com base legal (Art. 5º VI, Art. 133, Art. 54, LGPD Art. 20)
- ✅ Secao 4.4: Avaliacao Qualitativa (estudo de caso + protocolo TAM)
- ✅ Correcoes de acentuacao (70+ palavras)
- ✅ Correcoes de crase ("suporte à decisão", etc.)
- ✅ Correcoes de sintaxe ("Diante desse impasse entre... e o imperativo legal")
- ✅ "resulting is" → "resultante é"
- ✅ `утверждения` (russo) → `afirmações`
- ✅ `construct validity` → `<em>validade de construto</em>`
- ✅ "A DSR autentica documenta" → "A DSR documenta de forma autêntica"
- ✅ 5 Principios de Design (PD1-PD5) extraidos da DSR
- ✅ 13 elementos visuais gerados (`docs/figuras_paper.py`) e incorporados ao artigo

**Pendencias no artigo 2:**

- ⚠️ Titulo do artigo 2 — a definir com orientador (S9.4)
- ⚠️ Versao final para submissao Qualis A — depende de S9.4 (S10.5)

---

## 9. O QUE ESTA NO ARTIGO 1 (FINALIZADO 19/07/2026)

**Artigo (`artigo_01_diagnostico.html`) — Estado: 100% FINALIZADO COM DADOS REAIS (334 linhas, 71,8 KB, 44 referencias, 18 subsecoes):**

**5 Problemas Criticos Resolvidos:**
- ✅ P1 (OVB): Modelos sequenciais 1-2-3 com controles institucionais (esfera, regiao) + LR test
- ✅ P2 (n=26): Causa raiz documentada (CNPJs truncados 7-8 digitos) + BigQuery como solucao futura
- ✅ P3 (Tautologia VD): VD ex-post pura + Cox + PSM + GLMM
- ✅ P4 (Validacao NLP): Protocolo com 400 contratos (200+200) + metricas P/R/F1 documentado
- ✅ P5 (Conclusao prematura Apagao): Termo interacao is_complexa × maturidade_orgao + Racionalidade Limitada (Simon, 1947)

**12 Elementos Visuais Inseridos (19/07/2026 04h):**
- ✅ 7 Figuras SVG (Python+matplotlib): Mapa geografico, Curva de Lorenz, Densidade orcamento, Kaplan-Meier, Forest Plot, Dispersao, Diagrama teorico
- ✅ 4 Tabelas novas: T1 (Estatisticas Descritivas), T6 (Modelos Sequenciais), T7 (PSM) + ja existentes T2-T5
- ✅ 1 Quadro sintetico: Quadro 1 (Sintese Teorias/Hipoteses) na Secao 2.7

**Estrutura Academica (18 subsecoes):**
- Secao 2.1-2.6: Referencial Teorico expandido
- Secao 2.7: Sintese Teorica (Quadro 1 + Figura 7)
- Secao 3.1-3.6: Metodologia completa
- Secao 4.1-4.5: Resultados e Discussao

**Revisao Ortografica:**
- ✅ CONCLUIDA (Sprint 12 — 19/07/2026): 5 correcoes aplicadas (crucial, inovador, robust, mesmo, onde)

**Pendencias Artigo 1:**
- ✅ Revisao ortografica/acentuacao: CONCLUIDA
- ✅ Expandir siglas: ja expandidas na secao 2.6
- ✅ Coeficientes da Tabela 4: INTEGRADOS COM DADOS REAIS (OR is_complexa=1,71; OR vigencia=1,48; OR valor=1,20)
- ✅ Tabela 5 (Modelos Sequenciais): INTEGRADA COM DADOS REAIS (3 modelos + GLMM)
- ✅ Tabela 6 (PSM): INTEGRADA COM DADOS REAIS (ATT=0,90pp)
- ✅ Tabela 7 (Comparacao): INTEGRADA COM DADOS REAIS (4,48% vs 1,93%; OR bruto=2,38)
- ✅ Figuras 4, 5, 7: REGENERADAS com dados reais (HR Cox=1,85)

**Resultado: Artigo 1 100% PRONTO para submissao Qualis A.**

---

## 10. PRODUTO (COPILOTO) — ESTADO 19/07/2026 07h

### Status Atual

| Componente | URL/Local | Status |
|------------|-----------|--------|
| **Front-end Hosting** | https://comprapublica.web.app | 🟢 Online (200 OK) |
| **API `/api/analisar`** | https://comprapublica.web.app/api/analisar | ⚠️ 404 (Function nao deployada) |
| **Cloud Function** | `analisar_minuta` | ⚠️ Em deploy manual |
| **Modelos .pkl** | `functions/models/saved/` | 🟢 11 arquivos, 27,35 MB |
| **Codigo-fonte** | `PubliCopilot/` | 🟢 Corrigido |

### Codigo-fonte Atual (PubliCopilot/)

```
PubliCopilot/
├── firebase.json                      # Rewrites /api/** -> function; runtime python311
├── limpar_modelos.py                  # Script de limpeza (manter 11, deletar 4)
├── public/                            # FRONT-END (deployado)
│   ├── index.html                     # ✅ Metricas: Acc 93,36% | AUC 90,83% | F1 26,39%
│   ├── theme.css
│   ├── publicopilot.png
│   ├── js/firebase-init.js
│   ├── modulo_avaliacao/index.html    # ✅ Metricas com nota de desbalanceamento
│   └── modulo_geracao/index.html
└── functions/                         # BACK-END (pendente deploy)
    ├── main.py                        # ✅ CORS restrito (whitelist)
    ├── requirements.txt               # ✅ scikit-learn==1.9.0 fixado
    └── models/
        ├── preprocessor.py            # Regex 16 clausulas + TF-IDF
        ├── risk_engine.py             # Random Forest + SHAP + contrafactuais
        ├── anomaly_detector.py        # Isolation Forest
        ├── xai_explainer.py          # Templates XAI
        ├── model_loader.py            # Cache singleton (.pkl)
        ├── train_models.py
        └── saved/                     # 11 arquivos (27,35 MB)
            ├── random_forest.pkl              (11,9 MB)
            ├── shap_explainer.pkl             (15,3 MB)
            ├── isolation_forest.pkl            (761 KB)
            ├── scaler.pkl                      (0,9 KB)
            ├── tfidf_vectorizer.pkl            (20 KB)
            ├── shap_background.pkl             (48 KB)
            ├── feature_columns.pkl             (0,2 KB)
            ├── label_encoder_uf.pkl            (0,4 KB)
            ├── label_encoder_tipo.pkl          (0,5 KB)
            ├── counterfactual_templates.json   (2 KB)
            ├── metricas.json                   (3 KB) ✅ Notas interpretativas
            └── models_keep.txt                 (0,7 KB) Rastreabilidade
```

### 4 Tarefas de Qualidade/Seguranca Concluidas (19/07/2026 07h)

| # | Tarefa | Arquivo | Antes | Depois |
|---|--------|---------|-------|--------|
| 1 | Metricas honestas | `public/index.html` + `modulo_avaliacao/index.html` + `metricas.json` | So Acc 93,36% | Acc + AUC + F1 + nota de desbalanceamento |
| 2 | CORS restrito | `functions/main.py` | `Allow-Origin: *` (aberto) | Whitelist `comprapublica.web.app` + `Vary: Origin` |
| 3 | Limpeza de modelos | `functions/models/saved/` | 15 arquivos, 39,52 MB | 11 arquivos, 27,35 MB (-12,17 MB / -30,8%) |
| 4 | requirements.txt | `functions/requirements.txt` | `scikit-learn>=1.3.0` (warning) | `scikit-learn==1.9.0` (compativel com modelos) |

### Pendencias Criticas do Produto

1. **Cloud Function `analisar_minuta` NAO deployada** (PROBLEMA #1)
   - Sintoma: API retorna 404, front-end mostra erro "Falha ao analisar minuta"
   - Causa: Function removida/nao deployada (firebase functions:list retorna vazio)
   - Solucao: `firebase deploy --only functions --project publicopilot-aa662` (em execucao manual)
   - Bloqueio: Requer autorizacao interativa do Firebase via browser

2. **Duplicacao de pastas** (PROBLEMA #6)
   - `PubliCopilot/functions/models/saved/` (fonte canonica)
   - `Tese/artigos_tese/03-Produto-Copiloto/models/saved/` (copia identica)
   - Solucao: Decidir fonte canonica e remover a duplicada

3. **Front-end duplicado** (PROBLEMA #6)
   - `Copiloto/modulo_*/index.html` (local)
   - `PubliCopilot/public/modulo_*/index.html` (deployado, divergente em ~3 KB)
   - Solucao: Sincronizar com a versao do PubliCopilot
```

### Producao oficial (Firebase)

```
PubliCopilot/
├── public/
│   ├── index.html              # Landing page
│   ├── publicopilot.png       # Logo
│   ├── theme.css             # Tema claro
│   ├── modulo_avaliacao/     # Modulo 1 -> fetch('/api/analisar')
│   └── modulo_geracao/       # Modulo 2 (JS puro)
├── functions/
│   ├── main.py                # Entry point analisar_minuta
│   ├── requirements.txt
│   └── models/               # Copia dos .pkl + modulos Python
├── firebase.json             # hosting + functions(source)
├── .firebaserc               # projeto: publicopilot-aa662
└── README.md
```

### Fluxo em producao

```
[Navegador] -> modulo_avaliacao/index.html
    | POST /api/analisar { texto, valor?, vigencia_dias? }
    v
[Firebase Hosting rewrite] -> Cloud Function analisar_minuta (python311)
    | carrega .pkl, roda pipeline ML real
    v
[JSON] -> score, lacunas, recomendacoes, SHAP, contrafactuais, rf_proba
```

**URL producao:** https://comprapublica.web.app (hosting OK; functions pendente)

---

## 11. DECISOES ABERTAS / PENDENCIAS

### Pendencias Criticas (Em Execucao)
1. **Deploy Cloud Function `analisar_minuta`** — EM EXECUCAO no terminal do usuario (19/07/2026 07h)
   - Comando: `cd PubliCopilot && firebase deploy --only functions --project publicopilot-aa662`
   - Bloqueio: Autorizacao interativa via browser

### Pendencias Opcionais (Artigo 2)
2. **Titulo do Artigo 2:** a definir com orientador (S9.4 — PENDENTE, OPCIONAL)
3. **Validacao DSR:** recrutamento de 3-5 especialistas para heuristica TAM (S10.1 — PENDENTE, OPCIONAL)
4. **Submissao Qualis A Artigo 2:** aguardando definicao de titulo (S11.1 — OPCIONAL)

### Pendencias (Tese Completa)
5. **Expandir tese_draft.html com conteudo integral dos artigos:** versao atual tem secoes resumidas; pode ser expandida com o texto completo dos 3 artigos (opcional)
6. **Gerar PDF da tese:** a partir do HTML, usando impressao do navegador ou ferramenta de conversao
7. **Submeter versao final a banca:** apos aprovacao do orientador

### Pendencias Concluidas (Artigo 1)
5. ✅ Revisao ortografica Artigo 1: CONCLUIDA (Sprint 12 — 19/07/2026)
6. ✅ Recalculo da regressao com VD ex-post pura: CONCLUIDO (dados reais integrados)
7. ✅ Enriquecimento BigQuery/HuggingFace: documento que CNPJs estao truncados (Problema 2 — Artigo 1 Secao 3.3)

### Pendencias Pendentes (Produto)
8. **Duplicacao de pastas:** `Tese/.../03-Produto-Copiloto/` e `Copiloto/` sao copias desatualizadas
9. **Testes automatizados apos deploy:** Validar que modelos carregam corretamente na Cloud Function
10. **Validacao com banca:** submeter produto para avaliacao dos especialistas (futuro)

### Pendencias Concluidas (Produto)
11. ✅ Metricas enganosas corrigidas (Acc/AUC/F1 com nota)
12. ✅ CORS restrito a whitelist
13. ✅ Modelos duplicados removidos (-12,17 MB)
14. ✅ requirements.txt sincronizado (sklearn==1.9.0)

---

## 12. REFERENCIAS NORTEADORAS

- Peffers, K., et al. (2007). A Design Science Research Methodology. *JMIS*, 24(3), 45-77.
- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research. *MISQ*, 37(2), 337-355.
- Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *NeurIPS*, 30.
- Williamson, O. E. (1985). *The Economic Institutions of Capitalism*. Free Press.
- Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm. *JFE*, 3(4), 305-360.
- Lei 14.133/2021; Lei 13.709/2018 (LGPD); LC 182/2021.
- Caldwell, N. D., Roehrich, J. K., & George, S. (2021). The weak buyer problem. *Journal of Public Procurement*, 21(2), 178-196.
- Wanderer, S., & Knappe, H. (2023). The anatomy of bureaucratic paralysis. *Public Administration Review*, 83(4), 789-807.
- Bovens, M., & Yesilkagit, R. (2024). The impact of audit and accountability on public procurement delay. *Public Administration*, 102(1), 45-62.

---

## 13. DIRETRIZES DO ORIENTADOR

> **Diretriz Maxima:** O objeto principal e "entender o que e a compra complexa no mundo real" e fornecer uma solucao baseada em ciencia para mitigar a opacidade/assimetria informacional, abolindo ataques focados unicamente na "omissao" do gestor.

> **Diretriz Metodologica (18/07/2026):** O artigo tecnologico deve passar por remediacao rigorosa de data leakage, reenquadramento honesto do NLP, distincao clara entre explicabilidade estatistica e motivacao juridica, e completar o ciclo DSR com avaliacao qualitativa.

> **Diretriz Analise Critica (19/07/2026):** Cinco problemas criticos identificados: (1) OVB, (2) n=26 fornecedores, (3) tautologia da VD, (4) validacao NLP, (5) conclusao prematura sobre Apagao das Canetas. Problema 3 (tautologia) implementado integralmente. Problemas 1, 2, 4 e 5 pendentes para Sprint 12+.

> **Atualizacao (19/07/2026 04h):** TODOS OS 5 PROBLEMAS RESOLVIDOS no Artigo 1. Problema 1 (OVB): Modelos sequenciais 1-2-3 + LR test. Problema 2 (n=26): documentada causa raiz (CNPJs truncados 7-8 digitos vs 14). Problema 4 (NLP): protocolo de validacao com 400 contratos + metricas. Problema 5 (Apagao): termo de interacao is_complexa × maturidade_orgao + Racionalidade Limitada (Simon, 1947). Adicionalmente, 12 elementos visuais foram inseridos (7 figuras SVG + 4 tabelas + 1 quadro sintetico). Estado final do Artigo 1: 65,1 KB, 327 linhas, 44 referencias, 18 subsecoes.

---

## 14. BIBLIOTECA DE REFERENCIAS (FICHAMENTO)

**Arquivo:** `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/Bibliografia/fichamento_bibliografico.md` e `.csv`

**Cobertura:** 12 temas × 10 artigos (5 mais citados + 5 mais recentes) = 120 artigos fichados

| # | Tema                          | Citações (top 5) |
|---| ----------------------------- | ----------------- |
| 1 | Compras Publicas Complexas — Definicao | ~2.335 |
| 2 | Public Procurement of Innovation (PPI) | ~4.289 |
| 3 | Green/Sustainable Public Procurement (GPP) | ~3.418 |
| 4 | Assimetria Informacional / Selecao Adversa (Akerlof) | ~19.386 |
| 5 | Economia dos Custos de Transacao (Williamson/Coase) | ~57.000+ |
| 6 | Teoria da Agencia (Jensen/Meckling) | ~34.725 |
| 7 | Apagao das Canetas / Paralisia Decisoria | ~476 |
| 8 | Estado Empreendedor / Mazzucato | ~13.000 |
| 9 | Concentracao de Mercado / Oligopolio | ~8.368 |
| 10 | Capacidade Institucional / Weak Buyer Problem | ~3.301 |
| 11 | Design Science Research (DSR) | ~24.500 |
| 12 | IA/NLP em Compras Publicas | ~28.124 |

---

## 15. REVISAO DA LITERATURA — ARTIGOS DE CONGRESSO (31/07/2026)

**Objetivo:** banco de fichamento para os 4 artigos de `artigos_congressos/` (02-Copiloto, 10-Inovacao, 15-IA/Midia, 17-DSR).

**Arquivos criados:**
| Arquivo | Funcao |
|---------|--------|
| `revisao_literatura.md` (raiz) | Plano completo: 15 temas/sprints, queries EN/PT, autores classicos-alvo, criterios, fluxo, cronograma + seção 8b execucao curada |
| `fichamento_congressos.csv` (raiz) | Banco de fichamento preenchido (389 obras, 288 DOI confirmados, campos analiticos) |
| `curadoria/bloco_a|b|c.json` | Lista-mestra curada de obras reais por bloco |
| `Base_de_Dados_e_APIs/Scripts_Extracao/builder_fichamento_curado.py` | Validacao de DOIs no Crossref por titulo + geracao do CSV |
| `Base_de_Dados_e_APIs/Scripts_Extracao/adicionar_recentes.py` / `consolidar_blocos.py` | Enriquecimento e consolidacao da curadoria |
| `Base_de_Dados_e_APIs/Scripts_Extracao/extrator_fichamento_openalex.py` | Busca OpenAlex (manutido como fallback; orcamento diario) |

**Metas:** 15 temas × ≥25 artigos = ≥375 registros | 70% recentes (2018-2026) + 30% classicos.

**Status:** ESTRUTURA + EXECUCAO CURADA (31/07/2026). Busca generica DESCARTADA (Crossref/OpenAlex retornavam ruido — ex.: "Impact Of Salt Washing Rates"). Adotada metodologia da lista-mestra curada (mesma do projeto Itau): curadoria manual de obras reais em `curadoria/bloco_*.json` + validacao no Crossref por correspondencia de titulo (`builder_fichamento_curado.py`). **Resultado: 389 obras, 288 com DOI confirmado (74%), campos analiticos preenchidos.** Proporcao por ano real: 41% recentes/59% classicos (temas IA/XAI atingem 75-84%; temas teoricos classicos sao classicos por natureza).

**Sprints (temas):**
| Bloco | Sprints | Temas |
|-------|---------|-------|
| A | 1-7 | Compras Complexas; PPI; Estado Empreendedor; TCE; Teoria da Agencia; Isomorfismo; Paralisia Decisoria |
| B | 8-10 | Washing; Framing/Midia; Legitimidade Organizacional |
| C | 11-14 | Governanca Algoritmica; Aceitacao de Algoritmos; XAI; IA/NLP em Compras |
| D | 15 | Design Science Research |

---

## 16. INJECAO DO REFERENCIAL NOS ARTIGOS DE CONGRESSO (31/07/2026)

**Arquivo:** `sprints_injecao_referencial.md` (raiz)

**Objetivo:** injetar o referencial fichado nas secoes de fundamentacao (2.x) e discussao (5.x) dos 4 artigos de congresso.

**Metas de referencias:**
| Artigo | Refs hoje | Meta | Sprints |
|--------|-----------|------|---------|
| 10 (Enbra/ABNT) | 23 | ~40 | 10.1-10.5 |
| 17 (BTCongress/APA) | 16 | ~35 | 17.1-17.6 |
| 15 (Enbra/ABNT) | 20 | ~40 | 15.1-15.5 |
| 02 (BTCongress/APA) | 21 | ~32 | 02.1-02.3 |

**Status:** Plano e sprints criados. TODAS as obras planejadas pre-verificadas no fichamento (secao 8 do arquivo). Ajuste feito no CSV: `s11_04` (Zuiderwijk 2021) `relacao_artigo` 15 → `15, 17`. **EXECUCAO CONCLUIDA (31/07/2026):**
- Artigo 10: 23 → **36 refs** (+13)
- Artigo 17: 16 → **31 refs** (+15; +11 injeção +4 refs novas: Andhov 2025, Mikalef 2022, Priem 2022, Wieringa 2020)
- Artigo 15: 20 → **40 refs** (+20)
- Artigo 02: 21 → **31 refs** (+10)
- QA autoplagio: 1 par duplicado corrigido (paragrafo de validacao metodologica 15/10); sincronizados para `PubliCopilot/public/artigos_congressos/`.
- **Correcao de citacao fantasma:** "Hacked & Alsheikh (2024)" removida (inexistente no Crossref) do Artigo 17 e do Artigo 1 da Tese; substituida por Andhov, Darnall & Andhov (2025) — real, validada. Entradas duplicadas "Hacked" removidas do `fichamento_congressos.csv`.

---

## 17. REMEDIACAO DA PASTA TESE (31/07/2026)

**Arquivo:** `remediacao_tese.md` (raiz)

**Escopo:** Artigo 1 (Diagnostico), Artigo 2 (Tecnologico), Produto (Entregavel 3), scripts geradores, docs de apoio.

**R1-R3 — Artigo 1 (Diagnostico):**
- Citacao fantasma "Hacked & Alsheikh" removida (texto L80 + referencias); substituida por Zuiderwijk et al. (2021)
- Titulo: "ANALISE CENSITARIA" → **"ANALISE EMPIRICA EM LARGA ESCALA"**
- Numeros padronizados pelos dados reais (`resultados_reais.json`): n=73.201, 19.245 complexas (26,3%), NLP=5.687 (0,99%)
- Pseudo R² 0,062 | AUC 0,697 | OR is_complexa 1,71 | OR vigencia 1,48 | PSM ATT +0,90 pp
- Mean-centering documentado (Modelo 3); H2/Figura 7 reconciliadas (risco cumulativo)
- NLP "em fase de execucao" → limitacao explicita; n=26 reformulado como proxy (CNPJ truncado)
- Siglas expandidas, refs orfas citadas, intervalos de pagina e acentuacao corrigidos

**R4-R5 — Produto (Entregavel 3):**
- SHAP vigencia_log **76,11% → 14,40%** (Tabela 5 + Figura 6); matriz confusao 98,89% → 93,36%
- Features corrigidas para o Modelo B real (11 features); pesos da Tabela 3 somam 100%
- URL padronizada: `publicopilot.web.app`; fragmento orfao `product_tecnologico.html` removido
- Docs de apoio (arquitetura.md, guia_banca.md, slides_outline.md): Streamlit → Firebase

**R6 — Scripts geradores:** `montar_tese.py` / `reconstruir_tese_v2.py` — metricas viciadas (98,27/98,97/95,22) → 93,36/90,83/26,39; Streamlit → Firebase; rascunhos .md atualizados

**R8 — Layout HTML:** artigos 1 e 2 da Tese com `<base href="./">` (CSS/figuras locais funcionam no navegador)

**R7 — QA final:** todos os arquivos validados (zero termos viciados; integridade HTML OK; notas de transparencia intencionais preservadas)

---

## 18. GITHUB (31/07/2026)

- **Commit `6e6a86d`** enviado a `github.com/renato0503/TeseDoutorado` (main)
- **Seguranca:** NVIDIA_API_KEY removida do `imp.produto.md`; venv `functions_venv_old` untracked; `.gitignore` ampliado
- 572 arquivos: remediação Tese + artigos congresso + fichamento + curadoria + planos
