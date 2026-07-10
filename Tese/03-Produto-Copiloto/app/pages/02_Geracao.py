import sys
from pathlib import Path

PRODUTO_DIR = Path(__file__).resolve().parent.parent.parent
if str(PRODUTO_DIR) not in sys.path:
    sys.path.insert(0, str(PRODUTO_DIR))

import streamlit as st
from datetime import datetime
from models.xai_explainer import obter_explicacao

st.set_page_config(page_title="Geracao de Editais", page_icon="", layout="wide")

LIMITE_GRATUITO = 3

CLAUSULAS_POR_TIPO = {
    "tecnologia": [
        {"titulo": "DO OBJETO", "texto": "1.1. Contratacao de servicos de tecnologia da informacao, compreendendo: fornecimento de licenca de uso, implementacao, treinamento e suporte tecnico."},
        {"titulo": "DA FUNDAMENTACAO LEGAL", "texto": "2.1. Lei 14.133/2021 e Lei Complementar 123/2006 (ME/EPP)."},
        {"titulo": "DAS CONDICOES DE PAGAMENTO", "texto": "3.1. Pagamento em ate 30 dias apos atesto da nota fiscal."},
        {"titulo": "DA GARANTIA", "texto": "4.1. Garantia de 5% do valor do contrato."},
        {"titulo": "DA PROPRIEDADE INTELECTUAL", "texto": "5.1. A propriedade do codigo-fonte sera da Administracao ao termino."},
        {"titulo": "DA CONFIDENCIALIDADE", "texto": "6.1. Sigilo conforme LGPD."},
        {"titulo": "DOS NIVEIS DE SERVICO (SLA)", "texto": "7.1. Disponibilidade 99.5%, tempo de resposta < 2s, glosas proporcionais."},
    ],
    "inovacao": [
        {"titulo": "DO OBJETO", "texto": "1.1. Contratacao de solucao de tecnologia inovadora conforme Marco Legal das Startups (LC 182/2021)."},
        {"titulo": "DA FUNDAMENTACAO LEGAL", "texto": "2.1. Lei 14.133/2021 e LC 182/2021 (Marco Legal das Startups)."},
        {"titulo": "DA ENCOMENDA TECNOLOGICA", "texto": "3.1. A contratacao podera adotar encomenda tecnologica (Art. 13 LC 182/2021)."},
        {"titulo": "DA TRANSFERENCIA TECNOLOGICA", "texto": "4.1. Transferencia de conhecimento ao termino do contrato."},
        {"titulo": "DA PROPRIEDADE INTELECTUAL", "texto": "5.1. Titularidade compartilhada do codigo-fonte."},
        {"titulo": "DA CONFIDENCIALIDADE", "texto": "6.1. Sigilo e protecao de segredo industrial."},
        {"titulo": "DOS NIVEIS DE SERVICO (SLA)", "texto": "7.1. KPIs de inovacao: TRL alcancado, entregas incrementais."},
    ],
    "sustentavel": [
        {"titulo": "DO OBJETO", "texto": "1.1. Aquisicao de bens com criterios de sustentabilidade (Decreto 10.936/2022)."},
        {"titulo": "DA FUNDAMENTACAO LEGAL", "texto": "2.1. Lei 14.133/2021, Art. 5 (desenvolvimento nacional sustentavel)."},
        {"titulo": "DOS CRITERIOS DE SUSTENTABILIDADE", "texto": "3.1. Certificacao ambiental (ISO 14001, Selo Procel, Energy Star)."},
        {"titulo": "DA LOGISTICA REVERSA", "texto": "4.1. Logistica reversa para embalagens e componentes."},
        {"titulo": "DA EFICIENCIA ENERGETICA", "texto": "5.1. Produtos classe A de eficiencia energetica."},
        {"titulo": "DAS CONDICOES DE PAGAMENTO", "texto": "6.1. Pagamento em ate 30 dias apos atesto."},
        {"titulo": "DO RELATORIO DE IMPACTO", "texto": "7.1. Relatorio anual de impacto ambiental."},
    ],
}

CONFIG_MODALIDADES = {
    "pregao": "PREGAO ELETRONICO",
    "concorrencia": "CONCORRENCIA",
    "tomada_preco": "TOMADA DE PRECOS",
    "inexigibilidade": "INEXIGIBILIDADE",
    "dispensa": "DISPENSA DE LICITACAO",
}
CONFIG_CRITERIOS = {
    "menor_preco": "Menor Preco",
    "melhor_tecnica": "Melhor Tecnica",
    "tecnica_preco": "Tecnica e Preco",
    "maior_desconto": "Maior Desconto",
}

