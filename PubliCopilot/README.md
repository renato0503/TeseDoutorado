# PubliCopilot (Copiloto Algorítmico)

**Copiloto Algorítmico para Compras Públicas Complexas**

Plataforma de apoio à decisão para avaliação de editais e geração de cláusulas
para compras públicas complexas (inovação, TI, sustentabilidade), com **ML real**
servido 100% no Firebase.

**URL Produção:** https://comprapublica.web.app
**Projeto Firebase:** publicopilot-aa662
**Última atualização:** 19 de Julho de 2026 07h

---

## Estado Atual (19/07/2026)

| Componente | URL/Local | Status |
|------------|-----------|--------|
| Front-end (Hosting) | https://comprapublica.web.app | 🟢 Online |
| Auth Firebase | Login/Cadastro/Google | 🟢 Deployado |
| Firestore Rules | Regras de usuários/perfis | 🟢 Deployado |
| API `/api/analisar` | Firebase Function (com auth JWT) | ⚠️ Aguarda deploy manual |
| Modelos ML | `functions/models/saved/` | 🟢 11 arquivos, 27,35 MB |

---

## Arquitetura

```
PubliCopilot/
├── firebase.json                      # Rewrites /api/** -> function; runtime python311
├── firestore.rules                    # Regras de segurança do Firestore
├── limpar_modelos.py                  # Script de limpeza (manutenção)
├── README.md                          # Este arquivo
├── public/                            # FRONT-END (deployado)
│   ├── index.html                     # Landing + botões Login/Cadastro
│   ├── theme.css
│   ├── publicopilot.png
│   ├── css/auth.css                   # Estilos do modal de auth
│   ├── js/firebase-init.js            # Inicialização Firebase (App, Auth, Firestore)
│   ├── js/auth.js                     # Sistema de autenticação completo
│   ├── modulo_avaliacao/index.html    # Auth gate + token JWT
│   └── modulo_geracao/index.html      # Auth gate
└── functions/                         # BACK-END (pendente deploy)
    ├── main.py                        # CORS restrito + Auth JWT + lazy load
    ├── requirements.txt               # scikit-learn==1.9.0 + firebase-admin
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
            ├── metricas.json                   (3 KB)
            └── models_keep.txt                 (0,7 KB) Rastreabilidade
```

---

## Pipeline de ML (Módulo de Avaliação)

O front (`modulo_avaliacao`) faz `POST /api/analisar` com `{texto, valor?, vigencia_dias?}`.
A Cloud Function executa, em Python 3.11 real:

1. **NLP/Regex** — 16 padrões de cláusulas (Lei 14.133/2021) → cláusulas + lacunas.
2. **Score heurístico** (0–100) com pesos por cláusula.
3. **Isolation Forest + TF-IDF** (15k objetos PNCP) → feature de anomalia.
4. **Random Forest** (100k contratos, 11 features, 100 árvores) → `rf_proba` / risco.
5. **SHAP TreeExplainer** → top features + contrafactuais.
6. Recomendações híbridas (lacunas + SHAP) com fundamentos (Williamson, LGPD, LC 182).

O Módulo de Geração é client-side (templates da Lei 14.133 + justificativas XAI),
não depende de backend.

---

## Métricas Reportadas (Modelo B — Produção)

- **Acurácia:** 93,36%
- **AUC-ROC:** 90,83%
- **F1-Score:** 26,39% (reflete desbalanceamento de classes: 1,99% positivos)
- **N observados:** 100.000 contratos PNCP
- **Features:** 11 (incluindo `vigencia_log`, `interacao_if_vigencia`)

> **Nota metodológica:** A acurácia isolada é métrica enganosa em problemas
> com classes desbalanceadas. Um classificador trivial que sempre prediz "sem
> evento" obteria ~98% de acurácia. AUC-ROC e F1-Score oferecem visão
> complementar da qualidade discriminante do modelo.

---

## Pré-requisitos

- **Plano Blaze** no Firebase (a Cloud Function Python exige cobrança habilitada;
  o plano Spark gratuito não roda Cloud Functions).
- Node.js 20+ e Firebase CLI: `npm install -g firebase-tools`
- Python 3.11 local (opcional, só para testar a função via functions-framework)

---

## Deploy

```bash
cd PubliCopilot
firebase login
firebase use publicopilot-aa662
firebase deploy          # hosting + functions
```

Apenas a função (deploy em andamento no terminal do usuário, 19/07/2026 07h):
```bash
firebase deploy --only functions
```

