import sys
from pathlib import Path

PRODUTO_DIR = Path(__file__).resolve().parent.parent.parent
if str(PRODUTO_DIR) not in sys.path:
    sys.path.insert(0, str(PRODUTO_DIR))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from models.preprocessor import limpar_texto, obter_sugestao_reescrita
from models.risk_engine import analisar_risco_contratual, gerar_recomendacoes
from models.anomaly_detector import detectar_anomalia, status_modelo
from models.model_loader import get_metricas, get_shap_explainer

st.set_page_config(page_title="Avaliacao de Minutas", page_icon="", layout="wide")

LIMITE_GRATUITO = 3

EXEMPLOS = {
    "Edital de TI": """EDITAL DE LICITACAO Nº 001/2026
PREGÃO ELETRONICO PARA CONTRATACAO DE SERVICOS DE TECNOLOGIA DA INFORMACAO
1. DO OBJETO
1.1. Contratacao de empresa especializada para prestacao de servicos de desenvolvimento e manutencao de sistemas de informacao.
2. DA FUNDAMENTACAO LEGAL
2.1. Lei nº 14.133, de 1º de abril de 2021.
3. DOS CRITERIOS DE JULGAMENTO
3.1. Menor preco para julgamento das propostas.
4. DA HABILITACAO
4.1. Certidoes negativas de debitos federais, estaduais e municipais.
5. DO PRAZO DE VIGENCIA
5.1. Vigencia de 12 meses.
6. DAS CONDICOES DE PAGAMENTO
6.1. Pagamento em ate 30 dias apos atesto.
7. DA GARANTIA
7.1. Garantia contratual de 5%. """,

    "Contrato de Inovacao": """CONTRATO DE PRESTACAO DE SERVICOS DE INOVACAO TECNOLOGICA
1. DO OBJETO
1.1. Contratacao de solucao de inteligencia artificial para automacao de processos de auditoria.
2. DA JUSTIFICATIVA
2.1. Modernizacao da administracao publica.
3. DA PROPRIEDADE INTELECTUAL
3.1. Codigo-fonte pertence a Administracao ao termino do contrato.
4. DA CONFIDENCIALIDADE
4.1. Sigilo conforme LGPD.
5. DOS NIVEIS DE SERVICO (SLA)
5.1. Disponibilidade 99.5%, tempo de resposta < 2s.""",
}

