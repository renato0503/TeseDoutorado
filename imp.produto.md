# IMPLEMENTACAO DO PRODUTO (COPILOTO ALGORITMICO) — v2.1

Este documento controla as sprints de construcao e evolucao do **Produto (Entregavel 3)** da Tese de Doutorado, conforme o *pivot* de 03/07/2026.

O artefato final e um MVP funcional com **Machine Learning real** (TF-IDF + Isolation Forest + Random Forest + SHAP) treinado nos dados do PNCP (100k contratos). O MVP e servido **100% no Firebase** (Hosting + Cloud Functions Python + Firestore + Auth), eliminando a dependencia do Streamlit Cloud.

**Local do codigo-fonte (Streamlit, referencia academica):** `Tese/artigos_tese/03-Produto-Copiloto/`
**Local do deploy Firebase (producao):** `PubliCopilot/`
**URL producao:** https://publicopilot.web.app
**Comando deploy:** `cd PubliCopilot && firebase deploy`
**Comando local (referencia):** `streamlit run app/app.py`

**Ultima atualizacao:** 31/07/2026 — A1 RESOLVIDO: Cloud Function `analisar_minuta` deployada com sucesso (v17, ACTIVE, 512MB/120s). Causa raiz corrigida: faltava `roles/artifactregistry.writer` (upload). Nova pendencia: acesso publico (allUsers) bloqueado por org policy; hosting rewrite `/api/**` ainda retorna 404.

---

## STATUS GERAL — PAINEL DE MONITORAMENTO

### Sprint A: FUNDACAO E DEPLOY (8h — Prioridade 1)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| A1 | Deploy Cloud Function `analisar_minuta` | ✅ CONCLUIDO (31/07) | **v17 ACTIVE.** Causa raiz 25/07 era so leitura (`downloadArtifacts`); em 31/07 o build avancou e falhou por falta de UPLOAD (`uploadArtifacts`). Resolvido com `roles/artifactregistry.writer` + redeploy. |
| **A2** | **Retreinar modelo com target OBSERVAVEL** | ✅ CONCLUIDO | Target ex-post (aditivo_valor + multiplas_retificacoes). Acc=90,96%, AUC=91,05%, F1=22,67% |
| **A3** | **Regenerar `feature_columns.pkl` com 11 features** | ✅ CONCLUIDO | 11 features |
| **A4** | **Remover dados admin hardcoded (`admin-seed.js`)** | ✅ CONCLUIDO | admin-seed.js reescrito |
| **A5** | **`LabelEncoder` → `OrdinalEncoder(handle_unknown)`** | ✅ CONCLUIDO | train_models.py, model_loader.py, risk_engine.py |
| A6 | Validar deploy end-to-end (curl + frontend) | ⚠️ PARCIAL | Funcao ACTIVE, mas endpoint publico retorna 403 (sem allUsers) e hosting `/api/**` retorna 404. Ver secao 31/07/2026 |

### Sprint A+: EVOLUCOES ADICIONAIS (24/07/2026)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| A7 | Login anonimo automatico + modal cadastro perfil | ✅ CONCLUIDO | auth.js reescrito — anonimo na primeira visita, coleta nome/email/instituicao/perfil |
| A8 | Persistencia de analises no Firestore | ✅ CONCLUIDO | `analises/{uid}/historico/` — salva score, risco_ml, features_shap, timestamp |
| A9 | Dashboard admin | ✅ CONCLUIDO | `public/dashboard/index.html` — usuarios, analises, risco, score, export CSV |
| A10 | Pagina seed de admin | ✅ CONCLUIDO | `public/seed-admin.html` — cria doc no Firestore + orienta custom claim |
| A11 | Custom claim admin definida | ✅ CONCLUIDO | Via Firebase Admin SDK — `{"admin": true}` para o UID V7414xvbtFZWNltp5M1X0ximq7p2 |
| A12 | Firestore rules atualizadas | ✅ CONCLUIDO | Regras com `isAdmin()` por claim OU doc. Colecoes: usuarios, analises, editais, logs |
| A13 | deploy-key.json salvo + .gitignore | ✅ CONCLUIDO | `PubliCopilot/deploy-key.json` — protegido no .gitignore |
| A14 | Service account keys desbloqueadas | ✅ CONCLUIDO | Politica `disableServiceAccountKeyCreation` desativada no projeto |

