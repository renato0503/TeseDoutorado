# Erros e Alternativas — Deploy Firebase (PubliCopilot)

## Resumo do Estado

- **Hosting**: deploy OK — `https://comprapublica.web.app`
- **Functions**: bloqueado — todas as versões/alternativas falharam
  -Projeto: `publicopilot-aa662` (Blaze plano ativo)

---

## Problema 1 — venv Inexistente (Sprint 8)

**Erro original:**

```
Error: spawn "C:\Users\Renato\Documents\Doutorado\PubliCopilot\functions\venv\Scripts\activate.bat" ENOENT
```

**Causa:** diretório `functions/venv` não existia.
**Solução aplicada:**

```powershell
python -m venv "C:\Users\Renato\Documents\Doutorado\PubliCopilot\functions\venv"
```

Após isso, o erro de venv foi resolvido mas deu passo para o Problema 2.

---

## Problema 2 — "An unexpected error has occurred" (firebase-tools 13.9.0)

**Erro (firebase-tools 13.9.0):**

```
i  functions: Loading and analyzing source code for codebase default to determine what to deploy
(node:20960) [DEP0190] DeprecationWarning: Passing args to a child process with shell option true...
Error: An unexpected error has occurred.
```

**Causa:** firebase-tools 13.9.0 não consegue analisar código Python com a estrutura atual.
**Alternativas tentadas:**

| Tentativa                          | Versão | Resultado                                                    |
| ---------------------------------- | ------- | ------------------------------------------------------------ |
| `firebase deploy` original       | 13.9.0  | Erro "An unexpected error has occurred"                      |
| Downgrade para 12.4.0              | 12.4.0  | `Error: Failed to get Firebase project publicopilot-aa662` |
| Downgrade para 13.7.0              | 13.7.0  | `Error: Failed to get Firebase project`                    |
| Upgrade para 13.9.0                | 13.9.0  | Mesmo erro "An unexpected error has occurred"                |
| `firebase deploy --only hosting` | 13.9.0  | ✅ OK — hosting deploya                                     |
| Retorno para 13.9.0                | 13.9.0  | Problema persiste                                            |

---

## Problema 3 — "Failed to make request to serviceusage.googleapis.com"

**Erro (firebase-tools 13.7.0+):**

```
Error: Failed to make request to https://serviceusage.googleapis.com/v1/projects/publicopilot-aa662/services/cloudfunctions.googleapis.com
```

**Causa:** google-auth refresh token expirado ou credenciais inválidas para API `cloudfunctions.googleapis.com`.
**Alternativas tentadas:**

| Tentativa                                                          | Resultado                                                                   |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| `gcloud auth login` (conta `comercial@cerradofinancas.com.br`) | Requer shell interativo — não funciona                                    |
| `gcloud functions deploy` direto                                 | `Reauthentication failed. cannot prompt during non-interactive execution` |
| `firebase login:ci` com token existente                          | Token recusado                                                              |
| Autenticação via`firebase use --add`                           | Não resolve o token                                                        |
| Esperar 5s e repetir                                               | Abortado pelo usuário                                                      |

---

## Problema 4 — firebase.json "runtime" field

**Erro com `"runtime": "python312"` no firebase.json:**

```
Error: An unexpected error has occurred.
```

**Solução tentada:** remover `"runtime": "python312"` do firebase.json → mesmo erro.

**Erro com `"runtime": "python311"`:**

```
Error: Failed to make request to https://serviceusage.googleapis.com/v1/projects/publicopilot-aa662/services/artifactregistry.googleapis.com
```

**Solução aplicada:** manter `"source": "functions"` sem field `runtime`.

---

## Problema 5 — Autenticação gcloud vs Firebase CLI

**Estado atual das contas `gcloud auth list`:**

```
ACTIVE  ACCOUNT
*       comercial@cerradofinancas.com.br         ← correta para Firebase
        firebase-adminsdk-fbsvc@cerrafood.iam.gserviceaccount.com
        gerson@napolepizzaartesanal.com.br         ← conta errada
```

**Problema:** `gcloud functions deploy` precisa de `gcloud auth login` interativo, que não funciona neste ambiente. A conta `comercial@cerradofinancas.com.br` está autenticada no gcloud mas não é usada corretamente pelo firebase-tools.

---

## Alternativa Futura (não testada)

### Opção A — Deploy manual via gcloud (precisa terminal interativo)

```powershell
gcloud config set account comercial@cerradofinancas.com.br
gcloud functions deploy analisar_minuta \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --project publicopilot-aa662 \
  --region us-central1 \
  --source ./functions \
  --entry-point analisar_minuta
```

### Opção B — Atualizar projeto Firebase via Console

Acessar https://console.firebase.google.com/project/publicopilot-aa662/overview e verificar se há alguma configuração pendente.

### Opção C — Criar novo projeto Firebase

