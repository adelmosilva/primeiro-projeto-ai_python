"""
Dashboard Streamlit integrado com banco de dados PostgreSQL
AGT 4.0 v2.0 - Database Edition
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

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
        ["📊 Dashboard Geral", "📅 Período Específico", "📈 Comparativo"]
    )
    
    # Opções de período
    if modo in ["📅 Período Específico", "📈 Comparativo"]:
        mes = st.selectbox(
            "Mês",
            list(range(1, 13)),
            format_func=lambda x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                                   "Jul", "Ago", "Set", "Out", "Nov", "Dez"][x-1]
        )
        ano = st.number_input("Ano", min_value=2020, max_value=2030, value=2025)
    else:
        mes, ano = None, None
    
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
                
                st.pie_chart(
                    data=df_tipo.set_index("Tipo")["Total"],
                    use_container_width=True
                )
                
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
                st.pie_chart(df_t_geral.set_index("Tipo")["Total"])
        
        with col2:
            st.write(f"**{['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][mes-1]}/{ano}**")
            tipologia_periodo = servico.obter_tipologia(mes, ano)
            if tipologia_periodo:
                df_t_per = pd.DataFrame(tipologia_periodo, columns=["Tipo", "Total"])
                st.pie_chart(df_t_per.set_index("Tipo")["Total"])
        
    except Exception as e:
        st.error(f"❌ Erro: {e}")

# Rodapé
st.markdown("---")
st.caption(f"AGT 4.0 Dashboard | Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | PostgreSQL 17")