### Sprint B: SEGURANCA (6h — Prioridade 2)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| B1 | Sanitizar XSS: `innerHTML` → `textContent`/DOMPurify | ✅ CONCLUIDO | modulo_geracao: DOM methods. modulo_avaliacao: sanitizacao + DOM. dashboard + seed: ok |
| B2 | Remover fallback JWT sem assinatura (`main.py:catch ImportError`) | ✅ CONCLUIDO | `firebase-admin` como dependencia obrigatoria |
| B3 | CAPTCHA matematico → reCAPTCHA v3 | ⏳ PENDENTE | Requer chave do Google — pendente usuario |
| B4 | CORS `set_admin_claim`: `*` → whitelist | ✅ CONCLUIDO | Mesma whitelist do analisar_minuta |
| **B5** | **Validacao tamanho input (max 50KB)** | ✅ CONCLUIDO | `main.py` — `raise ValueError` se exceder |
| **B6** | **Revisar `firestore.rules`** | ✅ CONCLUIDO | `isAdmin()` por claim OU doc |

### Sprint C: INTEGRIDADE DO ML (5h — Prioridade 3)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| C1 | Logging estruturado (substituir `except: pass`) | ✅ CONCLUIDO | `logging.error()` adicionado nos 4 modulos. Substituido `except: pass` critico |
| C2 | Completar `counterfactual_templates.json` (4 features) | ✅ CONCLUIDO | +4 features: if_anomaly_score, if_is_anomaly, interacao_if_valor, interacao_if_vigencia (total 12) |
| **C3** | **Limpar codigo morto** | ✅ CONCLUIDO | objeto_len removido, limpar_cache mantido, venv/ limpo |
| C4 | Normalizacao unicode no `preprocessor.py` | ✅ CONCLUIDO | `unicodedata.normalize('NFKD', texto)` adicionado |
| **C5** | **Validar consistencia metricas vs modelo vs frontend** | ✅ CONCLUIDO | Metricas atualizadas no metricas.json e frontend |

### Sprint D: QUALIDADE E TESTES (6h — Prioridade 4)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| D1 | Copiar `tests/` da Tese para producao | ⏳ PENDENTE | Criar `PubliCopilot/functions/tests/` |
| D2 | Testes integracao HTTP (`test_main.py`) | ⏳ PENDENTE | 4 cenarios (401, 200, 400, 400) |
| **D3** | **Corrigir `train_models.py`** | ✅ CONCLUIDO | Path relativo, amostra aleatoria, target observavel, OrdinalEncoder |
| **D4** | **Limpeza infra (venv, __pycache__, .gitignore)** | ✅ CONCLUIDO | venv/ deletado, __pycache__ limpo, .gitignore com deploy-key.json |
| D5 | Rate limiting (30 req/min por user) | ✅ CONCLUIDO | Implementado em `main.py` — `_verificar_rate_limit()` com janela deslizante de 60s |

### Sprint E: FRONTEND E UX (4h — Prioridade 5)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| E1 | Implementar JS menu mobile (`nav__toggle`) | ✅ CONCLUIDO | Nav toggle adicionado em modulo_geracao (com JS + style inject). Modulo_avaliacao mantido |
| E2 | Corrigir `showTab()` evento deprecated | ✅ CONCLUIDO | `function showTab(tabId, event)` com parametro explicito |
| E3 | Conectar Modulo Geracao a API NVIDIA | ✅ CONCLUIDO | NVIDIA API integrada (modelo llama-3.3-70b). Fallback para templates estaticos se API indisponivel |
| E4 | Sincronizar `counterfactual_legal` front/backend | ✅ CONCLUIDO | `counterfactual_templates.json` copiado para `/public/data/`. Frontend carrega via fetch com fallback local. 12 features sincronizadas |

