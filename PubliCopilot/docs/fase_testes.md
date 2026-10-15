# Fase de Testes Multi-Orgão — PubliCopilot

> Documento vivo. Atualizado em **Outubro de 2026**.

Esta fase do PubliCopilot foi desenhada para validação empírica com **4 órgãos públicos parceiros**: **SESP-MT**, **Politec-MT**, **TJPR** e **TJRN**. Cada órgão recebe um conjunto de usuários cadastrados manualmente pelo administrador, com acesso ilimitado à plataforma para rodar análises e gerar editais quantas vezes desejarem, com **telemetria completa** de tudo o que é executado.

---

## 1. Objetivos da Fase

1. **Validar empiricamente** o Copiloto Algorítmico com casos reais de auditoria de minutas de editais em produção.
2. **Coletar telemetria** de uso (login, cliques, execuções, erros) para a tese de doutorado.
3. **Medir utilidade percebida** por pregoeiros, agentes de contratação e autoridades competentes.
4. **Coletar datasets anotados** (analises/{uid}/historico + editais/) para o Modelo B (Risco Contratual via Random Forest + SHAP).

---

## 2. Modelo de Acesso

### Como o usuário é cadastrado

Cadastro **100% manual e offline**, controlado pelo administrador da pesquisa (Renato). Não há auto-cadastro público nem convite aberto — apenas provisioning via:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\caminho\para\serviceAccount.json"
python scripts/admin_create_user.py `
    --modo unico `
    --email maria.silva@sesp.mt.gov.br `
    --nome "Maria Silva" `
    --orgao SESP-MT `
    --perfil pregoeiro `
    --whatsapp "(65) 99999-0001"
