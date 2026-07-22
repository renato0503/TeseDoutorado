import sys
from pathlib import Path

PRODUTO_DIR = Path(__file__).resolve().parent.parent
if str(PRODUTO_DIR) not in sys.path:
    sys.path.insert(0, str(PRODUTO_DIR))

import streamlit as st
from models.model_loader import get_metricas, modelos_disponiveis

st.set_page_config(
    page_title="Copiloto Algoritmico",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

ESTILO_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 40px 32px;
        border-radius: 20px;
        color: white;
        margin-bottom: 28px;
    }
    .main-header h1 { font-size: 2rem; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 8px; }
    .main-header p { color: rgba(255,255,255,0.7); font-size: 0.95rem; }
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        text-align: center;
    }
    .metric-value { font-size: 1.6rem; font-weight: 700; color: #007aff; }
    .metric-label { font-size: 0.7rem; color: #86868b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        height: 100%;
    }
    .feature-card h3 { font-size: 1rem; font-weight: 600; margin-bottom: 8px; }
    .feature-card p { color: #86868b; font-size: 0.85rem; line-height: 1.6; }
    .footer-bar {
        margin-top: 40px; padding-top: 20px;
        border-top: 1px solid #f0f0f0;
        text-align: center; color: #a1a1a6; font-size: 0.8rem;
    }
    .consultancy-box {
        background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
        border-radius: 16px; padding: 24px;
        color: white; text-align: center; margin-top: 24px;
    }
    .consultancy-box h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; }
    .consultancy-box p { font-size: 0.85rem; opacity: 0.9; margin-bottom: 16px; }
    .badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 600;
    }
    .badge-active { background: rgba(52,199,89,0.15); color: #34c759; }
    .badge-dsr { background: rgba(175,82,222,0.15); color: #af52de; }
    .badge-ml { background: rgba(0,122,255,0.12); color: #007aff; }
    .model-status { font-size: 0.75rem; padding: 8px 12px; border-radius: 8px; margin-bottom: 12px; }
    .model-status.ok { background: rgba(52,199,89,0.1); color: #34c759; border: 1px solid rgba(52,199,89,0.2); }
    .model-status.warn { background: rgba(255,149,0,0.1); color: #ff9500; border: 1px solid rgba(255,149,0,0.2); }
</style>
"""
st.markdown(ESTILO_CSS, unsafe_allow_html=True)

metricas = get_metricas()
disp = modelos_disponiveis()
modelos_ok = all(disp.values())

if "analises_gratuitas" not in st.session_state:
    st.session_state["analises_gratuitas"] = 0
if "plano" not in st.session_state:
    st.session_state["plano"] = "gratuito"

st.markdown(f"""
<div class="main-header">
    <h1>Copiloto Algoritmico para Compras Publicas</h1>
    <p>
        <span class="badge badge-dsr">Design Science Research</span>
        &nbsp;
        <span class="badge badge-active">Fucape Business School</span>
        &nbsp;
        <span class="badge badge-ml">ML Treinado (PNCP)</span>
    </p>
    <p style="margin-top:12px;">
        Ferramenta de apoio a decisao baseada em IA Explicavel (XAI) para pregoeiros e gestores publicos.<br>
        Reduz assimetria informacional em <strong>Compras Complexas</strong> (Inovacao, Tecnologia, Sustentabilidade).
    </p>
</div>
""", unsafe_allow_html=True)

st.caption(f"Plano atual: {st.session_state['plano'].upper()} | Analises usadas hoje: {st.session_state['analises_gratuitas']}/3")

st.info(
    "**Disclaimber Academico (Sprint 5):** Esta ferramenta e parte integrante da pesquisa de doutorado "
    "de Renato de Oliveira Rosa no Programa de Pos-Graduacao em Ciencias Contabeis e Administracao "
    "da Fucape Business School (Vitoria/ES), sob orientacao do Prof. Dr. Olavo Venturim Caldas. "
    "O uso e gratuito para fins academicos, de pesquisa e de avaliacao. O modelo Premium destina-se "
    "a viabilizar a continuidade e manutencao da pesquisa. A consultoria mencionada e independente "
    "e nao possui vinculo institucional com a Fucape."
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><div class="metric-value">572.045</div><div class="metric-label">Contratos PNCP</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="metric-value">5.687</div><div class="metric-label">Compras Complexas</div></div>', unsafe_allow_html=True)
with col3:
    acc = f"{metricas.get('acuracia', 0) * 100:.2f}%"
    st.markdown(f'<div class="metric-card"><div class="metric-value">{acc}</div><div class="metric-label">Acuracia RF (Treinado)</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{"ON" if modelos_ok else "OFF"}</div><div class="metric-label">Modelos ML Carregados</div></div>', unsafe_allow_html=True)

st.divider()

st.subheader("Modulos do Sistema")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div class="feature-card">
        <h3> Modulo de Avaliacao de Minutas</h3>
        <p>
            Cole o texto do seu edital e receba analise com
            <strong>Isolation Forest</strong> + <strong>Random Forest</strong> treinados em 50k contratos PNCP.
        </p>
        <p style="margin-top:12px;">
            <strong>Funcionalidades:</strong><br>
            NLP + TF-IDF para classificacao  ·  Deteccao de anomalias (Isolation Forest)<br>
            Predicao de risco (Random Forest)  ·  Recomendacoes com XAI/SHAP
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="feature-card">
        <h3> Modulo de Geracao de Editais</h3>
        <p>
            Preencha os dados e gere <strong>minuta completa</strong> com clausulas XAI
            baseadas em 19.640 editais do PNCP e na Lei 14.133/2021.
        </p>
        <p style="margin-top:12px;">
            <strong>Funcionalidades:</strong><br>
            Clausulas pre-configuradas  ·  Justificativas XAI (Williamson, LGPD, LC 182)<br>
            Exportacao  ·  Conformidade Lei 14.133/2021
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("Status dos Modelos ML")
col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    status_class = "ok" if disp.get("isolation_forest") else "warn"
    status_text = "TREINADO" if disp.get("isolation_forest") else "NAO ENCONTRADO"
    st.markdown(f'<div class="model-status {status_class}">Isolation Forest: <strong>{status_text}</strong><br><small>Treinado em 15.000 objetos do PNCP</small></div>', unsafe_allow_html=True)
with col_m2:
    status_class = "ok" if disp.get("random_forest") else "warn"
    status_text = f"TREINADO (acc={metricas.get('acuracia', 0)*100:.2f}%)" if disp.get("random_forest") else "NAO ENCONTRADO"
    st.markdown(f'<div class="model-status {status_class}">Random Forest: <strong>{status_text}</strong><br><small>100.000 contratos, 11 features, AUC={metricas.get("auc_roc", 0)*100:.2f}%</small></div>', unsafe_allow_html=True)
with col_m3:
    status_class = "ok" if disp.get("shap_explainer") else "warn"
    status_text = "DISPONIVEL" if disp.get("shap_explainer") else "NAO ENCONTRADO"
    st.markdown(f'<div class="model-status {status_class}">SHAP Explainer: <strong>{status_text}</strong><br><small>Explicabilidade em tempo real</small></div>', unsafe_allow_html=True)

st.divider()

st.subheader("Como funciona (XAI)")
col_x1, col_x2, col_x3 = st.columns(3)
with col_x1:
    st.markdown('<div class="feature-card"><h3>1. TF-IDF + Isolation Forest</h3><p>Vetoriza o objeto do contrato em 500 features e detecta anomalias contra a base de 15.000 objetos do PNCP.</p></div>', unsafe_allow_html=True)
with col_x2:
    st.markdown('<div class="feature-card"><h3>2. Random Forest</h3><p>Prediz o risco com base em 11 features (valor, vigencia, complexidade lexica, UF, tipo, interacoes IF) treinadas em 100k contratos.</p></div>', unsafe_allow_html=True)
with col_x3:
    st.markdown('<div class="feature-card"><h3>3. SHAP Values</h3><p>A IA explica qual feature mais contribuiu para o score de risco, garantindo transparencia e accountability.</p></div>', unsafe_allow_html=True)

st.divider()

st.markdown(f"""
<div class="consultancy-box">
    <h3> Precisa de ajuda especializada?</h3>
    <p>
        Seu edital de alto valor tem risco de impugnacao ou rejeicao no TCU?<br>
        Na versao <strong>Premium</strong>, nossa equipe alia o motor do Copiloto a <strong>Consultoria Especializada</strong>.
    </p>
    <p style="font-size:1.1rem;">
        <strong>Fale com a Consultoria Renato Rosa</strong>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-bar">
    <p>Copiloto Algoritmico · Pesquisa de Doutorado · Fucape Business School</p>
    <p>Orientador: Prof. Dr. Olavo Venturim Caldas | <a href="https://github.com/renato0503/TeseDoutorado" target="_blank">GitHub</a></p>
    <p style="font-size:0.7rem; margin-top:8px; color:#bbb;">
        Politica de Privacidade: Nenhum texto de edital submetido a analise e armazenado apos o termino da sessao.
        Nenhum dado e compartilhado com terceiros. Os modelos operam inteiramente em memoria (cache singleton).
        Nao utilizamos cookies de rastreamento nem armazenamos informacoes pessoais.
    </p>
</div>
""", unsafe_allow_html=True)
