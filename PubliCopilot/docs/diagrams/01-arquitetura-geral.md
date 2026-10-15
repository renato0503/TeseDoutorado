# Diagrama 01 — Arquitetura Geral do Sistema

**Stack:** Firebase Hosting + Cloud Functions (Python 3.11 Gen2) + Firestore + Firebase Auth + NVIDIA NIM API

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#1E293B','primaryTextColor':'#F1F5F9','primaryBorderColor':'#2EC4B6','lineColor':'#475569','secondaryColor':'#334155','tertiaryColor':'#0F172A'}}}%%
flowchart TB
    subgraph Browser["🌐 NAVEGADOR (Cliente)"]
        L["Landing Page /index.html"]
        MA["Módulo Avaliação<br/>/modulo_avaliacao/"]
        MG["Módulo Geração<br/>/modulo_geracao/"]
        D["Dashboard Admin<br/>/dashboard/"]
        AUTH["auth.js<br/>PubliAuth + Modal"]
        TEL["firebase-init.js<br/>registrarEvento()"]
    end

    subgraph Firebase["🔥 FIREBASE (Google Cloud)"]
        subgraph Hosting["Firebase Hosting"]
            STATIC["52 arquivos estáticos<br/>publicopiloto.web.app"]
        end
        subgraph AuthSvc["Firebase Auth"]
            AUTH_SERVICE["firebase-auth<br/>signInWithEmailAndPassword()<br/>signInAnonymously()<br/>Google OAuth"]
            CLAIMS["Custom Claims<br/>admin, orgaoId, perfil"]
        end
        subgraph FirestoreDB["Cloud Firestore"]
            USERS["usuarios/{uid}"]
            ORGS["orgaos/{orgaoId}"]
            EDITALS["editais/{editalId}"]
            ANALYSES["analises/{uid}/{id}"]
            LOGS["logs/{logId}"]
        end
    end

    subgraph CloudFunc["⚙️ CLOUD FUNCTION Gen2<br/>analisar_minuta"]
        CF_ENTRY["@functions_framework.http<br/>analisar_minuta()"]
        CORS_MW["CORS Middleware<br/>ALLOWED_ORIGINS whitelist"]
        AUTH_CF["_validar_token_firebase()<br/>verify_id_token()"]
        RATE_LIM["_verificar_rate_limit()<br/>1000 req/min por UID"]
        PIPELINE["Pipeline ML"]
        AUDIT["_registrar_audit_log()<br/>Firestore logs/"]
    end

    subgraph ML_MODELS["🤖 MODELOS ML (Python)"]
        RF["Random Forest 100 árvores<br/>models/saved/random_forest.pkl"]
        IF["Isolation Forest<br/>models/saved/isolation_forest.pkl"]
        SHAP["SHAP TreeExplainer<br/>models/saved/shap_explainer.pkl"]
        TFIDF["TF-IDF Vectorizer<br/>models/saved/tfidf_vectorizer.pkl"]
        PREPROC["preprocessor.py<br/>extrair_clausulas()<br/>detectar_lacunas()<br/>calcular_score()"]
    end

    subgraph NVIDIA["🤖 NVIDIA NIM API"]
        NV_API["build.nvidia.com<br/>Llama/NeMo + AI Endpoint"]
        NV_KEY["NVIDIA_API_KEY<br/>(env var)"]
    end

    %% Conexões
    L --> AUTH
    MA --> AUTH
    MG --> AUTH
    D --> AUTH

    AUTH --> AUTH_SERVICE
    AUTH_SERVICE --> CLAIMS
    AUTH_SERVICE -.->|verify_id_token| CF_ENTRY

    MA -->|POST /api/analisar_minuta| CF_ENTRY
    MG -->|POST /api/analisar_minuta<br/>modo:geracao| CF_ENTRY

    CF_ENTRY --> CORS_MW --> AUTH_CF --> RATE_LIM --> PIPELINE

    PIPELINE --> PREPROC
    PIPELINE -->|se modelos disponíveis| RF
    PIPELINE -->|se modelos disponíveis| IF
    PIPELINE -->|se modelos disponíveis| SHAP
    PIPELINE -->|text vectorization| TFIDF

    PIPELINE -->|geração de cláusulas| NV_API
    NV_API -.-> NV_KEY

    PIPELINE --> AUDIT
    AUDIT -.->|set(logs/{id})| LOGS

    MA -->|salvarGeracao()| EDITALS
    MA -->|registrarEvento()| TEL
    TEL -.->|add(logs/)| LOGS

    D -->|read| USERS
    D -->|read| ORGS
    D -->|read| ANALYSES
    D -->|read| EDITALS
    D -->|admin only| LOGS

    style Browser fill:#1E293B,stroke:#2EC4B6,color:#F1F5F9
    style Firebase fill:#1E293B,stroke:#8B5CF6,color:#F1F5F9
    style CloudFunc fill:#1E293B,stroke:#F59E0B,color:#F1F5F9
    style ML_MODELS fill:#1E293B,stroke:#EC4899,color:#F1F5F9
    style NVIDIA fill:#1E293B,stroke:#22C55E,color:#F1F5F9
    style Hosting fill:#0F172A,stroke:#475569,color:#94A3B8
    style AuthSvc fill:#0F172A,stroke:#475569,color:#94A3B8
    style FirestoreDB fill:#0F172A,stroke:#475569,color:#94A3B8
```

**Tags de arquivo:** `docs/diagrams/01-arquitetura-geral.md`
