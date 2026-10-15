# Jornada do Cliente — PubliCopilot

**plataforma:** `https://publicopiloto.web.app`  
**Cloud Function:** `https://us-central1-publicopiloto.cloudfunctions.net/analisar_minuta`  
**Status:** Produção (Blaze) — 15/10/2026

---

## Mapa de Telas

```
Landing
  ├── / (index.html)                    Landing page + navbar + CTA
  │     ├── Login Modal (overlay)       auth.js PubliAuth.Modal
  │     └── Cadastro Modal (overlay)   auth.js PubliAuth.Modal
  │
  ├── /modulo_avaliacao/               Módulo 1 — Análise de Editais
  │     ├── Avaliar Minuta             → POST /api/analisar_minuta
  │     ├── Exemplos pré-carregados     → SELECT `exemplos`
  │     ├── Resultado (score + risco)  ← API response
  │     └── Telemetria completa        → registrarEvento()
  │
  ├── /modulo_geracao/                 Módulo 2 — Geração de Cláusulas
  │     ├── Aba 1: Templates           → Templates Lei 14.133
  │     ├── Aba 2: Sugestão IA         → NVIDIA API
  │     └── Salvar/editais             → Firestore /editais/
  │
  ├── /dashboard/                      Painel Admin (admin only)
  │     ├── Métricas por orgão         → Firestore orgaos/
  │     ├── Tabela de usuários         → Firestore usuarios/
  │     ├── Tabela de análises         → Firestore analises/
  │     ├── Tabela de editais          → Firestore editais/
  │     ├── Logs de eventos (300)      → Firestore logs/
  │     └── Exportar CSV               → Multi-escopo
  │
  └── /seed-admin.html                 Utilitário — seed admin (dev)
```

---

## Jornada 1 — Visitante Anônimo

```
1. Acessa https://publicopiloto.web.app/
   → Landing page com hero, módulos, metodologia

2. Clica em "Solicitar Acesso" ou "Acessar Avaliação"
   → Abre modal de cadastro (auth.js PubliAuth.Modal)

3. Preenche: Nome, Email, Senha, WhatsApp, CAPTCHA
   → PubliAuth.cadastrar() → Firebase Auth (email/password)
   → Firestore: doc usuarios/{uid} criado com papel=usuario

4. REDIRECIONAMENTO:
   → Permanece na landing (sem redirect automático)
   → Clica manualmente em "Acessar Avaliação" ou "Acessar Geração"

5. Acessa /modulo_avaliacao/
   → Se não logado: login anônimo automático
   → Se primeiroAcesso: abre ProfileModal para completar dados
   → Usuário define: Instituição, Perfil, Órgão

6. Cola texto de edital + informa valor estimado
   → POST /api/analisar_minuta (Bearer token)
   → Cloud Function: valida token → extrai cláusulas (regex 16 padrões)
   → Isolation Forest (se modelos disponíveis) + Random Forest
   → SHAP: top-3 features + contrafactuais normativos
   → Retorna: score (0-100), classificação (baixo/médio/alto),
              lacunas, cláusulas, explicações

7. Recebe relatório completo na tela
   → Score + badge de risco
   → Lista de lacunas contratuais detectadas
   → Recomendações com fundamento jurídico (Lei 14.133)
   → Explicabilidade SHAP (se modelos disponíveis)
   → Contrafactuais normativos

8.(Telemetria) Cada ação gera evento em logs/:
   → page_view, avaliar_click, avaliar_inicio, avaliar_sucesso/erro
   → Todos os eventos são gravados com uid/orgaoId/timestamp
```

---

## Jornada 2 — Servidor de Órgão (SESP-MT, TJPR, etc.)

```
1. Recebe acesso do admin (email + senha temporária)

2. Login em https://publicopiloto.web.app/
   → Email: {usuario}@sesp.mt.gov.br (exemplo)
   → Senha: {senha temporária do admin_create_user.py}

3. Firestore: custom claims aplicados automaticamente:
   → orgaoId: "SESP-MT"
   → perfil: "pregoeiro"
   → papel: "usuario" (não admin)

4. Acessa /modulo_avaliacao/
   → Todos os editais analisados ficam vinculados ao seu orgaoId
   → Dashboard mostra métricas do seu órgão apenas

5. Analisa editais normalmente
   → /editais/{id} salvo com orgaoId = SESP-MT

6. Telemetria: todos os eventos incluem orgaoId e uid
```

---

## Jornada 3 — Administrador (Gestor)

```
1. Login: gestor.renatorosa@gmail.com
   → Custom claim: admin: true, papel: admin, orgaoId: gestor

2. Acessa /dashboard/
   → Acesso total: todos os órgãos, todos os usuários
   → Pode ver logs de eventos de todos

3. Funções do dashboard:
   → Seed de órgãos (seed-orgaos): SESP-MT, POLITEC-MT, TJPR, TJRN
   → Criação de usuários via admin_create_user.py (CLI)
   → Visualização de métricas por órgão (cards clicáveis)
   → Exportar CSV de: usuários / análises / editais / logs / tudo

4. Acessa /seed-admin.html (ferramenta de dev)
   → Para uso em desenvolvimento/staging apenas
```

