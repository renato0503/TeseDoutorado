# Diagramas — PubliCopilot v3.0

Documentação visual da arquitetura e fluxos do sistema. Todos renderizam nativamente no GitHub e VS Code (extensão Mermaid).

## Índice

| # | Diagrama | Tipo | Descrição |
|---|---|---|---|
| 01 | [Arquitetura Geral](./01-arquitetura-geral.md) | `flowchart TB` | Stack completa: Browser → Firebase → Cloud Function → ML Models → NVIDIA |
| 02 | [Autenticação](./02-autenticacao.md) | `sequenceDiagram` | 5 casos: cadastro, login órgão, login admin, API call, anônimo |
| 03 | [Avaliação de Minutas](./03-avaliacao.md) | `flowchart TB` | Pipeline completo: input → CORS/auth/rate-limit → ML → audit → response |
| 04 | [Geração de Cláusulas](./04-geracao.md) | `flowchart TB` | 3 modos: templates, NVIDIA NIM, reescrita |
| 05 | [Dashboard Administrativo](./05-dashboard.md) | `flowchart TB` | Métricas, filtros, tabs, cards por órgão, CSV export |
| 06 | [API Flow — Análise](./06-api-analise.md) | `sequenceDiagram` | Sequência cronológica: Browser → CORS → Auth → Rate Limit → ML → Firestore |
| 07 | [Schema Firestore](./07-firestore-schema.md) | `erDiagram` | Entidades + relacionamentos + índices compostos |
| 08 | [Telemetria](./08-telemetria.md) | `flowchart TB` | Sistema de eventos: coleta → tipos → registro → consumo |

## Como usar

Abra qualquer arquivo `.md` no VS Code com a extensão **Mermaid** (ou no GitHub) para visualizar o diagrama renderizado.

Alternativamente, abra os arquivos no repositório diretamente pelo GitHub:
```
https://github.com/renato0503/TeseDoutorado/blob/main/PubliCopilot/docs/diagrams/01-arquitetura-geral.md
```

## Nomenclatura

- **Actor:** 👤 Usuário, 🌐 Browser
- **Sistema:** 🔥 Firebase, ☁️ Cloud Function, 🤖 ML Models, 📄 Firestore
- **Estado:** ✅ Sucesso, ❌ Erro, ⚠️ Warning
- **Direção:** `TB` = top-bottom, `LR` = left-right
