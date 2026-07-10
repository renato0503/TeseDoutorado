# 🚀 Copiloto Algorítmico (Governo & Compras Complexas)

[![Status](https://img.shields.io/badge/Status-Beta_Fechado-orange.svg)]()
[![Model](https://img.shields.io/badge/AI-Explainable_(XAI)-blue.svg)]()

Bem-vindo ao **Copiloto Algorítmico**, o exoesqueleto cognitivo criado para apoiar pregoeiros e gestores públicos na estruturação de **Compras Complexas** (Inovação, TI, ESG). 

Desenvolvido como produto empírico da Tese de Doutorado na Fucape Business School, este artefato resolve a dor da assimetria informacional e da latência decisória, garantindo **Accountability** e legalidade aos processos licitatórios.

## 🎯 O Problema que Resolvemos
Gestores públicos sofrem com o "apagão técnico" ao tentar redigir editais de tecnologia avançada contra um mercado privado oligopolista e hiper-especializado. A insegurança jurídica leva a editais direcionados ou mal formulados, que são sumariamente punidos por Tribunais de Contas ou impugnados pelo mercado.

## ⚙️ Como Funciona (A Mágica do XAI)
Nós não somos uma "Caixa Preta". Operamos com Inteligência Artificial Explicável (XAI).
Ao fazer o upload da minuta do seu Edital, nosso motor passa o texto por dois filtros de Machine Learning:
1. **Isolation Forest:** Identifica anomalias e cláusulas "fora do padrão" de mercado.
2. **Random Forest (94,88% Acurácia):** Prediz o risco de impugnação.
3. **SHAP Values:** A inteligência artificial "grifa" qual cláusula exata está elevando o seu risco e *explica* o porquê.

## 💎 Planos (Freemium)

### 🟢 Versão Gratuita (Comunidade)
- Upload de 1 edital por mês.
- **Score Geral de Risco:** Saiba se o seu edital vai "passar" ou "bater na trave".
- **Alerta Primário:** Identificação da pior cláusula (mas sem sugestão de reescrita).

### 👑 Versão Premium / Consultoria Privada
Você descobriu que seu edital de R$ 5 Milhões tem 82% de chance de ser derrubado no TCU. E agora?
Na versão Premium, nossa equipe alia o motor do Copiloto à **Consultoria Especializada**:
- Relatório de Auditoria Completo (Saneamento preventivo).
- Sugestão de reescrita contrafactual de cláusulas com base em jurisprudência atualizada.
- Parecer técnico de defesa assinado.

👉 **[Fale com a Consultoria Renato Rosa](#)** e transforme sua licitação de risco em uma contratação de sucesso absoluto.

---

## 🛠️ Stack Tecnológico
- **Frontend:** Streamlit
- **Modelos:** Scikit-Learn (Random Forest, Isolation Forest), SHAP, Matplotlib
- **Infra:** Streamlit Cloud (gratuito) / Firebase Hosting (versao estatica)

## 📁 Estrutura do Produto

```
03-Produto-Copiloto/
├── app/
│   ├── app.py                     # Home do Streamlit (metricas, navegacao)
│   └── pages/
│       ├── 01_Avaliacao.py        # Modulo de Avaliacao de Minutas
│       └── 02_Geracao.py          # Modulo de Geracao de Editais
├── models/
│   ├── preprocessor.py            # NLP: limpeza, TF-IDF, regex clausulas
│   ├── risk_engine.py             # Motor de scoring e recomendacoes
│   ├── anomaly_detector.py        # Isolation Forest wrapper
│   └── xai_explainer.py           # SHAP templates e explicacoes textuais
├── data/                          # Referencias aos dados processados
├── docs/
│   └── arquitetura.md             # Arquitetura DSR detalhada
├── requirements.txt
└── README.md
```

## 🚀 Como Rodar

```bash
cd Tese/03-Produto-Copiloto
pip install -r requirements.txt
streamlit run app/app.py
```

O app abrira em `http://localhost:8501` com:
- **Home:** Metricas do PNCP, visao geral do sistema, link para consultoria
- **Modulo 1 (Avaliacao):** Upload de minuta, analise de clausulas, deteccao de lacunas, score XAI
- **Modulo 2 (Geracao):** Formulario para geracao de minuta completa com clausulas XAI

## 🌐 Versoes

| Versao | Local | Descricao |
|--------|-------|-----------|
| `Copiloto/modulo_*` | Repo raiz | Prototipos HTML estaticos (referencia de design) |
| `PubliCopilot/` | Firebase | Deploy estatico em `comprapublica.web.app` |
| `Tese/03-Produto-Copiloto/` | Streamlit | **MVP funcional com Python real (este repositorio)** |

Para entender a base academica e matematica por tras dos algoritmos, consulte a pasta `docs/arquitetura.md`.
