# PubliCopilot (Copiloto Algorítmico para Compras Públicas Complexas)

[![Status](https://img.shields.io/badge/Status-Produ%C3%A7%C3%A3o-green.svg)]()
[![Auth](https://img.shields.io/badge/Auth-Firebase_+_JWT-blue.svg)]()
[![Model](https://img.shields.io/badge/AI-Explainable_(XAI)-purple.svg)]()
[![ML](https://img.shields.io/badge/ML-Treinado_(PNCP)-orange.svg)]()
[![Deploy](https://img.shields.io/badge/Deploy-Firebase_Blaze-red.svg)]()
[![Version](https://img.shields.io/badge/Version-1.3_(19_07_2026)-yellow.svg)]()

Bem-vindo ao **PubliCopilot**, o exoesqueleto cognitivo criado para apoiar pregoeiros e gestores públicos na estruturação de **Compras Complexas** (Inovação, TI, ESG).

Desenvolvido como produto empírico da Tese de Doutorado na Fucape Business School, este artefato resolve a dor da assimetria informacional e da latência decisória, garantindo **Accountability**, explicabilidade via XAI e legalidade aos processos licitatórios.

## O Problema que Resolvemos

Gestores públicos sofrem com o "apagão técnico" ao tentar redigir editais de tecnologia avançada contra um mercado privado oligopolista e hiper-especializado. A insegurança jurídica leva a editais direcionados ou mal formulados, que são sumariamente punidos por Tribunais de Contas ou impugnados pelo mercado.

## Status Atual (v1.3 — 19/07/2026)

| Componente | URL/Local | Status |
|------------|-----------|--------|
| Front-end (Firebase Hosting) | https://comprapublica.web.app | 🟢 Online |
| Cloud Function `analisar_minuta` | /api/analisar | 🟢 Deployada |
| Cloud Function `set_admin_claim` | /set_admin_claim | ⚠️ Pendente deploy |
| Firebase Authentication | login email/senha + Google | 🟢 Ativo |
| Firestore Rules (RBAC) | isAdminByClaim / isOwner | 🟢 Ativo |
| 11 Modelos ML (.pkl) | functions/models/saved/ | 🟢 27,35 MB |

## Como Funciona (XAI + Design Science Research)

Ao submeter a minuta do Edital (texto via textarea), o backend Python passa o texto por cinco filtros integrados:

1. **NLP/Regex (16 padrões):** Identifica cláusulas contratuais obrigatórias (Lei 14.133/2021) → cláusulas + lacunas.
2. **TF-IDF + Isolation Forest:** Vetoriza o objeto em 500 features e detecta anomalias contra 15.000 contratos do PNCP.
3. **Random Forest (11 features):** Prediz risco com modelo treinado em 100.000 contratos PNCP.
4. **SHAP TreeExplainer:** Explica qual feature mais contribuiu para o score, garantindo transparência.
5. **Contrafactuais normativos:** Recomendações de ajustes com fundamentação jurídica.

**Métricas oficiais (Modelo B em produção, pós-remediação metodológica de 18/07/2026):**
- **Acurácia:** 93,36%
- **AUC-ROC:** 90,83%
- **F1-Score:** 26,39% (reflete desbalanceamento de classes: 1,99% positivos)

> Nota: A acurácia isolada é métrica enganosa em problemas com classes desbalanceadas. Um classificador trivial que sempre prediz "sem evento" obteria ~98% de acurácia. AUC-ROC e F1-Score oferecem visão complementar da qualidade discriminante.

## Sistema de Autenticação (v1.3)

O PubliCopilot v1.3 implementa **autenticação obrigatória** com Firebase Authentication:

### Fluxo de Cadastro
1. Usuário clica em **"Solicitar Acesso"** no header da landing page.
2. Preenche: **Nome completo** (3-100 chars), **WhatsApp com DDD** (10-11 dígitos), **E-mail**, **Senha forte** (≥8 chars, 1 maiúscula, 1 minúscula, 1 número), **Confirmação de Senha**.
3. Resolve um **CAPTCHA matemático** (anti-bot: `a OP b = ?`).
4. Conta criada via `firebase.auth.createUserWithEmailAndPassword`.
5. Perfil salvo em `usuarios/{uid}` no Firestore com `papel: 'usuario'`.

### Fluxo de Login
- **Email + Senha** (tradicional) — Firebase Auth SDK
- **Google OAuth** (popup) — `signInWithPopup(GoogleAuthProvider)`
- Token JWT ID é gerado e enviado no header `Authorization: Bearer <token>` para a Cloud Function

### RBAC (Role-Based Access Control)
- **Custom claim `admin: true`** no token JWT (definida via Cloud Function `set_admin_claim`)
- Coleção `usuarios` no Firestore com campo `papel: 'admin'|'usuario'`
- Firestore Rules checam `request.auth.token.admin == true` para operações sensíveis

### Validação no Backend (`main.py`)
A função `_validar_token_firebase()` valida o token usando `firebase-admin` SDK:
- Verifica assinatura JWT
- Verifica `aud` (audience == project ID)
- Verifica `exp` (expiração)
- Retorna `uid` e `email` do usuário autenticado

Para desenvolvimento local, defina `SKIP_AUTH=1` para bypassar a validação.

## Planos (Freemium)

### Versão Gratuita (Comunidade)
- 3 análises por sessão
- Score Geral de Risco com ML real
- Detecção de lacunas contratuais
- Cláusulas detectadas + recomendações

### Versão Premium / Consultoria Privada
- Análises ilimitadas
- **Sugestões de reescrita** de cláusulas problemáticas
- Relatório de Auditoria Completo (download .txt)
- Parecer técnico de defesa assinado

**Fale com a Consultoria Renato Rosa** e transforme sua licitação de risco em uma contratação de sucesso.

## Arquitetura (v1.3 — Firebase)

```
PubliCopilot/
├── firebase.json                      # Rewrites /api/** → function; runtime python311
├── firestore.rules                    # Regras RBAC com custom claim admin
├── limpar_modelos.py                  # Script de manutenção de modelos
├── README.md                          # Este arquivo
├── public/                            # FRONT-END (deployado)
│   ├── index.html                     # Landing page design elite
│   ├── theme.css                      # Design system (700+ linhas)
│   ├── publicopilot.png
│   ├── css/auth.css                   # Estilos modal auth + user menu
│   ├── js/firebase-init.js            # Singleton + whenFirebaseReady()
│   ├── js/auth.js                     # Sistema auth completo + captcha
│   ├── js/admin-seed.js               # Auto-seed do admin
│   ├── modulo_avaliacao/index.html    # Auth gate + Bearer token
│   └── modulo_geracao/index.html      # Auth gate
└── functions/                         # BACK-END
    ├── main.py                        # analisar_minuta + set_admin_claim
    ├── requirements.txt               # scikit-learn==1.9.0 + firebase-admin
    └── models/                       # 11 modelos ML (27,35 MB)
        ├── preprocessor.py            # 16 regex, lacunas, scoring
        ├── risk_engine.py             # RF + SHAP + contrafactuais
        ├── anomaly_detector.py        # TF-IDF + Isolation Forest
        ├── xai_explainer.py           # Templates XAI normativos
        ├── model_loader.py            # Cache singleton .pkl
        ├── train_models.py
        └── saved/                     # 11 .pkl + metricas.json
```

## Stack Tecnológico

| Camada | Tecnologia |
|--------|-----------|
| Frontend | HTML5 + CSS3 + JS vanilla (design system elite McKinsey/OECD) |
| Hosting | Firebase Hosting (CDN global) |
| Auth | Firebase Authentication (email/senha + Google OAuth + IndexedDB persist) |
| Backend | Firebase Cloud Functions (Python 3.11) + functions-framework |
| ML Engine | Scikit-Learn 1.9.0 (Random Forest, Isolation Forest) |
| XAI | SHAP 0.43+ (TreeExplainer) + contrafactuais normativos |
| NLP | TF-IDF Vectorizer (500 features) + 16 regex cláusulas |
| Validação | firebase-admin 6.4+ (JWT validation) |
| Dados | Firestore (usuarios, avaliacoes, editais, logs) |
| Segurança | CORS whitelist + RBAC + Firestore Rules |

## Como Acessar

### Produção (Firebase)
Acesse: **https://comprapublica.web.app**

1. Clique em **"Solicitar Acesso"** ou **"Entrar"** no header.
2. Faça login com Google ou email/senha.
3. Acesse os módulos: **Avaliação** ou **Geração**.

### Execução Local (Desenvolvimento)
```bash
# 1. Instalar dependências
cd PubliCopilot
pip install -r functions/requirements.txt

# 2. Rodar Cloud Function localmente
cd functions
functions-framework --target analisar_minuta --port 8080

# 3. Servir front-end
cd ../public
python -m http.server 8000

# 4. Acessar: http://localhost:8000
```

## Como Testar

```bash
cd PubliCopilot/functions
python -m pytest ../tests/test_models.py -v
```

## Modelos Treinados (11 arquivos .pkl)

| Modelo | Tamanho | Função |
|--------|---------|--------|
| `random_forest.pkl` | 11,9 MB | Predição de risco (11 features, 100 árvores) |
| `shap_explainer.pkl` | 15,3 MB | Explicabilidade SHAP |
| `isolation_forest.pkl` | 761 KB | Detecção de anomalias (100 árvores) |
| `scaler.pkl` | 0,9 KB | Normalização de features |
| `tfidf_vectorizer.pkl` | 20 KB | Vetorização TF-IDF (500 features) |
| `shap_background.pkl` | 48 KB | Background para SHAP |
| `feature_columns.pkl` | 0,2 KB | Lista de features do modelo |
| `label_encoder_uf.pkl` | 0,4 KB | Encoding UF |
| `label_encoder_tipo.pkl` | 0,5 KB | Encoding tipo contratual |
| `counterfactual_templates.json` | 2 KB | Templates de contrafactuais |
| `metricas.json` | 3 KB | Métricas do modelo em produção |

**Total:** 27,35 MB (após limpeza de 4 arquivos duplicados em 19/07/2026).

## Como o Admin é Configurado

1. Abra o Firebase Console: https://console.firebase.google.com/project/publicopilot-aa662/authentication/users
2. Crie o usuário `gestor.renatorosa@gmail.com` ou use um já existente.
3. Copie o **UID** (no exemplo: `0RezM8WDtqVp4Od3TMYNMKESPye2`).
4. Abra https://comprapublica.web.app e faça login com o admin.
5. Abra o Console do navegador (F12) e execute:
   ```javascript
   await setAdminClaim('0RezM8WDtqVp4Od3TMYNMKESPye2', true, 'SuaSenhaSecreta')
   ```
6. Faça logout e login novamente para o token ser atualizado com a custom claim.
7. O documento `usuarios/{uid}` será criado/atualizado automaticamente com `papel: 'admin'`.

## Deploy

```bash
# Front-end
cd PubliCopilot
firebase deploy --only hosting --project publicopilot-aa662

# Backend (Cloud Functions)
firebase deploy --only functions --project publicopilot-aa662

# Firestore Rules
firebase deploy --only firestore:rules --project publicopilot-aa662

# Tudo
firebase deploy --project publicopilot-aa662
```

## Versões do Artefato

| Versão | Local | Descrição | Status |
|--------|-------|-----------|--------|
| `Copiloto/modulo_*` | Repo raiz | Protótipos HTML estáticos (referência de design) | Legado |
| `Tese/03-Produto-Copiloto/` | Local | MVP Streamlit (referência acadêmica) | Documentação |
| `PubliCopilot/` | Firebase | **Deploy v1.3 com auth + ML real** | 🟢 Produção |

## Documentação Adicional

- `Tese/artigos_tese/03-Produto-Copiloto/produto_tecnologico.html` — Documentação técnica em formato APA
- `Tese/artigos_tese/03-Produto-Copiloto/docs/arquitetura.md` — Arquitetura DSR detalhada
- `novo.imp.md` — Controle geral do projeto de Doutorado
- `imp.produto.md` — Histórico de sprints do produto
- `erros_firebase.md` — Histórico de problemas e soluções Firebase
- `docs/context.md` — Contexto geral da pesquisa
- `PubliCopilot/README.md` — Este arquivo

Para detalhes acadêmicos, consulte os artigos em `Tese/artigos_tese/`.