Apenas o front:
```bash
firebase deploy --only hosting
```

---

## Testar a função localmente

```bash
cd functions
python -m pip install -r requirements.txt
python -m pip install functions-framework
functions-framework --target analisar_minuta --port 8080

# em outro terminal:
curl -X POST http://localhost:8080/ -H "Content-Type: application/json" \
  -d '{"texto":"Contratacao de sistema de IA. Lei 14.133/2021. Vigencia 24 meses."}'
```

---

## URLs

- **Produção (Hospedagem):** https://comprapublica.web.app
- **API de análise:** https://comprapublica.web.app/api/analisar

---

## Segurança

- Regras de Firestore para operações autenticadas.
- Credenciais em `env/` (gitignored).
- **CORS restrito** (corrigido em 19/07/2026): apenas origens autorizadas via env var
  `ALLOWED_ORIGINS` (padrão: `https://comprapublica.web.app,https://comprapublica.firebaseapp.com`).
- Adicionado header `Vary: Origin` para cache CDN correto.
- Modelos pickle com `scikit-learn==1.9.0` fixado (evita `InconsistentVersionWarning`).

---

## Manutenção

### Limpar modelos duplicados

```bash
python limpar_modelos.py            # dry-run (mostra o que faria)
python limpar_modelos.py --aplicar  # executa a limpeza
```

**Arquivos mantidos (11):** random_forest.pkl, isolation_forest.pkl, tfidf_vectorizer.pkl, scaler.pkl, shap_explainer.pkl, shap_background.pkl, feature_columns.pkl, label_encoder_uf.pkl, label_encoder_tipo.pkl, counterfactual_templates.json, metricas.json.

**Arquivos deletados (4):** random_forest_sem_vigencia.pkl (12,4 MB), scaler_sem_vigencia.pkl (0,9 KB), feature_columns_sem_vigencia.pkl (0,2 KB), shap_values_sample.pkl (51,7 KB).

A lista canônica está em `functions/models/saved/models_keep.txt`.

---

## Autenticação (Firebase Auth)

O produto implementa **autenticação obrigatória** para acessar os módulos de avaliação e geração.

### Fluxo de Cadastro
1. Usuário clica em **"Cadastrar"** no header.
2. Preenche: **Nome completo**, **WhatsApp (com DDD)**, **E-mail**, **Senha** (≥8 chars, 1 maiúscula, 1 minúscula, 1 número), **Confirmação de Senha**.
3. Resolve um **CAPTCHA matemático** (anti-bot).
4. Conta criada via `firebase.auth.createUserWithEmailAndPassword`.
5. Perfil salvo em `usuarios/{uid}` no Firestore com campos `papel: 'usuario'`.

### Fluxo de Login
- **Email + Senha** (tradicional)
- **Google OAuth** (popup)
- Token JWT ID é gerado e enviado no header `Authorization: Bearer <token>` para a Cloud Function.

### Validação no Backend (`main.py`)
A função `_validar_token_firebase()` valida o token usando `firebase-admin` SDK:
- Verifica assinatura JWT
- Verifica `aud` (audience == project ID)
- Verifica `exp` (expiração)
- Retorna `uid` e `email` do usuário autenticado

Para desenvolvimento local, defina `SKIP_AUTH=1` para bypassar a validação.

### Regras Firestore (`firestore.rules`)
- **Coleção `usuarios`**: usuário lê apenas seu próprio perfil
- **Coleção `avaliacoes`**: leitura apenas do próprio usuário + admin
- **Coleção `editais`**: leitura apenas do próprio usuário + admin
- **Coleção `logs`**: leitura apenas admin, criação autenticada

---

## Histórico de Versões

| Data | Versão | Mudanças |
|------|--------|----------|
| 18/07/2026 | v1.0 | Deploy inicial (hosting only); front-end online |
| 19/07/2026 | v1.1 | Métricas honestas; CORS restrito; modelos limpos (-12,17 MB); requirements.txt sincronizado; front-end v1.1 deployado |
| 19/07/2026 | v1.2 | **Sistema de autenticação completo**: login email/senha, Google OAuth, cadastro com nome+whatsapp+email+senha+confirmação+CAPTCHA matemático. Validação JWT na Cloud Function via firebase-admin. Firestore Rules atualizadas. Front-end v1.2 deployado. |
| 19/07/2026 | v1.3 (pendente) | Deploy da Cloud Function `analisar_minuta` com auth |