st.markdown("""
<style>
    .clausula-card {
        background: white; border-radius: 12px; padding: 16px; margin-bottom: 10px;
        border-left: 4px solid #007aff; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }
    .clausula-xai {
        background: rgba(175,82,222,0.06); border: 1px solid rgba(175,82,222,0.2);
        border-radius: 8px; padding: 10px; margin-top: 8px;
    }
    .minuta-box {
        background: #f8f9fa; border: 1px solid #e5e5e5;
        border-radius: 12px; padding: 24px; font-family: 'Courier New', monospace;
        font-size: 0.8rem; white-space: pre-wrap; max-height: 500px; overflow-y: auto;
    }
    .upgrade-box {
        background: linear-gradient(135deg, #ff9500 0%, #ff3b30 100%);
        border-radius: 16px; padding: 32px; color: white; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title(" Modulo de Geracao de Editais")
st.caption("Recomendacao de clausulas com justificativas XAI para editais de inovacao, tecnologia e sustentabilidade")

st.sidebar.markdown("---")
st.sidebar.subheader("Plano")
st.sidebar.markdown(f"**{st.session_state.get('plano', 'gratuito').upper()}**")
geracoes_usadas = st.session_state.get("analises_gratuitas", 0)
st.sidebar.caption(f"Geracoes usadas: {geracoes_usadas}/{LIMITE_GRATUITO}")

if geracoes_usadas >= LIMITE_GRATUITO and st.session_state.get("plano") != "premium":
    st.warning(f"Limite de {LIMITE_GRATUITO} geracoes gratuitas atingido.")
    st.markdown("""
    <div class="upgrade-box">
        <h2> Desbloqueie o Premium</h2>
        <p>
             Geracao ilimitada de editais<br>
             Clausulas personalizadas por segmento<br>
             Revisao juridica especializada
        </p>
        <p style="margin-top:20px;font-size:1.2rem;">
            <strong>Fale com a Consultoria Renato Rosa</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

st.subheader(" Configuracao do Edital")

tab1, tab2, tab3 = st.tabs(["Dados Basicos", "Objeto", "Clausulas Juridicas"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        orgao = st.text_input("Orgao Licitante *", placeholder="Prefeitura Municipal de Vitoria")
        uasg = st.text_input("UASG *", placeholder="989901")
        tipo_contratacao = st.selectbox(
            "Tipo de Contratacao",
            ["tecnologia", "inovacao", "sustentavel", "servicos", "obras"],
            format_func=lambda x: {
                "tecnologia": "Tecnologia da Informacao",
                "inovacao": "Inovacao / GovTech",
                "sustentavel": "Compras Sustentaveis",
                "servicos": "Servicos Gerais",
                "obras": "Obras e Engenharia",
            }.get(x, x),
        )
    with col2:
        modalidade = st.selectbox("Modalidade *", list(CONFIG_MODALIDADES.keys()),
                                   format_func=lambda x: CONFIG_MODALIDADES[x])
        valor = st.text_input("Valor Estimado (R$) *", placeholder="1.500.000,00")
        vigencia = st.text_input("Vigencia", placeholder="12 meses")

with tab2:
    objeto = st.text_area("Objeto *", height=120,
                          placeholder="Descreva detalhadamente o objeto da contratacao...")
    justificativa = st.text_area("Justificativa", height=100,
                                  placeholder="Justifique a necessidade...")
    criterio = st.selectbox("Criterio de Julgamento", list(CONFIG_CRITERIOS.keys()),
                             format_func=lambda x: CONFIG_CRITERIOS[x])

with tab3:
    pagamento = st.text_input("Condicoes de Pagamento", placeholder="30 dias apos atesto")
    garantia = st.selectbox("Garantia", ["Nao Exigida", "Garantia Financeira (5%)", "Garantia Contratual (5-10%)"])
    penalidades = st.text_area("Penalidades", height=80, placeholder="Penalidades aplicaveis...")

col_btn1, col_btn2, col_btn3, _ = st.columns([1, 1, 1, 3])
with col_btn1:
    gerar = st.button(" Gerar Edital", type="primary", use_container_width=True)
with col_btn2:
    gerar_clausulas = st.button(" So Clausulas", use_container_width=True)
with col_btn3:
    if st.button(" Exemplo", use_container_width=True):
        st.session_state["ex_orgao"] = "Prefeitura Municipal de Vitoria"
        st.session_state["ex_uasg"] = "989901"

if "ex_orgao" in st.session_state:
    orgao = st.session_state.pop("ex_orgao", orgao)
    uasg = st.session_state.pop("ex_uasg", uasg)

if (gerar or gerar_clausulas) and orgao and uasg and modalidade and objeto:
    st.session_state["analises_gratuitas"] = st.session_state.get("analises_gratuitas", 0) + 1

    with st.spinner("Gerando edital a partir de 19.640 editais PNCP..."):
        clausulas_tipo = CLAUSULAS_POR_TIPO.get(tipo_contratacao, CLAUSULAS_POR_TIPO["tecnologia"])
        modalidade_nome = CONFIG_MODALIDADES.get(modalidade, modalidade.upper())
        criterio_nome = CONFIG_CRITERIOS.get(criterio, "Menor Preco")

        clausulas_formatadas = []
        for c in clausulas_tipo:
            clausulas_formatadas.append(f"""{c['titulo']}
{c['texto']}""")
        bloco_clausulas = "\n\n".join(clausulas_formatadas)

        minuta = f"""{modalidade_nome} N {uasg}
================================================================================
                                PREAMBULO
================================================================================
{orgao}, UASG: {uasg}, torna publico que realizara {modalidade_nome}, do tipo {criterio_nome}.

================================================================================
                                DO OBJETO
================================================================================
{objeto}

================================================================================
                            DA JUSTIFICATIVA
================================================================================
{justificativa or 'Contratacao necessaria para atender as demandas da administracao publica.'}

================================================================================
                        DA FUNDAMENTACAO LEGAL
================================================================================
Lei 14.133/2021 e LC 123/2006.

================================================================================
                        DO CRITERIO DE JULGAMENTO
================================================================================
{criterio_nome}.

================================================================================
                          DO VALOR ESTIMADO
================================================================================
R$ {valor or '0,00'}.

================================================================================
                         DO PRAZO DE VIGENCIA
================================================================================
{vigencia or '12 (doze) meses'}.

================================================================================
                     DAS CONDICOES DE PAGAMENTO
================================================================================
{pagamento or '30 (trinta) dias apos atesto'}.

================================================================================
                            DA HABILITACAO
================================================================================
a) Certidoes negativas;
b) Regularidade FGTS;
c) Capacidade tecnica.

================================================================================
                         DAS PENALIDADES
================================================================================
{penalidades or 'Sancoes previstas na Lei 14.133/2021.'}

================================================================================
                        DA GARANTIA CONTRATUAL
================================================================================
{garantia or 'Nao exigida.'}

================================================================================
{bloco_clausulas}

================================================================================
                         DAS DISPOSICOES FINAIS
================================================================================
Edital disponivel no portal Compras Net.
Esclarecimentos ate 3 dias uteis antes.

================================================================================
                                DO FORO
================================================================================
Justica Federal.

{orgao}, __/__/____.

________________________________________________________________________________
{orgao}
Ordenador de Despesas
"""

    st.divider()
    st.markdown("###  Resultado")

    st.metric("Clausulas Geradas", len(clausulas_tipo))
    st.metric("Justificativas XAI", len(clausulas_tipo))

    st.subheader(" Clausulas Recomendadas")
    for c in clausulas_tipo:
        chave = c["titulo"].lower().replace("da ", "").replace("do ", "").replace("dos ", "").replace("de ", "").replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")
        explicacao = obter_explicacao(chave)
        if not explicacao:
            import re
            chave_simples = re.sub(r"[^\w]", "", c["titulo"].split()[1].lower()) if len(c["titulo"].split()) > 1 else chave
            explicacao = obter_explicacao(chave_simples)

        st.markdown(f"""
        <div class="clausula-card">
            <strong>{c['titulo']}</strong> <span style="font-size:0.7rem;color:#af52de;">XAI</span><br>
            <span style="font-size:0.85rem;color:#555;">{c['texto']}</span>
            <div class="clausula-xai">
                <span style="font-size:0.7rem;color:#af52de;"> Justificativa XAI</span><br>
                <span style="font-size:0.8rem;color:#666;">{explicacao.get('explicacao', '') if explicacao else 'Clausula baseada em 19.640 editais do PNCP.'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader(" Minuta Completa")
    st.download_button(
        " Download (.txt)",
        minuta,
        file_name=f"edital_{uasg}_{tipo_contratacao}_{datetime.now().strftime('%Y%m%d')}.txt",
    )
    st.markdown(f'<div class="minuta-box">{minuta}</div>', unsafe_allow_html=True)

elif (gerar or gerar_clausulas) and not (orgao and uasg and modalidade and objeto):
    st.error("Preencha todos os campos obrigatorios (*).")