### Sprint F: EVOLUCAO (8h — Prioridade 6, Opcional)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| **F1** | **Persistir analises no Firestore** | ✅ CONCLUIDO | `analises/{uid}/historico/` — implementado |
| F2 | Pagina historico do usuario | 📋 OPCIONAL | Listar analises anteriores |
| **F3** | **Dashboard admin com metricas agregadas** | ✅ CONCLUIDO | `public/dashboard/index.html` — total usuarios, analises, risco, export CSV |
| F4 | Exportar relatorio PDF | 📋 OPCIONAL | jsPDF com score, SHAP, contrafactuais |
| F5 | Melhorar fallback anomaly_detector | 📋 OPCIONAL | Heuristicas mais robustas |

### Sprint G: HARDENING POS-DEPLOY (1h — Prioridade 1, Executar apos A1)

| # | Tarefa | Status | Obs |
|---|--------|--------|-----|
| G1 | Remover `ADMIN_SETUP_SECRET` das env vars | ❌ BLOQUEADO | Depende de A1 |
| G2 | Deletar `key.json` do disco | ✅ CONCLUIDO | `deploy-key.json` mantido (protegido por .gitignore) |
| G3 | `firebase functions:list` — so `analisar_minuta` | ❌ BLOQUEADO | Depende de A1 |
| G4 | Testar endpoint sem token → 401 | ❌ BLOQUEADO | Depende de A1 |
| G5 | Limpar versoes antigas do Artifact Registry | ❌ BLOQUEADO | Depende de A1 |
| G6 | Simular firestore.rules no console | ✅ CONCLUIDO | Regras publicadas manualmente |
| G7 | `checklist_seguranca.md` criado | ✅ CONCLUIDO | `docs/checklist_seguranca.md` |

### Resumo

| Status | Qtd | Sprints |
|--------|-----|---------|
| ✅ CONCLUIDO | 34 | A1, A2-A5, A7-A14, B1-B2, B4-B6, C1-C5, D3-D5, E1-E4, F1, F3, G2, G6-G7 |
| ⏳ PENDENTE | 3 | B3 (reCAPTCHA, aguardando chave), D1-D2 (testes) |
| ⚠️ PARCIAL | 1 | A6 (validacao end-to-end — 403/404, ver 31/07) |
| ❌ BLOQUEADO | 4 | G1, G3-G5 (dependem do acesso publico da funcao / allUsers) |
| 📋 OPCIONAL | 3 | F2, F4-F5 |
| **Total** | **44** | **7 sprints (A-G) + NVIDIA** |

**Proximo bloqueio a resolver:** acesso publico a `analisar_minuta` (allUsers bloqueado por org policy) + redeploy hosting com rewrite `/api/**`.

### Diagnostico (25/07/2026 23h)
O erro de build encontrado nos logs do Cloud Build:
```
DENIED: Permission 'artifactregistry.repositories.downloadArtifacts' denied on resource
'projects/publicopilot/locations/us-central1/repositories/gcf-artifacts'
```

A service account `432118179013-compute@developer.gserviceaccount.com` (Compute Engine default)
precisa de permissao de leitura no Artifact Registry.

### Solucao (rodar como `comercial@cerradofinancas.com.br` — Proprietario)
```powershell
cd C:\Users\Renato\Documents\Doutorado\PubliCopilot
gcloud config set account comercial@cerradofinancas.com.br

# 1. Dar permissao Artifact Registry Reader para a compute SA
gcloud artifacts repositories add-iam-policy-binding gcf-artifacts --location=us-central1 --project=publicopilot --member=serviceAccount:432118179013-compute@developer.gserviceaccount.com --role=roles/artifactregistry.reader

# 2. Deploy da funcao (com --allow-unauthenticated)
gcloud functions deploy analisar_minuta --runtime python311 --trigger-http --allow-unauthenticated --project publicopilot --region us-central1 --source=functions --entry-point=analisar_minuta --memory=512MB --timeout=120s --set-env-vars NVIDIA_API_KEY=<NVIDIA_API_KEY>

# 3. Validar
curl.exe -X POST "https://us-central1-publicopilot.cloudfunctions.net/analisar_minuta" -H "Content-Type: application/json" -H "Authorization: Bearer $(gcloud auth print-identity-token)" -d '{\"texto\":\"teste\",\"modo\":\"avaliacao\"}'

# 4. Firebase hosting
firebase deploy --only hosting
```

---

## RESOLUCAO A1 + DIAGNOSTICO 31/07/2026

### Timeline completa do deploy (31/07/2026)

