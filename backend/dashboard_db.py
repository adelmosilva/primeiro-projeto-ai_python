"""
Dashboard Streamlit integrado com banco de dados PostgreSQL
AGT 4.0 v2.0 - Database Edition
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import matplotlib.pyplot as plt

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.servico_tickets import obter_servico
from app.services.analysis_service import AnalysisService
from app.services.pdf_report_service import PDFReportService
from app.config import REPORTS_OUTPUT_DIR

# Configurar página
st.set_page_config(
    page_title="AGT 4.0 - Dashboard (DB)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("📊 AGT 4.0 - Dashboard com Banco de Dados")
st.markdown("Análise em tempo real de tickets do Jira via PostgreSQL")
st.markdown("---")

@st.cache_resource
def obter_servico_cache():
    """Cache do serviço para evitar múltiplas conexões."""
    return obter_servico()

def formatar_numero(n):
    """Formata número com separador de milhar."""
    return f"{int(n):,.0f}".replace(",", ".")

# Sidebar com opções
with st.sidebar:
    st.header("⚙️ Configurações")
    
    modo = st.radio(
        "Modo de visualização:",
        ["📊 Dashboard Geral", "📅 Período Específico", "📈 Comparativo de Meses"]
    )
    
    # Inicializar variáveis
    mes, ano = None, None
    mes1, ano1, mes2, ano2 = None, None, None, None
    
    # Opções de período
    if modo == "📅 Período Específico":
        col1, col2 = st.columns(2)
        with col1:
            mes = st.selectbox(
                "Mês",
                list(range(1, 13)),
                format_func=lambda x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"][x-1],
                key="mes_especifico"
            )
        with col2:
            ano = st.number_input("Ano", min_value=2020, max_value=2030, value=2025, key="ano_especifico")
    
    elif modo == "📈 Comparativo de Meses":
        st.subheader("Mês 1 (Esquerda)")
        col1, col2 = st.columns(2)
        with col1:
            mes1 = st.selectbox(
                "Mês",
                list(range(1, 13)),
                format_func=lambda x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"][x-1],
                key="mes1"
            )
        with col2:
            ano1 = st.number_input("Ano", min_value=2020, max_value=2030, value=2025, key="ano1")
        
        st.divider()
        
        st.subheader("Mês 2 (Direita)")
        col3, col4 = st.columns(2)
        with col3:
            mes2 = st.selectbox(
                "Mês",
                list(range(1, 13)),
                format_func=lambda x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"][x-1],
                key="mes2",
                index=1
            )
        with col4:
            ano2 = st.number_input("Ano", min_value=2020, max_value=2030, value=2025, key="ano2")
    
    # Info de conexão
    st.markdown("---")
    st.caption("Conexão com banco de dados via SSH tunnel")

# MODE 1: Dashboard Geral
if modo == "📊 Dashboard Geral":
    st.header("Visão Geral - Todos os Tickets")
    
    try:
        with st.spinner("Carregando dados..."):
            servico = obter_servico_cache()
            
            # Obter resumo
            resumo = servico.obter_resumo()
            
            # Métricas principais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "📌 Total de Tickets",
                    formatar_numero(resumo['total']),
                    help="Todos os tickets no banco"
                )
            
            with col2:
                st.metric(
                    "✅ Abertos",
                    formatar_numero(resumo['abertos']),
                    delta=f"{100 * resumo['abertos'] / max(1, resumo['total']):.1f}%"
                )
            
            with col3:
                st.metric(
                    "✔️ Fechados",
                    formatar_numero(resumo['fechados']),
                    delta=f"{100 * resumo['fechados'] / max(1, resumo['total']):.1f}%"
                )
            
            with col4:
                taxa_fechamento = (resumo['fechados'] / max(1, resumo['total'])) * 100
                st.metric(
                    "📈 Taxa de Fechamento",
                    f"{taxa_fechamento:.1f}%"
                )
        
        st.markdown("---")
        
        # Top Módulos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📦 Top 10 Módulos/Componentes")
            top_modulos = servico.obter_top_modulos()
            
            if top_modulos:
                df_modulos = pd.DataFrame(
                    top_modulos,
                    columns=["Componente", "Total"]
                )
                
                # Gráfico
                st.bar_chart(
                    df_modulos.set_index("Componente"),
                    use_container_width=True
                )
                
                # Tabela
                st.dataframe(
                    df_modulos,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Sem dados")
        
        with col2:
            st.subheader("🖥️ Top 10 Servidores/Clusters")
            top_servidores = servico.obter_top_servidores()
            
            if top_servidores:
                df_servidores = pd.DataFrame(
                    top_servidores,
                    columns=["Servidor", "Total"]
                )
                
                # Gráfico
                st.bar_chart(
                    df_servidores.set_index("Servidor"),
                    use_container_width=True
                )
                
                # Tabela
                st.dataframe(
                    df_servidores,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Sem dados")
        
        st.markdown("---")
        
        # Tipologia e Origem
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Tipologia de Tickets")
            tipologia = servico.obter_tipologia()
            
            if tipologia:
                df_tipo = pd.DataFrame(
                    tipologia,
                    columns=["Tipo", "Total"]
                )
                
                # Pie chart com matplotlib
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.pie(df_tipo["Total"], labels=df_tipo["Tipo"], autopct="%1.1f%%", startangle=90)
                ax.set_title("Distribuição por Tipo")
                st.pyplot(fig)
                
                st.dataframe(
                    df_tipo,
                    use_container_width=True,
                    hide_index=True
                )
        
        with col2:
            st.subheader("👤 Origem dos Tickets (Top 5)")
            origem = servico.obter_origem()
            
            if origem:
                df_origem = pd.DataFrame(
                    origem[:5],
                    columns=["Relator", "Total"]
                )
                
                st.bar_chart(
                    df_origem.set_index("Relator"),
                    use_container_width=True
                )
                
                st.dataframe(
                    df_origem,
                    use_container_width=True,
                    hide_index=True
                )
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        st.exception(e)

# MODE 2: Período Específico
elif modo == "📅 Período Específico":
    st.header(f"Análise - {['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1]} de {ano}")
    
    try:
        with st.spinner(f"Carregando dados de {mes}/{ano}..."):
            servico = obter_servico_cache()
            
            # Resumo do período
            resumo_periodo = servico.obter_resumo(mes, ano)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total no Período",
                    formatar_numero(resumo_periodo['total']),
                )
            
            with col2:
                st.metric(
                    "Abertos",
                    formatar_numero(resumo_periodo['abertos']),
                )
            
            with col3:
                st.metric(
                    "Fechados",
                    formatar_numero(resumo_periodo['fechados']),
                )
        
        st.markdown("---")
        
        # Detalhes do período
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📦 Módulos neste Período")
            top_modulos_periodo = servico.obter_top_modulos(mes, ano)
            
            if top_modulos_periodo:
                df_m = pd.DataFrame(top_modulos_periodo, columns=["Componente", "Total"])
                st.bar_chart(df_m.set_index("Componente"), use_container_width=True)
                st.dataframe(df_m, use_container_width=True, hide_index=True)
            else:
                st.info("Sem dados para este período")
        
        with col2:
            st.subheader("🖥️ Servidores neste Período")
            top_serv_periodo = servico.obter_top_servidores(mes, ano)
            
            if top_serv_periodo:
                df_s = pd.DataFrame(top_serv_periodo, columns=["Servidor", "Total"])
                st.bar_chart(df_s.set_index("Servidor"), use_container_width=True)
                st.dataframe(df_s, use_container_width=True, hide_index=True)
            else:
                st.info("Sem dados para este período")
        
    except Exception as e:
        st.error(f"❌ Erro: {e}")

# MODE 3: Comparativo
elif modo == "📈 Comparativo":
    st.header(f"Comparativo - {['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1]} de {ano} vs Todos os Períodos")
    
    try:
        with st.spinner("Carregando dados..."):
            servico = obter_servico_cache()
            
            # Resumo geral
            resumo_geral = servico.obter_resumo()
            
            # Resumo do período
            resumo_periodo = servico.obter_resumo(mes, ano)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total Geral",
                    formatar_numero(resumo_geral['total']),
                )
                st.metric(
                    "Total no Período",
                    formatar_numero(resumo_periodo['total']),
                )
            
            with col2:
                pct_periodo = (resumo_periodo['total'] / max(1, resumo_geral['total'])) * 100
                st.metric(
                    "% do Total",
                    f"{pct_periodo:.1f}%",
                )
            
            with col3:
                st.metric(
                    "Diferença",
                    formatar_numero(resumo_geral['total'] - resumo_periodo['total']),
                )
        
        st.markdown("---")
        
        # Comparação de composição
        st.subheader("📊 Composição de Tipologia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Geral**")
            tipologia_geral = servico.obter_tipologia()
            if tipologia_geral:
                df_t_geral = pd.DataFrame(tipologia_geral, columns=["Tipo", "Total"])
                fig1, ax1 = plt.subplots(figsize=(6, 4))
                ax1.pie(df_t_geral["Total"], labels=df_t_geral["Tipo"], autopct="%1.1f%%")
                st.pyplot(fig1)
        
        with col2:
            st.write(f"**{['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1]}/{ano}**")
            tipologia_periodo = servico.obter_tipologia(mes, ano)
            if tipologia_periodo:
                df_t_per = pd.DataFrame(tipologia_periodo, columns=["Tipo", "Total"])
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                ax2.pie(df_t_per["Total"], labels=df_t_per["Tipo"], autopct="%1.1f%%")
                st.pyplot(fig2)
        
    except Exception as e:
        st.error(f"❌ Erro: {e}")

# MODE 4: Comparativo de Meses
elif modo == "📈 Comparativo de Meses":
    st.header("Comparativo Entre Dois Meses")
    
    mes_nome1 = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"][mes1-1]
    mes_nome2 = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"][mes2-1]
    
    try:
        with st.spinner(f"Carregando {mes_nome1}/{ano1} e {mes_nome2}/{ano2}..."):
            servico = obter_servico_cache()
            
            # Obter dados dos dois meses
            resumo1 = servico.obter_resumo(mes1, ano1)
            resumo2 = servico.obter_resumo(mes2, ano2)
            
            # Métricas principais lado a lado
            st.subheader("📊 Resumo Geral")
            col1, col2, col3 = st.columns([1, 0.1, 1])
            
            with col1:
                st.markdown(f"### 📅 {mes_nome1}/{ano1}")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric("Total", formatar_numero(resumo1['total']))
                with c2:
                    st.metric("Abertos", formatar_numero(resumo1['abertos']))
                with c3:
                    st.metric("Fechados", formatar_numero(resumo1['fechados']))
                with c4:
                    taxa1 = (resumo1['fechados'] / max(1, resumo1['total'])) * 100
                    st.metric("Taxa", f"{taxa1:.1f}%")
            
            with col2:
                st.write("")
            
            with col3:
                st.markdown(f"### 📅 {mes_nome2}/{ano2}")
                c5, c6, c7, c8 = st.columns(4)
                with c5:
                    st.metric("Total", formatar_numero(resumo2['total']))
                with c6:
                    st.metric("Abertos", formatar_numero(resumo2['abertos']))
                with c7:
                    st.metric("Fechados", formatar_numero(resumo2['fechados']))
                with c8:
                    taxa2 = (resumo2['fechados'] / max(1, resumo2['total'])) * 100
                    st.metric("Taxa", f"{taxa2:.1f}%")
            
            st.markdown("---")
            
            # Variações
            st.subheader("📈 Variações")
            col1, col2, col3 = st.columns([1, 0.1, 1])
            
            with col1:
                delta_total = resumo2['total'] - resumo1['total']
                delta_abertos = resumo2['abertos'] - resumo1['abertos']
                delta_fechados = resumo2['fechados'] - resumo1['fechados']
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Total", f"{delta_total:+d}", delta=delta_total)
                with c2:
                    st.metric("Abertos", f"{delta_abertos:+d}", delta=delta_abertos)
                with c3:
                    st.metric("Fechados", f"{delta_fechados:+d}", delta=delta_fechados)
            
            with col2:
                st.write("")
            
            with col3:
                pct_variacao = ((resumo2['total'] - resumo1['total']) / max(1, resumo1['total'])) * 100
                st.markdown(f"**Variação Total: {pct_variacao:+.1f}%**")
                
                if pct_variacao > 0:
                    st.info(f"📈 {mes_nome2}/{ano2} teve {pct_variacao:.1f}% mais tickets")
                elif pct_variacao < 0:
                    st.warning(f"📉 {mes_nome2}/{ano2} teve {abs(pct_variacao):.1f}% menos tickets")
                else:
                    st.success(f"➡️ Mesma quantidade de tickets")
            
            st.markdown("---")
            
            # Top Módulos lado a lado
            st.subheader("📦 Top Módulos/Componentes")
            col1, col2, col3 = st.columns([1, 0.05, 1])
            
            with col1:
                st.markdown(f"#### {mes_nome1}/{ano1}")
                top_modulos1 = servico.obter_top_modulos(mes1, ano1)
                if top_modulos1:
                    df_mod1 = pd.DataFrame(top_modulos1, columns=["Componente", "Total"])
                    st.dataframe(df_mod1, use_container_width=True, hide_index=True)
                    
                    fig1, ax1 = plt.subplots(figsize=(5, 4))
                    ax1.barh(df_mod1["Componente"], df_mod1["Total"], color='#667eea')
                    ax1.set_xlabel("Quantidade")
                    ax1.invert_yaxis()
                    st.pyplot(fig1)
            
            with col2:
                st.write("")
            
            with col3:
                st.markdown(f"#### {mes_nome2}/{ano2}")
                top_modulos2 = servico.obter_top_modulos(mes2, ano2)
                if top_modulos2:
                    df_mod2 = pd.DataFrame(top_modulos2, columns=["Componente", "Total"])
                    st.dataframe(df_mod2, use_container_width=True, hide_index=True)
                    
                    fig2, ax2 = plt.subplots(figsize=(5, 4))
                    ax2.barh(df_mod2["Componente"], df_mod2["Total"], color='#764ba2')
                    ax2.set_xlabel("Quantidade")
                    ax2.invert_yaxis()
                    st.pyplot(fig2)
            
            st.markdown("---")
            
            # Top Servidores lado a lado
            st.subheader("🖥️ Top Servidores/Clusters")
            col1, col2, col3 = st.columns([1, 0.05, 1])
            
            with col1:
                st.markdown(f"#### {mes_nome1}/{ano1}")
                top_serv1 = servico.obter_top_servidores(mes1, ano1)
                if top_serv1:
                    df_serv1 = pd.DataFrame(top_serv1, columns=["Servidor", "Total"])
                    st.dataframe(df_serv1, use_container_width=True, hide_index=True)
                    
                    fig3, ax3 = plt.subplots(figsize=(5, 4))
                    ax3.barh(df_serv1["Servidor"], df_serv1["Total"], color='#667eea')
                    ax3.set_xlabel("Quantidade")
                    ax3.invert_yaxis()
                    st.pyplot(fig3)
            
            with col2:
                st.write("")
            
            with col3:
                st.markdown(f"#### {mes_nome2}/{ano2}")
                top_serv2 = servico.obter_top_servidores(mes2, ano2)
                if top_serv2:
                    df_serv2 = pd.DataFrame(top_serv2, columns=["Servidor", "Total"])
                    st.dataframe(df_serv2, use_container_width=True, hide_index=True)
                    
                    fig4, ax4 = plt.subplots(figsize=(5, 4))
                    ax4.barh(df_serv2["Servidor"], df_serv2["Total"], color='#764ba2')
                    ax4.set_xlabel("Quantidade")
                    ax4.invert_yaxis()
                    st.pyplot(fig4)
            
            st.markdown("---")
            
            # Tipologia lado a lado
            st.subheader("📋 Tipologia (Tipo de Item)")
            col1, col2, col3 = st.columns([1, 0.05, 1])
            
            with col1:
                st.markdown(f"#### {mes_nome1}/{ano1}")
                tipologia1 = servico.obter_tipologia(mes1, ano1)
                if tipologia1:
                    df_tip1 = pd.DataFrame(tipologia1, columns=["Tipo", "Total"])
                    st.dataframe(df_tip1, use_container_width=True, hide_index=True)
                    
                    fig5, ax5 = plt.subplots(figsize=(5, 4))
                    ax5.pie(df_tip1["Total"], labels=df_tip1["Tipo"], autopct="%1.1f%%")
                    st.pyplot(fig5)
            
            with col2:
                st.write("")
            
            with col3:
                st.markdown(f"#### {mes_nome2}/{ano2}")
                tipologia2 = servico.obter_tipologia(mes2, ano2)
                if tipologia2:
                    df_tip2 = pd.DataFrame(tipologia2, columns=["Tipo", "Total"])
                    st.dataframe(df_tip2, use_container_width=True, hide_index=True)
                    
                    fig6, ax6 = plt.subplots(figsize=(5, 4))
                    ax6.pie(df_tip2["Total"], labels=df_tip2["Tipo"], autopct="%1.1f%%")
                    st.pyplot(fig6)
    
    except Exception as e:
        st.error(f"❌ Erro: {e}")

# Rodapé
st.markdown("---")
st.caption(f"AGT 4.0 Dashboard | Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | PostgreSQL 17")
