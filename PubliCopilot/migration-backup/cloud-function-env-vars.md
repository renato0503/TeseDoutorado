# Migration Backup: Configuração do Cloud Function antigo (publicopilot)

## Env vars aplicadas no último deploy tentado
Capturadas do output do terminal do Renato em 14/10/2026.

```
NVIDIA_API_KEY=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
```

## Env vars defaults do código (functions/main.py)
```
SKIP_AUTH=0
FIREBASE_PROJECT_ID=<AUTO-PREENCHIDO-EM-DEPLOY>
ALLOWED_ORIGINS=https://publicopilot.web.app,https://publicopilot.firebaseapp.com
MAX_REQ_PER_MIN=1000
ENABLE_AUDIT_LOG=1
```

## Comando de deploy usado (referência)
```
gcloud functions deploy analisar_minuta --gen2 --runtime=python311 --region=us-central1 --source=functions --entry-point=analisar_minuta --trigger-http --memory=512MB --timeout=120s --set-env-vars "NVIDIA_API_KEY=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" --allow-unauthenticated
```

## Após migrar para o novo projeto:
Substituir a URL `publicopilot.web.app` em `ALLOWED_ORIGINS` pelo novo host, ex.:
`ALLOWED_ORIGINS=https://<novo>.web.app,https://<novo>.firebaseapp.com`

## ⚠️ Segurança
A NVIDIA_API_KEY apareceu em log de chat e em chamadas gcloud. **Rotação recomendada após migração.**
Plataforma: https://build.nvidia.com/settings/api-keys