| Passo | Acao | Resultado |
|-------|------|-----------|
| 1 | Verificar permissoes Artifact Registry | `roles/artifactregistry.reader` JA estava aplicado (25/07) |
| 2 | Redeploy `gcloud functions deploy analisar_minuta` | Build falhou: `Permission 'artifactregistry.repositories.uploadArtifacts' denied` |
| 3 | Logs do Cloud Build (`gcloud builds log`) | Confirmou: erro era de UPLOAD da imagem Docker, nao mais de download |
| 4 | Causa raiz | compute SA `432118179013-compute@developer.gserviceaccount.com` tinha `reader` mas nao `writer` |
| 5 | `add-iam-policy-binding ... --role=roles/artifactregistry.writer` | Inicialmente PERMISSION_DENIED com deploy-account (sem setIamPolicy) |
| 6 | Contas testadas | `gestor.renatorosa@gmail.com` e `comercial@cerradofinancas.com.br` sem permissao/reauth; `deploy-account` tem `roles/editor` mas nao pode setar IAM do Artifact Registry |
| 7 | Owner do projeto identificado | `user:comercial@cerradofinancas.com.br` (`roles/owner`) — usuario executou `gcloud auth login` e `add-iam-policy-binding` manualmente no terminal |
| 8 | Confirmacao | `get-iam-policy` agora mostra `reader` + `writer` para a compute SA |
| 9 | Redeploy final (deploy-account) | ✅ **`analisar_minuta` v17 ACTIVE** — `https://us-central1-publicopilot.cloudfunctions.net/analisar_minuta`, 512MB, 120s, NVIDIA_API_KEY preservada |
| 10 | `add-iam-policy-binding ... --member=allUsers --role=roles/cloudfunctions.invoker` | deploy-account: 403 sem permissao. owner: **400 org policy** — `User allUsers is not in permitted organization` |
| 11 | Teste endpoint publico (POST sem token) | **403 Proibido** (funcao exige autenticacao, allUsers bloqueado) |
| 12 | Teste via hosting `https://comprapublica.web.app/api/analisar` | **404** — hosting nao esta roteando `/api/**` (rewrite nao ativo) |
| 13 | `firebase deploy --only hosting` | ⏸️ Abortado pelo usuario — pendente |

### Conclusao (31/07/2026)

- ✅ **A1 RESOLVIDO:** Cloud Function `analisar_minuta` **deployada (v17, ACTIVE)**.
- ⚠️ **Acesso publico:** o projeto possui **org policy** que impede `allUsers` (invocacao publica da funcao). Consequencia: chamada direta a funcao retorna 403.
- ⚠️ **Hosting rewrite:** `https://comprapublica.web.app/api/analisar` retorna 404 — o hosting precisa ser redeployado para ativar o rewrite `/api/**` (abortado por solicitacao do usuario).
- ℹ️ **Nota:** como a funcao exige token (sem allUsers), o rewrite do hosting pode nao funcionar mesmo apos redeploy se o org policy bloquear invocacao anonima. Alternativas: (a) liberar allUsers via exemption no org policy, (b) autenticar via Identity Platform no frontend e enviar `Authorization: Bearer <token>` (fluxo ja suportado em `main.py` via firebase-admin).

### Passos pendentes (proxima sessao)

1. Redeploy do hosting (`firebase deploy --only hosting`) para ativar rewrite `/api/**`.
2. Definir estrategia de acesso a funcao (org policy allUsers vs. autenticacao Bearer).
3. Validar end-to-end (A6): POST real com token Firebase Auth.
4. Apos acesso funcionar, concluir Sprint G (G1, G3, G4, G5).

---

## AUDITORIA SENIOR DE ENGENHARIA (24/07/2026)

### Resumo Executivo

O PubliCopilot possui arquitetura sofisticada (4 camadas Firebase + 5 estagios ML) e documentacao academica solida. Apos a Sprint A (24/07/2026):

- **ML corrigido:** Target observavel ex-post (1,99% positivos), 11 features, OrdinalEncoder, sem data leakage
- **Auth refeito:** Login anonimo automatico, coleta de perfil (nome/email/instituicao), admin por custom claim + Firestore doc
- **Persistencia:** Analises salvas em `analises/{uid}/historico/` para coleta academica
- **Dashboard admin:** Criado com metricas agregadas, export CSV
- **Cloud Function:** Bloqueada — build falha no Cloud Build. Pendente deploy manual