Se o projeto `publicopilot-aa662` estiver com algum estado corrompido, criar um novo projeto e migrar.

### Opção D — Usar outra plataforma (Render, Railway, etc.)

Se Firebase continuar impassível, considerar migrar a Cloud Function para outra plataforma que suporte deploy via API key.

### Opção E — Investigar token OAuth refresh

O firebase-tools 13.9.0 tenta refresh do token OAuth via browser interativo. É possível que seja necessário um token de refresh persistente configurado no firebase config.

---

## Arquivos Modificados Durante as Tentativas

- `firebase.json`: field `runtime` removido/adicionado/mudado entre `python312` e `python311`
- `functions/venv/`: criado do zero com `python -m venv`
- firebase-tools: múltiplas versões testadas (12.4.0, 13.7.0, 13.9.0, 13.7.0)

---

## Deploy Concluído com Sucesso

- ✅ **Hosting**: `https://comprapublica.web.app` — 6 arquivos publicados
- ❌ **Functions**: não deployado — aguardando solução de autenticação





O cenário que você descreveu é um clássico "inferno de dependências" do Firebase com Python no Windows. O erro `serviceusage.googleapis.com` combinado com `cannot prompt during non-interactive execution` é a pista definitiva: **o Firebase CLI está tentando renovar um token OAuth expirado em segundo plano e falhando porque não consegue abrir o navegador.**

A solução definitiva para contornar isso **não é** brigar com o `firebase login`, mas sim usar uma **Chave de Conta de Serviço (Service Account Key)**. Isso elimina a necessidade de interação humana, autentica diretamente com o Google Cloud e resolve 99% desses erros de "unexpected error".

Siga este passo a passo cirúrgico para resolver o problema:

---

### 🛠️ FASE 1: Limpeza Total do Ambiente

Antes de tentar de novo, vamos remover versões conflitantes e caches corrompidos.

1. Abra o PowerShell como **Administrador**.
2. Desinstale todas as versões do firebase-tools:
   ```powershell
   npm uninstall -g firebase-tools
   ```
3. Limpe o cache do npm:
   ```powershell
   npm cache clean --force
   ```
4. Instale a versão mais estável atual para Python (a 13.x tem bugs conhecidos no Windows com Python, a 12.9.1 é a mais robusta para isso):
   ```powershell
   npm install -g firebase-tools@12.9.1
   ```

---

### 🔑 FASE 2: Autenticação Robusta (A Solução Definitiva)

Vamos criar uma chave que não expira e não pede navegador.

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Certifique-se de que o projeto selecionado no topo é o **`publicopilot-aa662`**.
3. No menu lateral, vá em **IAM e Administração** > **Contas de Serviço**.
4. Clique em **+ CRIAR CONTA DE SERVIÇO**.
   - Nome: `firebase-deployer`
   - Clique em "Criar e Continuar".
5. Na etapa de permissões, conceda estes **3 papéis** (um por um):
   - `Administrador do SDK Admin do Firebase` (Firebase Admin SDK Administrator)
   - `Desenvolvedor do Cloud Functions` (Cloud Functions Developer)
   - `Visualizador do Cloud Build` (Cloud Build Viewer)
6. Clique em "Concluído".
7. Na lista de contas de serviço, clique nos **três pontinhos** ao lado de `firebase-deployer@...` e escolha **Gerenciar chaves**.
8. Clique em **Adicionar chave** > **Criar nova chave** > Escolha **JSON** > Criar.
9. Um arquivo `.json` será baixado. **Mova este arquivo** para a raiz do seu projeto (ex: `C:\Users\Renato\Documents\Doutorado\PubliCopilot\service-account-key.json`).
   ⚠️ **NUNCA** suba este arquivo para o GitHub. Adicione-o ao seu `.gitignore`.

---

### ⚙️ FASE 3: Habilitar APIs Obrigatórias

O erro `serviceusage` ocorre porque o Firebase tenta verificar se as APIs estão ativas e falha. Vamos ativá-las manualmente.