st.markdown("""
<style>
    .score-circle {
        width: 100px; height: 100px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.8rem; font-weight: 800; color: white; margin: 0 auto;
    }
    .lacuna-card {
        background: white; border-radius: 12px; padding: 14px; margin-bottom: 8px;
        border-left: 4px solid; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }
    .lacuna-alta { border-color: #ff3b30; }
    .lacuna-media { border-color: #ff9500; }
    .lacuna-baixa { border-color: #ffcc00; }
    .clausula-tag {
        display: inline-block; padding: 4px 10px; border-radius: 12px;
        font-size: 0.75rem; font-weight: 500; margin: 3px;
        background: #e8f5e9; color: #2e7d32;
    }
    .result-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px; padding: 24px; color: white; margin-bottom: 16px;
    }
    .upgrade-box {
        background: linear-gradient(135deg, #ff9500 0%, #ff3b30 100%);
        border-radius: 16px; padding: 32px; color: white; text-align: center;
    }
    .upgrade-box h2 { font-size: 1.5rem; font-weight: 700; }
    .upgrade-box p { font-size: 0.95rem; opacity: 0.95; }
    .metric-ml {
        background: rgba(0,122,255,0.08); border-radius: 8px;
        padding: 10px 14px; font-size: 0.75rem; color: #007aff;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.title(" Modulo de Avaliacao de Minutas")
st.caption("Analise com Isolation Forest + Random Forest treinados em 50.000 contratos PNCP")

st.sidebar.markdown("---")
st.sidebar.subheader("Status do Sistema")
status = status_modelo()
st.sidebar.markdown(f"TF-IDF: {'OK' if status['tfidf_ok'] else 'N/A'}")
st.sidebar.markdown(f"Isolation Forest: {'OK' if status['isolation_ok'] else 'N/A'}")
st.sidebar.markdown(f"ML Treinado: {'SIM' if status['usando_modelo_treinado'] else 'FALLBACK'}")

st.sidebar.markdown("---")
st.sidebar.subheader("Plano")
st.sidebar.markdown(f"**{st.session_state.get('plano', 'gratuito').upper()}**")
analises = st.session_state.get("analises_gratuitas", 0)
st.sidebar.progress(min(analises / LIMITE_GRATUITO, 1.0), text=f"{analises}/{LIMITE_GRATUITO} analises")
st.sidebar.caption("Premium: ilimitado + relatorios + reescrita")

if analises >= LIMITE_GRATUITO and st.session_state.get("plano") != "premium":
    st.warning(f"Voce atingiu o limite de {LIMITE_GRATUITO} analises gratuitas.")
    st.markdown("""
    <div class="upgrade-box">
        <h2> Desbloqueie o Copiloto Premium</h2>
        <p><strong>Recursos Premium:</strong></p>
        <p>
             Analises ilimitadas<br>
             Relatorio de auditoria completo (PDF)<br>
             Sugestao de reescrita de clausulas<br>
             Parecer tecnico de defesa assinado<br>
             Historico de analises
        </p>
        <p style="margin-top:20px;font-size:1.2rem;">
            <strong>Fale com a Consultoria Renato Rosa</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(" Entrada da Minuta")
    exemplo_selecionado = st.selectbox("Carregar exemplo", ["Selecione..."] + list(EXEMPLOS.keys()))
    if exemplo_selecionado and exemplo_selecionado != "Selecione...":
        st.session_state["minuta_texto"] = EXEMPLOS[exemplo_selecionado]

    texto = st.text_area(
        "Cole o texto da minuta:",
        value=st.session_state.get("minuta_texto", ""),
        height=250,
        key="input_minuta",
    )
    uploaded = st.file_uploader("Upload .txt", type=["txt"])
    if uploaded is not None:
        texto = uploaded.read().decode("utf-8")
        st.session_state["minuta_texto"] = texto

    st.divider()
    st.caption("Dados do contrato (para predicao ML com target observavel)")
    valor_estimado = st.number_input(
        "Valor estimado do contrato (R$):",
        min_value=0.0,
        value=10000.0,
        step=1000.0,
        format="%.2f",
        help="Usado pelo Random Forest para predicao de risco (feature valor_log).",
    )
    vigencia_dias = st.number_input(
        "Vigencia prevista (dias):",
        min_value=1,
        value=365,
        step=30,
        help="Duracao prevista do contrato. Contratos < 30 dias tem risco elevado (dado observavel do PNCP).",
    )

    analisar = st.button(" Analisar Minuta (ML Real)", type="primary", use_container_width=True)

with col2:
    st.subheader(" Funcionalidades ML")
    st.markdown("""
    - TF-IDF + Isolation Forest
    - Random Forest (11 features)
    - SHAP explicabilidade
    - Deteccao de lacunas
    - Recomendacoes XAI
    """)

    st.divider()
    metricas = get_metricas()
    if metricas:
        st.subheader(" Metricas do Modelo")
        st.markdown(f'<div class="metric-ml">Acuracia: {metricas.get("acuracia", 0)*100:.2f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-ml">AUC-ROC: {metricas.get("auc_roc", 0)*100:.2f}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-ml">CV 5-fold: {metricas.get("cv_mean", 0)*100:.2f}%</div>', unsafe_allow_html=True)

if analisar and texto.strip():
    st.session_state["analises_gratuitas"] = st.session_state.get("analises_gratuitas", 0) + 1

    metadados = {"valor": valor_estimado, "vigencia_dias": int(vigencia_dias)}

    with st.spinner("Executando TF-IDF + Isolation Forest + Random Forest integrado + SHAP + Contrafactuais..."):
        resultado = analisar_risco_contratual(texto, metadados)
        anomalia = detectar_anomalia(texto)
        recomendacoes = gerar_recomendacoes(resultado["lacunas"], resultado["clausulas_encontradas"], resultado.get("features_shap"))

    st.divider()
    st.markdown("###  Relatorio de Analise (ML)")

    score = resultado["score"]
    if score >= 70:
        cor_score, label_score = "#34c759", "Adequado"
    elif score >= 50:
        cor_score, label_score = "#ff9500", "Alerta"
    else:
        cor_score, label_score = "#ff3b30", "Critico"

    col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
    with col_r1:
        st.markdown(f'<div class="score-circle" style="background:{cor_score};">{score}%</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center;font-weight:600;color:{cor_score};">{label_score}</p>', unsafe_allow_html=True)
    with col_r2:
        st.metric("Palavras", resultado["total_palavras"])
    with col_r3:
        st.metric("RF Score", f"{resultado['rf_score']}" if resultado["rf_score"] is not None else "N/A")
    with col_r4:
        st.metric("RF Proba", f"{resultado['rf_proba']:.2f}" if resultado["rf_proba"] is not None else "N/A")
    with col_r5:
        st.metric("Anomalia", "Sim" if anomalia["is_anomalia"] else "Nao")

    if resultado["rf_proba"] is not None:
        risco_ml = resultado.get("risco_ml", "N/A")
        proba_pct = resultado["rf_proba"] * 100
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:12px;margin-bottom:12px;border:1px solid #e5e5e5;">
            <strong>Predicao Random Forest:</strong> Risco <span style="color:{'#ff3b30' if risco_ml == 'alto' else '#ff9500' if risco_ml == 'medio' else '#34c759'};">{risco_ml.upper()}</span> ({proba_pct:.1f}%)<br>
            <small>Treinado em 50.000 contratos PNCP | Acuracia: {resultado['metricas_treino']['acuracia']*100:.2f}%</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader(" Clausulas Identificadas")
        if resultado["clausulas_encontradas"]:
            for c in resultado["clausulas_encontradas"]:
                st.markdown(f'<span class="clausula-tag">{c}</span>', unsafe_allow_html=True)
        else:
            st.warning("Nenhuma clausula padrao identificada.")

        st.subheader(" Lacunas Detectadas")
        if resultado["lacunas"]:
            for l in resultado["lacunas"]:
                classe = f"lacuna-{l['prioridade']}"
                emoji = "" if l["prioridade"] == "alta" else "" if l["prioridade"] == "media" else ""
                st.markdown(f'<div class="lacuna-card {classe}"><strong>{emoji} {l["item"]}</strong> ({l["prioridade"].upper()})<br><small style="color:#86868b;">{l["desc"]}</small></div>', unsafe_allow_html=True)
        else:
            st.success("Nenhuma lacuna critica!")

    with col_dir:
        st.subheader(" Recomendacoes")
        if recomendacoes:
            for r in recomendacoes:
                cor = "#ff3b30" if r["tipo"] == "CRITICA" else "#ff9500" if r["tipo"] == "IMPORTANTE" else "#34c759"
                emoji = "" if r["tipo"] == "CRITICA" else "" if r["tipo"] == "IMPORTANTE" else ""
                st.markdown(f'<div style="background:white;border-radius:12px;padding:12px;margin-bottom:8px;border-left:4px solid {cor};box-shadow:0 1px 6px rgba(0,0,0,0.05);"><strong>{emoji} [{r["tipo"]}]</strong> {r["texto"]}<br><small style="color:#86868b;">{r["fundamento"]}</small></div>', unsafe_allow_html=True)
        else:
            st.success("Nenhuma recomendacao adicional necessaria.")

    st.divider()
    st.subheader(" Explicabilidade (XAI/SHAP)")

    if resultado["features_shap"]:
        import matplotlib
        matplotlib.use("Agg")
        fig, ax = plt.subplots(figsize=(8, 3))
        features = [f["feature"][:25] for f in resultado["features_shap"][:7]]
        pesos = [f["peso"] for f in resultado["features_shap"][:7]]
        colors = ["#ff3b30" if p > 0.02 else "#ff9500" if p > 0.005 else "#34c759" for p in pesos]
        ax.barh(range(len(features)), pesos, color=colors)
        ax.set_yticks(range(len(features)))
        ax.set_yticklabels(features, fontsize=9)
        ax.set_xlabel("Contribuicao SHAP", fontsize=9)
        ax.set_title("Feature Importance (SHAP)", fontsize=11, fontweight="bold")
        ax.invert_yaxis()
        for i, v in enumerate(pesos):
            ax.text(v + 0.0005, i, f"{v:.4f}", va="center", fontsize=8)
        st.pyplot(fig)

    if resultado.get("contrafactuais"):
        st.divider()
        st.subheader(" Explicacoes Contrafactuais (XAI)")
        st.caption("SPRINT 2.2: O que mudaria no risco se cada feature fosse alterada?")
        for cf in resultado["contrafactuais"]:
            st.info(f"**{cf['feature']}** (peso SHAP: {cf['peso']:.4f})\n\n{cf['contrafactual']}")

        st.divider()
        st.subheader(" Fundamento Juridico das Features (XAI Normativamente Ancorada)")
        from models.xai_explainer import gerar_texto_legal_counterfactual
        textos_legais = gerar_texto_legal_counterfactual(resultado["contrafactuais"])
        if textos_legais:
            for tl in textos_legais:
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:14px;margin-bottom:10px;border-left:5px solid #2e7d32;box-shadow:0 1px 6px rgba(0,0,0,0.06);">
                    <strong style="color:#2e7d32;">{tl['nome_legal']}</strong>
                    <p style="margin:6px 0 0 0;font-size:0.85rem;color:#1a1a1a;">{tl['pergunta_legal']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Nenhum fundamento juridico disponivel para as features do modelo.")

    st.markdown(f"""
    <div class="result-card">
        <p><strong>Modelos utilizados (SPRINT 1+2):</strong></p>
        <p> TF-IDF + Isolation Forest (15.000 objetos PNCP, integrado ao RF)<br>
         Random Forest Classifier ({resultado['metricas_treino']['acuracia']*100:.2f}% acuracia, AUC={resultado['metricas_treino']['auc_roc']*100:.2f}%)<br>
         SHAP TreeExplainer + Contrafactuais dinamicos</p>
        <p><strong>Anomalia:</strong> {anomalia['mensagem']}</p>
        <p style="margin-top:12px;font-size:0.75rem;color:rgba(255,255,255,0.6);">
            Target observavel: desfechos reais do PNCP (18.8% positivos)<br>
            Treinado em {datetime.now().strftime('%Y-%m-%d')} sobre 100.000 contratos do PNCP (Set/2021 - Ago/2024).
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("plano") == "premium":
        st.divider()
        st.subheader(" Sugestoes de Reescrita (Premium)")

        mapa_chaves = {
            "Clausula de Garantia": "garantia",
            "Confidencialidade/LGPD": "confidencialidade",
            "Rescisao Contratual": "rescisao",
            "Niveis de Servico (SLA)": "sla",
            "Propriedade Intelectual": "propriedade_intelectual",
            "Responsabilidades": "responsabilidade",
        }

        sugestoes_geradas = 0
        for lacuna in resultado["lacunas"]:
            chave = mapa_chaves.get(lacuna["item"])
            if chave:
                sugestao = obter_sugestao_reescrita(chave)
                if sugestao:
                    sugestoes_geradas += 1
                    with st.expander(f" Reescrever: {lacuna['item']}"):
                        st.code(sugestao, language=None)

        if sugestoes_geradas == 0:
            st.info("Nenhuma sugestao de reescrita necessaria. O edital esta bem estruturado.")

        st.divider()
        st.subheader(" Relatorio Premium")
        relatorio = f"""RELATORIO DE AUDITORIA - COPILOTO ALGORITMICO
Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Score de Conformidade: {score}% ({label_score})
Risco Random Forest: {resultado.get('risco_ml', 'N/A').upper()} ({resultado['rf_proba']*100:.1f}% prob.)
Clausulas: {', '.join(resultado['clausulas_encontradas'])}
Lacunas: {len(resultado['lacunas'])}
Recomendacoes: {len(recomendacoes)}
Sugestoes de reescrita: {sugestoes_geradas}
"""
        st.download_button(" Baixar Relatorio (.txt)", relatorio, file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")

elif analisar and not texto.strip():
    st.warning("Por favor, cole o texto de uma minuta para analise.")