### Metricas do Modelo Atual

| Metrica | Valor | Nota |
|---------|-------|------|
| Acuracia | 90,96% | |
| AUC-ROC | 91,05% | Metrica primaria para classe desbalanceada |
| F1-Score | 22,67% | 1,99% de positivos |
| CV 5-fold | 90,80% | |
| Features | 11 | vigencia_log 18%, valor_log 22%, uf_encoded 19%, tipo_encoded 18% |

---

## NOVIDADES v2.1 (25/07/2026)

### Integracao NVIDIA IA
- **Cliente:** `PubliCopilot/functions/models/nvidia_client.py` — cliente para API NVIDIA (modelo `meta/llama-3.3-70b-instruct`)
- **Geracao de editais:** Modulo Geracao agora chama API real via backend. Fallback para templates estaticos se API indisponivel
- **Geracao de sugestoes:** `gerar_sugestao_reescrita()` disponivel para preencher lacunas contratuais com IA
- **Seguranca:** Chave API armazenada em `env/.env` (gitignored). Em producao, configurar via `--set-env-vars NVIDIA_API_KEY=...`

### Correcoes Criticas
- **Bug encoders:** `risk_engine.py` agora usa `get_encoder_uf()` e `get_encoder_tipo()` em vez de hardcodar 0
- **Unicode:** `preprocessor.py:limpar_texto()` agora faz `unicodedata.normalize('NFKD', texto)`
- **Logging:** Todos os 4 modulos tem `logging.error()` nos blocos except. Substituido `except Exception: pass` critico (risk_engine.py:274)
- **Counterfactual templates:** Expandido de 8 para 12 features (incluindo `if_anomaly_score`, `if_is_anomaly`, `interacao_if_valor`, `interacao_if_vigencia`)

### XSS Sanitizado
- **modulo_geracao:** Todo o JS reescrito com DOM methods (createElement, textContent). Zero innerHTML com dados dinamicos
- **modulo_avaliacao:** Sanitizacao + DOM methods na secao de explicabilidade. COUNTERFACTUAL_LEGAL sincronizado com backend (12 features)
- **Firebase:** Security headers adicionados (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)

### Rate Limiting
- `_verificar_rate_limit(uid)`: 30 req/min por usuario. Retorna 429 HTTP se excedido
- Janela deslizante de 60s. Implementado no `main.py` como dicionario em memoria

### Melhorias Frontend
- Modulo Geracao: conectado ao backend NVIDIA, fallback template-mode quando API off
- `showTab()` corrigido (parametro `event` explicito)
- Menu mobile adicionado (nav__toggle) via JS inject
- `counterfactual_templates.json` servido como asset estatico em `/public/data/`

---

## ARQUIVOS-CHAVE (ATUALIZADO 25/07/2026)

| Arquivo | Funcao |
|---------|--------|
| `PubliCopilot/functions/main.py` | Cloud Function (entry point) |
| `PubliCopilot/functions/models/risk_engine.py` | Pipeline ML (RF + SHAP + contrafactuais) |
| `PubliCopilot/functions/models/preprocessor.py` | Regex (16 clausulas) + score heuristico |
| `PubliCopilot/functions/models/anomaly_detector.py` | Isolation Forest (deteccao de anomalias) |
| `PubliCopilot/functions/models/model_loader.py` | Cache singleton de .pkl + get_encoder_* |
| `PubliCopilot/functions/models/xai_explainer.py` | Templates XAI + contrafactuais |
| `PubliCopilot/functions/models/train_models.py` | Script de treinamento (target observavel, 11 features, OrdinalEncoder) |
| `PubliCopilot/functions/models/saved/` | 11+ arquivos .pkl + metricas.json |
| `PubliCopilot/public/index.html` | Landing page |
| `PubliCopilot/public/modulo_avaliacao/index.html` | Modulo de avaliacao (anonimo + salva analise) |
| `PubliCopilot/public/modulo_geracao/index.html` | Modulo de geracao |
| `PubliCopilot/public/dashboard/index.html` | Dashboard admin (novo) |
| `PubliCopilot/public/seed-admin.html` | Pagina de seed admin (novo) |
| `PubliCopilot/public/js/auth.js` | Auth reescrito (anonimo, perfil, admin) |
| `PubliCopilot/public/js/firebase-init.js` | Inicializacao Firebase + salvarAnalise |
| `PubliCopilot/public/js/admin-seed.js` | Admin seed (sem dados hardcoded) |
| `PubliCopilot/functions/models/nvidia_client.py` | Cliente NVIDIA API (novo) |
| `PubliCopilot/public/data/counterfactual_templates.json` | Templates contrafactuais servidos como asset (novo) |
| `PubliCopilot/firebase.json` | Configuracao Firebase (com security headers) |
| `PubliCopilot/firestore.rules` | Regras atualizadas (admin por claim/doc) |
| `PubliCopilot/deploy-key.json` | Chave service account (protegida .gitignore) |
| `PubliCopilot/set_admin_claim.py` | Script auxiliar para custom claims |
| `erros_firebase.md` | Historico de erros de deploy |

