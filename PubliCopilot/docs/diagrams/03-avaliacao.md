# Diagrama 03 — Módulo de Avaliação de Minutas

**Endpoint:** `POST /api/analisar_minuta` (Cloud Function `analisar_minuta`)

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#1E293B','primaryTextColor':'#F1F5F9','primaryBorderColor':'#2EC4B6','lineColor':'#475569'}}}%%
flowchart TB
    subgraph FRONTEND["🌐 FRONTEND — modulo_avaliacao/index.html"]
        A1["📋 Usuário acessa<br/>/modulo_avaliacao/"]
        A2{"Logado?"]
        A2 -->|NÃO| A3["PubliAuth.loginAnonimo()<br/>ou PubliAuth.abrirLogin()"]
        A2 -->|SIM| A4["UI pronta"]
        A3 --> A4
        A4 --> A5["Seleciona exemplo<br/>(opcional)"]
        A5 --> A6["Ou cola texto próprio<br/>+ informa valor (R$)"]
        A6 --> A7["Clica <b>Avaliar Minuta</b>"]
        A7 --> A8["registrarEvento('avaliar_click')"]
        A8 --> A9["PubliAuth.getIdToken()"]
        A9 --> A10["📡 POST /api/analisar_minuta<br/>Bearer {token}<br/>{ texto, valor }"]
    end

    subgraph CF_GATE["☁️ CLOUD FUNCTION — analisar_minuta()"]
        C1["CORS check<br/>OPTIONS preflight"]
        C1 --> C2["_obter_uid_email_claims()<br/>verify_id_token()"]
        C2 --> C3{"Token<br/>válido?"]
        C3 -->|NÃO| C4["❌ HTTP 401<br/>{erro: 'Token ausente/inválido'}"]
        C3 -->|SIM| C5["_verificar_rate_limit(uid)<br/>1000 req/min"]
        C5 --> C6{"Rate limit<br/>ok?"]
        C6 -->|NÃO| C7["❌ HTTP 429<br/>{erro: 'Limite excedido'}"]
        C6 -->|SIM| C8["_extrair_dados(request)<br/>parse JSON/form"]
        C8 --> C9{"Texto<br/>presente?"]
        C9 -->|NÃO| C10["❌ HTTP 400<br/>{erro: 'Informe o texto'}"]
    end

    subgraph PIPELINE_ML["⚙️ PIPELINE ML — analisar_risco_contratual()"]
        C9 -->|SIM| P1["extrair_clausulas(texto)<br/>🔍 16 regex patterns<br/>Lei 14.133/2021"]
        P1 --> P2["detectar_lacunas(texto)<br/>⚠️ Heurística: vigência,<br/>pagamento, garantia, etc."]
        P2 --> P3["calcular_score(clausulas, lacunas)<br/>📊 Score heurístico 0-100"]
        P3 --> P4{"Modelos<br/>disponíveis?"]
        P4 -->|NÃO| P5["✅ Fallback heurístico<br/>score + lacunas<br/>(sem ML)"]
        P4 -->|SIM| P6["detectar_anomalia(texto)<br/>⚡ Isolation Forest<br/>TF-IDF 500 features"]
        P6 --> P7["_extrair_features_ml()<br/>7 features: valor_log,<br/>vigencia_log, complexidade, etc."]
        P7 --> P8["rf.predict_proba(features_scaled)<br/>🌲 Random Forest<br/>100 árvores"]
        P8 --> P9["explainer.shap_values()<br/>📈 SHAP TreeExplainer<br/>top-3 features"]
        P9 --> P10["_gerar_contrafactual()<br/>⚖️ Contrafactuais<br/>normativos Lei 14.133"]
        P10 --> P11["Montar payload JSON"]
        P5 --> P11
        P11 --> P12["gerar_recomendacoes()<br/>⚖️ Recomendações com<br/>fundamento jurídico"]
        P12 --> P13["gerar_explicacoes_clausulas()<br/>💡 Explicações por cláusula"]
    end

    subgraph AUDIT_LOG["📝 AUDIT LOG"]
        P13 --> AL["_registrar_audit_log(<br/>  tipo:'api_analisar',<br/>  uid, email, orgaoId,<br/>  duracao_ms, status,<br/>  extras:{score, risco}"]
        AL --> AL2["Firestore: set(logs/{id}, {...})"]
    end

    subgraph RESPONSE["📤 RESPONSE"]
        P13 --> R1["HTTP 200 OK"]
        R1 --> R2["Payload JSON:<br/>{ score, risco, classificacao,<br/>clausulas_encontradas,<br/>lacunas, recomendacoes,<br/>rf_proba, features_shap,<br/>contrafactuais, metricas_treino }"]
    end

    subgraph FRONTEND_RET["🌐 FRONTEND — Callback"]
        R2 --> F1["registrarEvento('avaliar_sucesso')<br/>{ score, risco, lacunasQtd }"]
        F1 --> F2["UI: exibe score badge<br/>+ lista de lacunas<br/>+ recomendações"]
        F2 --> F3["salvarGeracao() opcional<br/>→ Firestore editais/{id}"]
    end

    C4 --> RESPONSE
    C7 --> RESPONSE
    C10 --> RESPONSE
    style FRONTEND fill:#1E293B,stroke:#2EC4B6,color:#F1F5F9
    style CF_GATE fill:#1E293B,stroke:#F59E0B,color:#F1F5F9
    style PIPELINE_ML fill:#1E293B,stroke:#8B5CF6,color:#F1F5F9
    style AUDIT_LOG fill:#1E293B,stroke:#EC4899,color:#F1F5F9
    style RESPONSE fill:#1E293B,stroke:#22C55E,color:#F1F5F9
    style FRONTEND_RET fill:#1E293B,stroke:#2EC4B6,color:#F1F5F9
    style C4 fill:#7f1d1d,stroke:#EF4444,color:#F1F5F9
    style C7 fill:#7f1d1d,stroke:#EF4444,color:#F1F5F9
    style C10 fill:#7f1d1d,stroke:#EF4444,color:#F1F5F9
```

**Tags de arquivo:** `docs/diagrams/03-avaliacao.md`
