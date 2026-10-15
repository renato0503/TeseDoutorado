# Diagrama 05 — Dashboard Administrativo

**Tela:** `public/dashboard/index.html` — acesso restrito a `admin:true`

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'primaryColor':'#1E293B','primaryTextColor':'#F1F5F9','primaryBorderColor':'#2EC4B6','lineColor':'#475569'}}}%%
flowchart TB
    subgraph ENTRY["🚪 ENTRY — dashboard/index.html"]
        D1["Acessa /dashboard/"]
        D1 --> D2{"isAdmin()?"]
        D2 -->|NÃO| D3["⛔ Acesso negado<br/>redirect /"]
        D2 -->|SIM| D4["✅ Carrega dashboard"]
    end

    subgraph METRICS["📊 CARDÁPIO DE MÉTRICAS"]
        D4 --> M1["📈 TotalUsuarios<br/>COUNT(usuarios/)"]
        D4 --> M2["📋 TotalAnalises<br/>COUNT(analises/)"]
        D4 --> M3["📄 TotalEditais<br/>COUNT(editais/)"]
        D4 --> M4["🏆 ScoreMédio<br/>AVG(analises.score)"]
        D4 --> M5["⚠️ RiscoAlto<br/>COUNT(analises WHERE risco='alto')"]
        D4 --> M6["📻 Eventos24h<br/>COUNT(logs WHERE timestamp>24h)"]
    end

    subgraph FILTER_ORGAO["🎛️ FILTRO POR ÓRGÃO"]
        M1 --> F1["Dropdown: Todos | SESP-MT<br/>| POLITEC-MT | TJPR | TJRN"]
        F1 --> F2["Firestore: WHERE orgaoId=={filtro}<br/>para todas as tabelas"]
    end

    subgraph TABS["📑 ABAS — tabelas filtradas"]
        F2 --> T1["👥 Aba: Usuários"]
        F2 --> T2["📋 Aba: Análises"]
        F2 --> T3["📄 Aba: Editais"]
        F2 --> T4["📋 Aba: Logs"]

        T1 --> T1D["uid · nome · email<br/>órgão · perfil · provedor<br/>· último acesso"]
        T2 --> T2D["uid · data · score<br/>risco · #lacunas · duração"]
        T3 --> T3D["órgão · tipo · valor<br/>cláusulas geradas · data"]
        T4 --> T4D["tipo · uid · email<br/>timestamp · status · IP"]
    end

    subgraph ORG_CARDS["🏛️ CARDS POR ÓRGÃO"]
        F2 --> OC1["🏛️ SESP-MT<br/>clickable"]
        F2 --> OC2["🏛️ POLITEC-MT<br/>clickable"]
        F2 --> OC3["🏛️ TJPR<br/>clickable"]
        F2 --> OC4["🏛️ TJRN<br/>clickable"]
        OC1 --> OCD["Filtra todas as tabelas<br/>WHERE orgaoId='SESP-MT'"]
        OC2 --> OCD
        OC3 --> OCD
        OC4 --> OCD
        OCD --> OCD2["Detalha drill-down<br/>por órgão selecionado"]
    end

    subgraph EXPORT["📥 EXPORTAÇÃO CSV"]
        T1D --> E1["Botão: Exportar CSV"]
        T2D --> E1
        T3D --> E1
        T4D --> E1
        E1 --> E2["scope: usuarios | analises<br/>| editais | logs | tudo"]
        E2 --> E3["Gera CSV com headers<br/>adequados ao escopo"]
    end

    style ENTRY fill:#1E293B,stroke:#2EC4B6,color:#F1F5F9
    style METRICS fill:#1E293B,stroke:#F59E0B,color:#F1F5F9
    style FILTER_ORGAO fill:#1E293B,stroke:#8B5CF6,color:#F1F5F9
    style TABS fill:#1E293B,stroke:#EC4899,color:#F1F5F9
    style ORG_CARDS fill:#1E293B,stroke:#22C55E,color:#F1F5F9
    style EXPORT fill:#1E293B,stroke:#F97316,color:#F1F5F9
    style D3 fill:#7f1d1d,stroke:#EF4444,color:#F1F5F9
    style D2 fill:#1E293B,stroke:#EC4899,color:#F1F5F9
```

**Tags de arquivo:** `docs/diagrams/05-dashboard.md`