---

## FLUXO EM PRODUCAO (ALVO)

```
[Navegador]
  |-- Login anonimo automatico (se nao logado)
  |-- Modal de perfil (nome, email, instituicao) — nao bloqueante
  |-- modulo_avaliacao/index.html
      | POST /api/analisar { texto, valor?, vigencia_dias? }
      | Authorization: Bearer <token>
      v
  [Firebase Hosting rewrite] -> Cloud Function analisar_minuta (python311)
      | 1. Valida token JWT (firebase-admin)
      | 2. Pre-processamento NLP (16 regex)
      | 3. Deteccao de anomalias (Isolation Forest)
      | 4. Estimacao de risco (Random Forest, 11 features)
      | 5. Atribuicao SHAP (TreeExplainer)
      | 6. Contrafactuais normativos + recomendacoes
      v
  [JSON] -> score, lacunas, clausulas, rf_proba, risco_ml,
            features_shap, contrafactuais, metricas
      v
  [Firestore] -> analises/{uid}/historico/{autoId}
      | texto_resumo, score, risco_ml, clausulas, timestamp
      v
  [Dashboard admin] -> usuarios, analises, export CSV
```

---

## CRONOGRAMA SUGERIDO

```
Semana 1 (24/07):  Sprint A concluida (exceto A1 pendente deploy)
Semana 2:           Sprint B (Seguranca) + C (ML)  ~11h
Semana 3:           Sprint D (Testes) + E (Frontend) ~10h
                    Sprint G (pos-deploy) ~1h
Semana 4:           Sprint F (Evolucao) ~8h (opcional)
```

**Risco principal:** A1 — Cloud Function deploy. Se erro persistir no Cloud Build, migrar backend para Render.com.

---

## HISTORICO DE SPRINTS CONCLUIDAS

### Sprint 1-10 (03/07-19/07/2026) — CONCLUIDAS

| Sprint | Conteudo | Data |
|--------|----------|------|
| 1 | Fundacao do Produto (MVP Core) | 10/07 |
| 2 | ML Real e Dados PNCP | 10/07 |
| 3 | Experiencia do Usuario e Freemium | 10/07 |
| 4 | Polimento Final | 10/07 |
| 5 | Port para Firebase (Cloud Function) | 18/07 |
| 6 | Remediacao Metodologica | 18/07 |
| 7 | Sincronizacao Tecnica | 18/07 |
| 8 | Implementacao Textual XAI | 18/07 |
| 9 | Revisao Formal Artigo 2 | 18/07 |
| 10 | Avaliacao DSR e Finalizacao | 18/07 |

### Sprint A (24/07/2026) — CONCLUIDA (Parcial)

| # | Tarefa | Status |
|---|--------|--------|
| A2 | Retreinar modelo com target observavel | ✅ |
| A3 | Regenerar feature_columns.pkl com 11 features | ✅ |
| A4 | Remover dados admin hardcoded | ✅ |
| A5 | LabelEncoder → OrdinalEncoder | ✅ |
| A7 | Login anonimo + modal perfil | ✅ |
| A8 | Persistencia analises Firestore | ✅ |
| A9 | Dashboard admin | ✅ |
| A10 | Seed admin page | ✅ |
| A11 | Custom claim via Admin SDK | ✅ |
| A12 | Firestore rules atualizadas | ✅ |
| A13 | Deploy-key + gitignore | ✅ |
| A14 | Service account keys desbloqueadas | ✅ |