1. No [Google Cloud Console](https://console.cloud.google.com/), com o projeto `publicopilot-aa662` selecionado.
2. Use a barra de pesquisa superior para buscar e **ATIVAR** estas 3 APIs (uma por uma):
   - `Cloud Functions API`
   - `Cloud Build API`
   - `Artifact Registry API`
3. Aguarde 1 minuto após ativar a última.

---

### 📝 FASE 4: Corrigir os Arquivos de Configuração

O Firebase para Python é rigoroso com o `firebase.json`.

1. Abra seu `firebase.json` e deixe-o **exatamente** assim:

   ```json
   {
     "functions": [
       {
         "source": "functions",
         "codebase": "default",
         "runtime": "python311",
         "ignore": [
           "venv",
           "__pycache__",
           "*.pyc",
           ".git",
           ".env"
         ]
       }
     ],
     "hosting": {
       "public": "public",
       "ignore": [
         "firebase.json",
         "**/.*",
         "**/node_modules/**"
       ]
     }
   }
   ```

   *(Nota: Use `python311`. O `python312` ainda apresenta instabilidades no ambiente de build do Firebase).*
2. Dentro da pasta `functions`, certifique-se de que o arquivo `requirements.txt` existe e contém, no mínimo:

   ```text
   firebase-functions>=0.1.0
   Flask>=2.0.0
   ```

---

### 🚀 FASE 5: O Deploy "À Prova de Falhas"

Agora vamos forçar o CLI a usar a chave JSON que baixamos, ignorando completamente o token OAuth quebrado.

1. No PowerShell, navegue até a raiz do projeto (`PubliCopilot`).
2. Defina a variável de ambiente que aponta para sua chave (isso dura apenas nesta sessão do terminal):
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Renato\Documents\Doutorado\PubliCopilot\service-account-key.json"
   ```
3. Execute o deploy **apenas da função específica** (isso evita que o Firebase tente analisar códigos quebrados em outras funções):
   ```powershell
   firebase deploy --only functions:analisar_minuta
   ```

---

### 🛡️ PLANO B: Se o Firebase CLI continuar falhando (Recomendado para Python)

O suporte a Python no Firebase Functions é notoriamente frágil no Windows. Se o passo acima falhar, **não perca mais tempo com o Firebase para o backend**. Use a arquitetura híbrida, que é muito mais profissional e estável:

1. **Mantenha o Firebase apenas para o Hosting** (Frontend estático), que já está funcionando (`https://comprapublica.web.app`).
2. **Faça o Deploy da API Python no Render.com ou Railway.app** (ambos têm planos gratuitos generosos e suportam Python nativamente sem dor de cabeça).

**Como fazer o Plano B (Exemplo com Render):**

1. Crie uma conta no [Render.com](https://render.com).
2. Crie um novo **Web Service**.
3. Conecte seu repositório GitHub do `PubliCopilot`.
4. Configure:
   - **Build Command:** `pip install -r functions/requirements.txt`
   - **Start Command:** `cd functions && gunicorn app:app` (assumindo que seu arquivo principal se chama `app.py` e a instância do Flask é `app`).
5. O Render vai te dar uma URL (ex: `https://publicopilot-api.onrender.com`).
6. No seu frontend (Hospedado no Firebase), altere a chamada da API para apontar para essa nova URL do Render.

**Por que o Plano B é melhor?**

- Elimina 100% dos erros de `firebase-tools` no Windows.
- O Render lida com o `venv` e as dependências do Python automaticamente.
- Você não precisa brigar com permissões do Google Cloud IAM.
- O tempo de desenvolvimento cai de horas para 10 minutos.

### Resumo da Ação Imediata:

Tente a **Fase 2 + Fase 5** (Service Account JSON). Se em 15 minutos não funcionar, abandone o Firebase Functions e migre o backend Python para o **Render.com** (Plano B), mantendo o frontend no Firebase Hosting. É a rota mais rápida para ter seu Doutorado/Artigo com o sistema 100% no ar.

---

## Atualização 19/07/2026 07h

### Diagnóstico Atual

- `firebase functions:list --project publicopilot-aa662` retorna **tabela vazia**.
- Função `analisar_minuta` **NUNCA foi deployada** (foi removida em algum momento, ou o deploy sempre falhou silenciosamente).
- API `/api/analisar` retorna **404 Not Found** quando chamada de fora.
- Front-end continua funcionando (HTML+CSS+JS deployados).

### Codigo-fonte Corrigido (19/07/2026 07h)

Apos 4 tarefas de qualidade/seguranca, o codigo da Cloud Function esta pronto:

1. **CORS restrito** (`main.py`): `Allow-Origin` agora eh dinamico via whitelist, nao mais `*`
2. **Modelos limpos** (`functions/models/saved/`): 11 arquivos essenciais, 27,35 MB (eram 15, 39,52 MB)
3. **requirements.txt fixado**: `scikit-learn==1.9.0` (compativel com modelos treinados)
4. **Comentario Python 3.12 corrigido para 3.11** (consistente com firebase.json)

### Pendencia Atual (19/07/2026 07h)

O deploy da Cloud Function `analisar_minuta` esta em execucao manual no terminal do usuario.
Aguardando confirmacao de que o deploy foi concluido com sucesso.

Comandos para o terminal (em execucao):

```bash
cd C:\Users\Renato\Documents\Doutorado\PubliCopilot
firebase deploy --only functions --project publicopilot-aa662
```

Apos o deploy, validar com:

```bash
curl -X POST https://comprapublica.web.app/api/analisar ^
  -H "Content-Type: application/json" ^
  -d "{\"texto\": \"OBJETO: Teste de deploy. VIGENCIA: 12 meses.\"}"
```

Se retornar JSON com `score` e `clausulas_encontradas`, o deploy foi bem-sucedido.