```

**Saída:** o script gera uma **senha temporária aleatória** (atende aos requisitos mínimos) que é impressa UMA ÚNICA VEZ. O administrador deve enviar a senha ao usuário por canal seguro (e-mail institucional, WhatsApp, etc.).

Após o primeiro login, o usuário é forçado a redefinir a senha (sinalizado pelo flag `primeiroAcesso: true` e `senhaTemporaria: true`).

### Tipos de perfis suportados

| Perfil               | Uso esperado                                                       |
|----------------------|---------------------------------------------------------------------|
| `pregoeiro`          | Conduz pregoes, avalia minutas, gera editais                       |
| `agente_compras`     | Autua processos, faz ETP, minuta editais                           |
| `gestor`             | Revisa, aprova, dá ciência em análise                             |
| `assessor_juridico`  | Analisa juridicamente, usa o modulo de Avaliacao contrafactual    |
| `autoridade_competente` | Aprova/homologa decisões finais                                  |
| `servidor`           | Outros servidores do orgão (consulta, leitura, curiosidade)         |

### Limites

- **Rate limit:** 1000 req/min por UID (configurável via env var `MAX_REQ_PER_MIN`; definir `0` desativa).
- **Quota:** sem quota diária nesta fase.
- **Anonimo:** o login anônimo **foi removido** do gate principal. Os modulos exigem usuario identificado para haver rastreabilidade.

---

## 3. Schema Firestore

### Coleções

| Coleção | Path | Quem lê | Quem escreve |
|---|---|---|---|
| `usuarios/{uid}` | top-level | próprio uid OU admin | próprio uid (em 1o acesso) OU admin (reprovisionamento) |
| `orgaos/{orgaoId}` | top-level | autenticados | admin |
| `analises/{uid}/historico/{docId}` | subcollection (analises/{uid}) | próprio uid OU admin | próprio uid |
| `editais/{editalId}` | top-level | dono OU admin | autenticado (com `usuarioId == auth.uid`) |
| `logs/{logId}` | top-level | admin | autenticado (best-effort) |

### Usuário (`usuarios/{uid}`)

```json
{
  "nome": "Maria Silva",
  "email": "maria.silva@sesp.mt.gov.br",
  "whatsapp": "(65) 99999-0001",
  "instituicao": "Secretaria de Estado de Seguranca Publica de Mato Grosso",
  "orgaoId": "SESP-MT",
  "orgaoNome": "Secretaria de Estado de Seguranca Publica de Mato Grosso",
  "perfil": "pregoeiro",
  "papel": "usuario",
  "ativo": true,
  "totalAnalises": 0,
  "totalGeracoes": 0,
  "provedor": "password",
  "primeiroAcesso": false,
  "cadastradoPorAdmin": true,
  "senhaTemporaria": true,
  "dataCriacao": "...",
  "ultimoAcesso": "..."
}
```

E recebe custom claims:
```json
{
  "orgaoId": "SESP-MT",
  "perfil": "pregoeiro",
  "admin": false,
  "senhaTemporaria": true,
  "cadastradoPorAdmin": true
}
```

### Orgão (`orgaos/{orgaoId}`)

```json
{
  "orgaoId": "SESP-MT",
  "nome": "Secretaria de Estado de Seguranca Publica de Mato Grosso",
  "sigla": "SESP-MT",
  "estado": "MT",
  "contato_email": "compras@sesp.mt.gov.br",
  "ativo": true,
  "criadoEm": "...",
  "atualizadoEm": "..."
}
```

Os 4 órgãos são populados automaticamente na primeira carga do dashboard admin ou via `python scripts/admin_create_user.py --modo seed-orgaos`.

### Análise (`analises/{uid}/historico/{docId}`)

Métricas de uma execução do módulo de avaliação. Schema completo em `functions/main.py`.

```json
{
  "texto_resumo": "Pregao Eletronico 01/2026 - Contratação de solucao de IA...",
  "score": 78.5,
  "classificacao": "Bom",
  "risco_ml": "baixo",
  "rf_proba": 0.12,
  "clausulas_encontradas": [...],
  "lacunas": ["Não há cláusula de propriedade intelectual"],
  "features_shap": [{"feature": "valor_log", "peso": -0.31}, ...],
  "contrafactuais": ["valor_log"],
  "duracao_ms": 1240,
  "modelo_treinado": true,
  "total_palavras": 312,
  "dataCriacao": "..."
}
```

### Edital gerado (`editais/{editalId}`)

```json
{
  "orgao": "Prefeitura Municipal de X",
  "orgaoId": "SESP-MT",
  "orgaoNome": "Secretaria de Estado de Seguranca Publica de Mato Grosso",
  "usuarioId": "abc123",
  "uasg": "989901",
  "modalidade": "pregao",
  "tipo_contrato": "inovacao",
  "valor": "1500000.00",
  "vigencia": "24 meses",
  "objeto": "Contratacao de solucao de IA...",
  "justificativa": "...",
  "criterio": "menor_preco",
  "requisitos_tecnicos": "...",
  "kpis": "...",
  "pagamento": "30 dias",
  "garantia": "garantia_contratual",
  "penalidades": "Multa de 2%...",
  "minuta": "<texto completo da minuta gerada>",
  "clausulas": [
    {"titulo": "DO OBJETO", "texto": "...", "xai": true, "explicacao": "..."},
    ...
  ],
  "fonte": "nvidia" | "template",
  "metadados": {...},
  "totalClausulas": 12,
  "duracaoMs": 8500,
  "dataCriacao": "..."
}
```

### Log de telemetria (`logs/{logId}`)

Granular — ver seção 4.

---

## 4. Telemetria

A plataforma registra **todo evento relevante** na coleção `logs/` (best-effort, nunca quebra a app):

### Eventos do frontend (`public/js/firebase-init.js` — `registrarEvento()`)

| Tipo                   | Quando                                              | Campos principais                              |
|------------------------|------------------------------------------------------|------------------------------------------------|
| `page_view`            | Carregou landing/modulo_avaliacao/modulo_geracao     | `modulo`, `logado`, `anonimo`                  |
| `login_sucesso`        | Login email/senha ou Google completou                | `anonimo`, `provedor`                          |
| `login_anonimo`        | Login anônimo (depreciado; mantido p/ legado)        | —                                              |
| `login_erro`           | Falha em qualquer modo de login                      | `modo`, `erro`                                 |
| `cadastro_sucesso`     | Auto-cadastro concluiu (não usado em testes)         | `perfil`, `instituicao`                        |
| `cadastro_erro`        | Validação ou Firebase falhou                         | `motivo`, `detalhes`                           |
| `logout`               | Sign-out                                            | `uid`                                          |
| `perfil_atualizado`    | Modal de primeiro acesso salvo                       | `perfil`, `instituicao`, `pulou`               |
| `primeiro_acesso`      | Primeiro login de um usuário recém-criado            | `provedor`, `emailVerificado`                  |
| `avaliar_click`        | Clicou em "Analisar Minuta" no modulo_avaliacao      | `textoQtdChars`, `textoQtdPalavras`            |
| `avaliar_inicio`       | Chamada `POST /api/analisar` iniciou                 | `textoQtdChars`                                |
| `avaliar_sucesso`      | Resposta 200 OK                                      | `score`, `risco_ml`, `rf_proba`, `duracaoMs`, `analiseDocId` |
| `avaliar_erro`         | Qualquer falha                                      | `erro`, `duracaoMs`                            |
| `exemplo_selecionado`  | Clicou num botão "Carregar Exemplo"                  | `exemplo` (tecnologia/inovacao/...)            |
| `gerar_click`          | Clicou em "Gerar Edital" ou "Gerar Clausulas"        | `botao`                                        |
| `gerar_inicio`         | Chamada `POST /api/analisar` (modo geracao) iniciou  | `modo`, `tipo_contrato`, `modalidade`, `valor` |
| `gerar_sucesso`        | Edital gerado e persistido em `editais/`              | `fonte`, `totalClausulas`, `editalDocId`, `duracaoMs` |
| `gerar_erro`           | Falha na geração                                     | `erro`, `status`                               |
| `carregar_exemplo`     | Botão "Carregar Exemplo" no modulo_geracao            | `modulo`                                       |

### Eventos do backend (`functions/main.py` — `_registrar_audit_log()`)

| Tipo           | Quando                                       | Campos                                          |
|----------------|----------------------------------------------|-------------------------------------------------|
| `api_analisar` | Toda chamada à `/api/analisar`               | `modo` (avaliacao/geracao), `statusCode`, `duracaoMs`, `subtipo`, `score`, `risco_ml`, `clausulasQtd`, `lacunasQtd`, `ip`, `userAgent`, `origin`, `orgaoId` |

### Privacidade / LGPD

- **Nenhum dado sensível** (CPF, RG, dados de proponentes reais) é coletado.
- O `texto_resumo` em `analises/` é truncado em **300 caracteres**.
- `userAgent` e `referer` são coletados em logs para diagnosticar problemas técnicos.
- IPs são coletados apenas para rate-limit / auditoria de segurança.
- Logs nunca contêm a senha do usuário (campo `senha` é redacted automaticamente).

---

## 5. Procedimento Operacional

### Antes do teste
1. Confirmar com cada orgão: lista nominal + e-mail institucional + perfil.
2. Acordo de uso assinado (LGPD + termo de uso do produto de pesquisa).
3. Provisionar todos os usuários via `admin_create_user.py` (use um JSON para batch).
4. Verificar que os 4 `orgaos/` estão populados (`--modo seed-orgaos`).
5. Enviar credenciais por canal seguro.

### Durante o teste
- Acessar `https://publicopilot.web.app/dashboard/` diariamente.
- Filtrar por orgão.
- Exportar CSV semanal.
- Investigar logs de erro com prioridade.