### A1 — RESOLVIDO (Deploy Cloud Function)

**Status (31/07/2026):** ✅ DEPLOYADA — `analisar_minuta` v17 ACTIVE em `us-central1` (512MB/120s). Historia: 25/07 build falhava por `downloadArtifacts` (leitura); 31/07 o build avancou e falhou por `uploadArtifacts` (escrita). Aplicado `roles/artifactregistry.writer` na compute SA + redeploy. Acesso publico (allUsers) bloqueado por org policy — ver secao "RESOLUCAO A1 + DIAGNOSTICO 31/07/2026".

```powershell
cd C:\Users\Renato\Documents\Doutorado\PubliCopilot
gcloud config set account comercial@cerradofinancas.com.br
gcloud artifacts repositories add-iam-policy-binding gcf-artifacts --location=us-central1 --project=publicopilot --member=serviceAccount:432118179013-compute@developer.gserviceaccount.com --role=roles/artifactregistry.reader
gcloud functions deploy analisar_minuta --runtime python311 --trigger-http --allow-unauthenticated --project publicopilot --region us-central1 --source=functions --entry-point=analisar_minuta --memory=512MB --timeout=120s --set-env-vars NVIDIA_API_KEY=<NVIDIA_API_KEY>
firebase deploy --only hosting
```

---

## CONTINUAR DAQUI (24/07/2026 10h10) — HISTORICO

> ⚠️ **SUPERADO em 31/07/2026** — ver secao "RESOLUCAO A1 + DIAGNOSTICO 31/07/2026". A funcao esta deployada (v17 ACTIVE). Bloqueio atual: acesso publico (org policy allUsers) + hosting rewrite 404.

O deploy da Cloud Function esta 95% resolvido. O erro de build foi diagnosticado:

**Causa:** A service account `432118179013-compute@developer.gserviceaccount.com` (Compute Engine default) nao tem permissoes para fazer push da imagem Docker no Artifact Registry nem para executar builds do Cloud Build.

**Ja resolvido:**
- ✅ `roles/logging.logWriter` adicionado a compute SA

**Para resolver (terminal do usuario, conta `comercial@cerradofinancas.com.br`):**

```powershell
gcloud projects add-iam-policy-binding publicopilot `
  --member="serviceAccount:432118179013-compute@developer.gserviceaccount.com" `
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding publicopilot `
  --member="serviceAccount:432118179013-compute@developer.gserviceaccount.com" `
  --role="roles/cloudbuild.builds.editor"

gcloud config set account deploy-account@publicopilot.iam.gserviceaccount.com

gcloud functions deploy analisar_minuta `
  --runtime python311 --trigger-http --allow-unauthenticated `
  --project publicopilot --region us-central1 `
  --source=functions --entry-point=analisar_minuta `
  --memory=512MB --timeout=60s
```

**Apos deploy, validar (A6):**
```powershell
curl -X POST https://us-central1-publicopilot.cloudfunctions.net/analisar_minuta `
  -H "Content-Type: application/json" `
  -d '{\"texto\": \"Contratacao de software para gestao publica\"}'
```

**Fazer deploy do hosting (subir novas paginas):**
```powershell
firebase deploy --only hosting
```

---

## REFERENCIAS NORTEADORAS

- Peffers, K., et al. (2007). A Design Science Research Methodology. *JMIS*, 24(3), 45-77.
- Gregor, S., & Hevner, A. R. (2013). Positioning and presenting design science research. *MISQ*, 37(2), 337-355.
- Lundberg, S. M., & Lee, S. I. (2017). SHAP. *NeurIPS*, 30.
- Williamson, O. E. (1985). *The Economic Institutions of Capitalism*. Free Press.
- Lei 14.133/2021; Lei 13.709/2018 (LGPD); LC 182/2021.
- Caldwell, N. D., Roehrich, J. K., & George, S. (2021). The weak buyer problem. *Journal of Public Procurement*, 21(2), 178-196.
