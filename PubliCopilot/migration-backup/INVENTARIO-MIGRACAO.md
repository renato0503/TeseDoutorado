# Inventário de Migração — publicopilot (comercial@cerradofinancas.com.br → gestor.renatorosa@gmail.com)

**Data:** 15/10/2026  
**Operação:** Apagar projeto `publicopilot` antigo e recriar sob `gestor.renatorosa@gmail.com`

## ✅ O que foi capturado

| Item | Onde está | Como recuperar |
|---|---|---|
| Código fonte completo (PubliCopilot, scripts, docs) | Git local (6 commits à frente de `9da629e`) | Já em `C:\Users\Renato\Documents\Doutorado\PubliCopilot` |
| 10 Auth users (incluindo `gestor.renatorosa@gmail.com`) | `migration-backup/auth-users.json` | `firebase auth:import` no novo projeto (requer plan Blaze no destino) |
| Env vars do Cloud Function (NVIDIA_API_KEY) | `migration-backup/cloud-function-env-vars.md` | Re-aplicar no `--set-env-vars` do `gcloud functions deploy` |
| 2 commits já deployados no Hosting | Git | Re-deploy com `firebase deploy --only hosting` |

## ❌ O que NÃO foi possível capturar (billing fechado)

| Item | Por quê perdeu | Solução |
|---|---|---|
| ML models `.pkl` (9 arquivos, ~27 MB) no `functions/models/saved/` | Bucket `gcf-sources-432118179013-us-central1` está com `AccessDenied: billing closed` | **Retreinar** via `python functions/models/train_models.py` |
| Training data (PNCP, ~100k contratos) em `C:\Users\Renato\Documents\Doutorado\dados\processed\` | Pasta `dados/` não existe localmente | Re-extrair via `scripts/pncp_pipeline/orquestrador.py` ou da fonte original |
| Firestore data (análises, editais, logs) | `firestore:export` precisa de bucket GCS com billing aberto | Re-criar do zero (provavelmente não tem dados críticos ainda — 10 usuários, mas sem análises/audit significativos) |

## 🔄 Passo-a-passo para o NOVO projeto

### Antes de apagar o antigo:

1. **Verifique se tem os `.pkl` em outro lugar** (HD externo, Google Drive). Procure por `random_forest.pkl` no seu PC inteiro:
   ```powershell
   Get-ChildItem -Recurse -Filter "random_forest.pkl" C:\ | Select-Object -First 5 FullName
   ```
2. Salve a planilha/CSV de `pncp_contratos_full.csv` se tiver.
3. **Garanta que o billing do NOVO projeto está OPEN e funcionando** (cartão válido, billing account ativo).

### Apagar o antigo:

1. Acesse `https://console.firebase.google.com/project/publicopilot/settings/general`
2. Role até o final, clique em **"Delete project"**
3. Confirme digitando o ID do projeto

### Criar o NOVO projeto:

1. Acesse `https://console.firebase.google.com/`
2. **Add project** → escolha ID (sugestão: `publicopilot-v2` ou `publi-copilot-tese`)
3. Ativar **Blaze** logo após criar
4. Habilitar APIs no GCP:
   ```bash
   gcloud config set project <NOVO_ID>
   gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com firestore.googleapis.com
   ```

### Re-deploy no novo projeto:

1. Atualizar `firebase-init.js` com o novo `apiKey` (pegar em Project Settings → Web app config)
2. Atualizar `.firebaserc` com novo ID
3. Deploy:
   ```bash
   firebase login --reauth   # como gestor.renatorosa@gmail.com
   firebase use <NOVO_ID>
   firebase deploy --only firestore:rules,firestore:indexes
   firebase deploy --only functions
   firebase deploy --only hosting
   ```

### Recriar usuários testadores:

Use `scripts/admin_create_user.py` apontando para o novo projeto (via `GOOGLE_APPLICATION_CREDENTIALS` ou `--credentials` com service account do novo projeto).

## ⚠️ Riscos

- **Histórico de análises/editais será perdido** (não exportável). Se quiser, copie manualmente do dashboard → Exportar CSV antes de apagar.
- **NVIDIA_API_KEY exposta em chat** — recomendo rotacionar em `https://build.nvidia.com/settings/api-keys` antes do novo deploy.
- **Custom claims (admin/orgaoId) dos 10 usuários não migram** — precisam ser re-aplicados via `admin_create_user.py` ou manualmente no console.
