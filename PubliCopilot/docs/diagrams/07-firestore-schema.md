# Diagrama 07 — Schema do Firestore + Índices

**Collections:** `usuarios/`, `orgaos/`, `editais/`, `analises/`, `logs/`

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#1E293B','primaryTextColor':'#F1F5F9','primaryBorderColor':'#2EC4B6','lineColor':'#475569'}}}%%
erDiagram
    usuarios {
        string uid PK "Firebase Auth UID"
        string email "Email do usuário"
        string nome "Nome completo"
        string papel "usuario | admin"
        string perfil "pregoeiro | servidor | pesquisador"
        string orgaoId "SESP-MT | POLITEC-MT | TJPR | TJRN | gestor"
        string provedor "password | google.com | anonymous"
        bool ativo "Conta ativa?"
        bool primeiroAcesso "Precisa completar perfil?"
        int totalAnalises "Contador de análises"
        string whatsapp "DDD + número"
        string instituicao "Nome da instituição"
        timestamp dataCriacao "Server timestamp"
        timestamp ultimoAcesso "Server timestamp"
        timestamp dataAtualizacao "Server timestamp"
    }

    orgaos {
        string orgaoId PK "SESP-MT | POLITEC-MT | TJPR | TJRN"
        string nome "Nome completo do órgão"
        string sigla "Sigla (ex: SESP-MT)"
        string estado "MT | PR | RN"
        string tipo "secretaria | politec | tribunal"
        string regiao "Centro-Oeste | Sul | Nordeste"
        bool ativo "Órgão ativo?"
        timestamp dataCriacao "Server timestamp"
    }

    analises {
        string analiseId PK "Auto-ID Firestore"
        string uid FK "usuarios.uid — criador"
        string orgaoId "Órgão do usuário no momento"
        string texto "Texto do edital"
        number score "0-100 — score heurístico"
        string risco "baixo | medio | alto"
        string classificacao "Classificação do risco"
        array lacunas "Lista de lacunas detectadas"
        array clausulas "Cláusulas encontradas"
        number rf_proba "Probabilidade RF (0-1)"
        number duracao_ms "Tempo de processamento"
        timestamp dataCriacao "Server timestamp"
    }

    editais {
        string editalId PK "Auto-ID Firestore"
        string orgaoId "Órgão"
        string titulo "Título do edital"
        string tipo "inovacao | sustentabilidade | tecnologia"
        number valor "Valor estimado"
        array clausulasGeradas "Cláusulas recomendadas"
        string usuarioId FK "usuarios.uid — criador"
        timestamp dataCriacao "Server timestamp"
    }

    logs {
        string logId PK "Auto-ID Firestore"
        string tipo "page_view | login_sucesso | avaliar_sucesso | avaliar_erro | logout | api_analisar | ..."
        string uid "UID do usuário (ou 'anon')"
        string email "Email do usuário"
        string orgaoId "Órgão do usuário"
        object claims "Custom claims: {admin, papel, orgaoId}"
        string modo "avaliacao | geracao"
        number duracao_ms "Duração da operação"
        string status "sucesso | erro"
        string ip "IP do cliente (request.headers['X-Forwarded-For'])"
        string userAgent "User-Agent do navegador"
        object extras "Dados extras dependentes do evento"
        timestamp timestamp "Server timestamp — índice DESC"
    }

    usuarios ||--o{ analises : "cria"
    usuarios ||--o{ editais : "cria"
    orgaos ||--o{ analises : "agrupa_por_orgao"
    orgaos ||--o{ editais : "agrupa_por_orgao"
    orgaos ||--o{ logs : "gera_eventos"
    usuarios ||--o{ logs : "gera_eventos"
```

## Índices Compostos (firestore.indexes.json)

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#1E293B','primaryTextColor':'#F1F5F9','primaryBorderColor':'#2EC4B6','lineColor':'#475569'}}}%%
flowchart LR
    subgraph IDX["📑 Composite Indexes — firestore.indexes.json"]
        direction TB
        I1["Collection: analises<br/>Fields: orgaoId ASC + dataCriacao DESC<br/>Query: WHERE orgaoId==? ORDER BY dataCriacao DESC"]
        I2["Collection: analises<br/>Fields: uid ASC + dataCriacao DESC<br/>Query: WHERE uid==? ORDER BY dataCriacao DESC"]
        I3["Collection: editais<br/>Fields: orgaoId ASC + dataCriacao DESC<br/>Query: WHERE orgaoId==? ORDER BY dataCriacao DESC"]
        I4["Collection: editais<br/>Fields: usuarioId ASC + dataCriacao DESC<br/>Query: WHERE usuarioId==? ORDER BY dataCriacao DESC"]
        I5["Collection: logs<br/>Fields: orgaoId ASC + timestamp DESC<br/>Query: WHERE orgaoId==? ORDER BY timestamp DESC"]
        I6["Collection: logs<br/>Fields: uid ASC + timestamp DESC<br/>Query: WHERE uid==? ORDER BY timestamp DESC"]
        I7["Collection: logs<br/>Fields: tipo ASC + timestamp DESC<br/>Query: WHERE tipo==? ORDER BY timestamp DESC"]
    end
    style IDX fill:#1E293B,stroke:#8B5CF6,color:#F1F5F9
```

**Tags de arquivo:** `docs/diagrams/07-firestore-schema.md`