### Após o teste
1. **Anestesia**: marcar `usuarios/{uid}.ativo = false`.
2. Snapshot final: exportar logs + análises + editais.
3. Anotar feedback qualitativo dos usuários.
4. Desativar/limpar a coleção `logs/` se necessário.

---

## 6. Comandos Úteis

### Provisionar em lote (exemplo)

```bash
cat > usuarios_sesp.json <<EOF
[
  {"email":"pregoeiro1@sesp.mt.gov.br","nome":"Pregoeiro 1","orgao":"SESP-MT","perfil":"pregoeiro"},
  {"email":"agente1@sesp.mt.gov.br","nome":"Agente 1","orgao":"SESP-MT","perfil":"agente_compras"}
]
EOF
python scripts/admin_create_user.py --arquivo usuarios_sesp.json
```

### Inicializar orgãos (idempotente)

```bash
python scripts/admin_create_user.py --modo seed-orgaos
```

### Listar 20 últimas execuções por orgão (Firestore console)

```
Collection: logs
Filters:
  - tipo == 'api_analisar'
  - orgaoId == 'SESP-MT'
  - sucesso == true
Order by: dataCriacao DESC
Limit: 20
```

### Deploy

```bash
firebase deploy --only firestore:rules,firestore:indexes
firebase deploy --only functions
firebase deploy --only hosting
```

---

## 7. Próximos Passos (fora do escopo desta sprint)

- [ ] Painel de avaliação por especialista (pesquisador preencher notas Kappa, IVC).
- [ ] Export do dataset anotado em CSV para Papers 16/17.
- [ ] Cron job de backup semanal para GCS.
- [ ] Migrar para Cloud Run (sai do plano Blaze e suporta escala).
- [ ] Substituir login anônimo por fluxo de "lead" com captura de e-mail.
