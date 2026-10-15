# Diagrama 04 — Módulo de Geração de Cláusulas

**Endpoint:** `POST /api/analisar_minuta` com `{ modo: "geracao" }`

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#1E293B','primaryTextColor':'#F1F5F9','primaryBorderColor':'#2EC4B6','lineColor':'#475569'}}}%%
flowchart TB
    subgraph FRONTEND["🌐 FRONTEND — modulo_geracao/index.html"]
        G1["📝 Acessa /modulo_geracao/<br/>(requer login)"]
        G2{"Modo<br/>selecionado?"]
        G1 --> G2
        G2 -->|📚 Templates| G3["Seleciona tipo:<br/>Inovação · Sustentabilidade<br/>Tecnologia · ESG"]
        G3 --> G4["Seleciona subtipo<br/>da cláusula"]
        G2 -->|🤖 NVIDIA IA| G5["Preenche contexto:<br/>tipo, valor, órgão,<br/>descrição do objeto"]
        G2 -->|✏️ Reescrita| G6["Insere cláusula<br/>original para reescrever"]
    end

    subgraph CF_GERACAO["☁️ CLOUD FUNCTION — _executar_geracao()"]
        CG1["Recebe body com<br/>{ modo:'geracao', tipo, descricao }"]
        CG1 --> CG2{"Tipo de<br/>geração?"]
        CG2 -->|template| CG3["Busca em<br/>models/predefined_clauses.py<br/>ou templates inline"]
        CG3 --> CG4["Aplica variáveis:<br/>{ ORGAO, VALOR, DATA }<br/>no template"]
        CG2 -->|nvidia| CG5["NVIDIA NIM API Client<br/>gerar_minuta()"]
        CG5 --> CG6["Prompt: contexto + tipo<br/>+ Lei 14.133/2021"]
        CG6 --> CG7["Parse da resposta<br/>JSON: { clausulas }"]
        CG2 -->|reescrita| CG8["NVIDIA NIM API Client<br/>gerar_sugestao_reescrita()"]
        CG8 --> CG9["Prompt: cláusula original<br/>+ melhores práticas<br/>+ LGPD + 14.133"]
        CG9 --> CG7
        CG4 --> CG10["Montar minuta + metadata"]
        CG7 --> CG10
    end

    subgraph NVIDIA["🤖 NVIDIA NIM API — build.nvidia.com"]
        NV["build.nvidia.com<br/>/v1/chat/completions<br/>Model: Llama-4-Maverick"]
        NV_KEY["NVIDIA_API_KEY<br/>(env var)"]
        CG5 -.-> NV
        CG8 -.-> NV
        NV -.-> NV_KEY
    end

    subgraph SAVE["💾 PERSISTÊNCIA"]
        CG10 --> S1["salvarGeracao(dados)<br/>Firestore: editais/{autoId}"]
        S1 --> S2["Campos: orgaoId, titulo,<br/>tipo, valor, clausulasGeradas,<br/>usuarioId, dataCriacao"]
        S2 --> S3["registrarEvento('gerar_sucesso')"]
    end

    subgraph RESP["📤 RESPONSE"]
        CG10 --> R1["HTTP 200<br/>{ modo:'geracao',<br/>minuta, clausulas,<br/>metadados }"]
        R1 --> R2["Frontend exibe<br/>cláusula formatada + preview"]
        R2 --> R3["✏️ Usuário pode<br/>editar cláusula"]
        R3 --> R4["📥 Exportar<br/>como .txt"]
    end

    style FRONTEND fill:#1E293B,stroke:#2EC4B6,color:#F1F5F9
    style CF_GERACAO fill:#1E293B,stroke:#F59E0B,color:#F1F5F9
    style NVIDIA fill:#1E293B,stroke:#22C55E,color:#F1F5F9
    style SAVE fill:#1E293B,stroke:#EC4899,color:#F1F5F9
    style RESP fill:#1E293B,stroke:#8B5CF6,color:#F1F5F9
```

**Tags de arquivo:** `docs/diagrams/04-geracao.md`