---

## Fluxo de Autenticação (detalhado)

```
┌─────────────────┐
│  Landing page   │  onAuthStateChanged listener ativo
│  (/index.html)  │
└────────┬────────┘
         │ usuário clica "Entrar"
         ▼
┌─────────────────┐
│  Modal login    │  PubliAuth.abrirLogin()
│  (overlay)      │  • Email/senha → signInWithEmailAndPassword
└────────┬────────┘  • Google → signInWithPopup
         │ OK       • Anônimo → signInAnonymously
         ▼
┌─────────────────────────────────────┐
│  onAuthStateChanged dispara (auth.js)│
│  → atualizaUI()                      │
│    • Mostra/esconde botões nav        │
│    • Grava ultimoAcesso no Firestore  │
│    • Detecta primeiroAcesso → ProfileModal│
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Usuário na     │  Telemetria: login_sucesso
│  landing logado  │  (uid/email/orgaoId em logs/)
└─────────────────┘
```

---

## Fluxo de Análise de Minuta (API)

```
Browser                        Cloud Function              Firestore
   │                               │                          │
   │ POST /api/analisar_minuta      │                          │
   │ Authorization: Bearer {token} │                          │
   │ {texto, valor}                │                          │
   │───────────────────────────────▶│                          │
   │                               │                          │
   │                          1. Extrair uid/email/claims   │
   │                          2. Verificar rate limit       │
   │                               │                          │
   │                          3. validar_token_firebase()    │
   │                             ✅ Token válido?             │
   │                               │                          │
   │                          4. Pipeline ML:               │
   │                             extrair_clausulas()         │
   │                             detectar_lacunas()           │
   │                             calcular_score()  ← heurística │
   │                             (RF, IF, SHAP) ← só se .pkl│
   │                               │                          │
   │                          5. Se ENABLE_AUDIT_LOG=1:     │
   │                               │                          │
   │                               │  set(doc logs/{id}, {    │
   │                               │    tipo: "analise",      │
   │                               │    uid, email, orgaoId,  │
   │                               │    duracao_ms, status }) │
   │                               │─────────────────────────▶│
   │                               │                          │
   │◀──────────────────────────────│                          │
   │  {score, risco, lacunas,       │                          │
   │   clausulas, explicacoes,       │                          │
   │   metricas}                    │                          │
```

---

## Estrutura de Dados Firestore

```
/usuarios/{uid}
  email, nome, papel, perfil, orgaoId,
  provedor, ativo, primeiroAcesso,
  totalAnalises, whatsapp, instituicao,
  dataCriacao, ultimoAcesso

/orgaos/{orgaoId}        ← criado via seed-orgaos
  nome, sigla, estado, tipo, regiao,
  ativo, dataCriacao

/editais/{editalId}       ← criado pelo módulo de geração
  orgaoId, titulo, tipo, valor,
  clausulasGeradas[], dataCriacao,
  uid (criador)

/analises/{analiseId}     ← criado pelo módulo de avaliação
  uid, orgaoId, texto, score,
  risco, lacunas[], dataCriacao

/logs/{logId}             ← audit trail automático
  tipo, uid, email, orgaoId, claims{},
  duracao_ms, status, ip, userAgent,
  extras{}, timestamp
```

---

## Usuários de Teste (ambiente de validação)

| Email | Órgão | Papel | Senha |
|---|---|---|---|
| `gestor.renatorosa@gmail.com` | gestor | admin | `G3st0r@2026!` |
| `sesp-teste@sesp.mt.gov.br` | SESP-MT | pregoeiro | `7L%9JSh0pxl1cX` |
| `politec-teste@politec.mt.gov.br` | POLITEC-MT | pregoeiro | `Lw8&XT3pU*j0vE` |
| `tjpr-teste@tjpr.jus.br` | TJPR | pregoeiro | `&PhfU6S8Fv78$!` |
| `tjrn-teste@tjrn.jus.br` | TJRN | pregoeiro | `nUXfwLZVzH7Enh` |

---

## Testes de Smoke

```bash
# Landing
curl -s -o /dev/null -w "%{http_code}" https://publicopiloto.web.app/
# Esperado: 200

# Dashboard
curl -s -o /dev/null -w "%{http_code}" https://publicopiloto.web.app/dashboard/
# Esperado: 200

# Módulo Avaliação
curl -s -o /dev/null -w "%{http_code}" https://publicopiloto.web.app/modulo_avaliacao/
# Esperado: 200

# Módulo Geração
curl -s -o /dev/null -w "%{http_code}" https://publicopiloto.web.app/modulo_geracao/
# Esperado: 200

# API sem token
curl -s -X POST https://us-central1-publicopiloto.cloudfunctions.net/analisar_minuta \
  -H "Content-Type: application/json" \
  -d '{"texto":"teste","valor":1000}'
# Esperado: {"erro":"Token de autenticacao ausente...","code":"unauthorized"}

# API com token inválido
curl -s -X POST https://us-central1-publicopiloto.cloudfunctions.net/analisar_minuta \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer INVALID" \
  -d '{"texto":"teste","valor":1000}'
# Esperado: {"erro":"Token invalido...","code":"unauthorized"}
```
