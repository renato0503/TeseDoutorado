# Checklist de Seguranca — PubliCopilot

**Ultima atualizacao:** 23/07/2026

---

## Antes do Deploy (toda vez)

- [ ] `ADMIN_SETUP_SECRET` configurado como env var no Firebase Console
- [ ] `key.json` ou qualquer service account key **NÃO** versionada no git
- [ ] `.gitignore` contem `key.json`, `credentials.json`, `__pycache__/`
- [ ] CORS restrito a whitelist em `main.py` (sem `*`)
- [ ] `SKIP_AUTH=0` (nunca deployar com `SKIP_AUTH=1`)
- [ ] `firebase-admin` listado em `requirements.txt`
- [ ] Nenhum UID, email ou senha hardcoded em arquivos publicos (`public/js/`)

---

## No Primeiro Deploy da Cloud Function

- [ ] Rodar `firebase deploy --only functions` e confirmar saida sem erros
- [ ] Rodar `firebase functions:list` e confirmar que `analisar_minuta` aparece como `READY`
- [ ] Testar endpoint sem token: `curl -X POST https://publicopilot.web.app/api/analisar` deve retornar **401**
- [ ] Testar endpoint com token valido: deve retornar **200** com `score` e `rf_proba`
- [ ] Verificar logs da function no Firebase Console (sem erros de import/pickle)

---

## Nos Primeiros 5 Minutos Apos Deploy Bem-Sucedido

- [ ] **Remover `ADMIN_SETUP_SECRET`** das variaveis de ambiente no Firebase Console
- [ ] **Deletar `key.json`** do disco local (service account key)
- [ ] Limpar versoes antigas do Artifact Registry:
  ```bash
  gcloud artifacts docker images list us-central1-docker.pkg.dev/publicopilot/cloud-run-source-deploy/
  gcloud artifacts docker images delete IMAGEM_ANTIGA --delete-tags --quiet
  ```
- [ ] Verificar Firestore Rules com simulacao:
  ```bash
  # No Firebase Console > Firestore > Rules, usar botao "Simulate"
  # Testar leitura nao-autenticada em /usuarios/{uid}
  ```

---

## Rotina Semanal

- [ ] Revisar logs de acesso no Firebase Console (Authentication > Usuarios)
- [ ] Verificar custos no GCP Billing: https://console.cloud.google.com/billing
  - **Esperado:** $0.00 se dentro do free tier
- [ ] `ADMIN_SETUP_SECRET` se ainda ativo, rotacionar (alterar valor)

---

## Emergencia (Vazamento Detectado)

| Acao | Prioridade | Como Fazer |
|------|-----------|------------|
| Rotacionar apiKey | Imediata | Firebase Console > Project Settings > General > Web API Key > Regenerate |
| Revogar service account | Imediata | GCP Console > IAM > Service Accounts > Deletar chave comprometida |
| Revisar Firestore | Urgente | Firestore > Data > Procurar documentos criados sem autorizacao |
| Deletar e recriar Cloud Function | Urgente | `firebase functions:delete analisar_minuta` e redeployar |
| Notificar usuarios | Se houver | Recolher tokens comprometidos, forcar logout geral |

---

## Checklist Git (Antes de Commitar)

```bash
git diff --cached --name-only | grep -E 'key\.json|credentials\.json|\.env|\.pem$'
# Se retornar algo, NAO COMMITAR — adicionar ao .gitignore
```

**Arquivos que NUNCA devem ser commitados:**
- `**/key.json`
- `**/credentials.json`
- `**/*service-account*.json`
- `**/.env`
- `**/__pycache__/`
- `**/*.pyc`

---

## Referencias

- https://firebase.google.com/docs/projects/iam/overview
- https://cloud.google.com/functions/docs/securing
- https://cloud.google.com/artifact-registry/docs/clean-up
