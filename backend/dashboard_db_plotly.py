"""
Dashboard Streamlit com Plotly para gráficos interativos
Versão Plotly do dashboard_db.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# USAR unified_db_service em vez de servico_tickets direto
from backend.unified_db_service import obter_servico
from app.services.analysis_service import AnalysisService
from app.services.pdf_report_service import PDFReportService
from app.config import REPORTS_OUTPUT_DIR

# Configurar página
st.set_page_config(
    page_title="AGT 4.0 - Dashboard (Plotly)",
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
st.title("📊 AGT 4.0 - Dashboard com Plotly")
st.markdown("Análise interativa de tickets com gráficos Plotly")
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
            ano = st.number_input("Ano", value=datetime.now().year, min_value=2020)
    
    elif modo == "📈 Comparativo de Meses":
        st.subheader("Período 1")
        col1, col2 = st.columns(2)
        with col1:
            mes1 = st.selectbox(
                "Mês 1",
                list(range(1, 13)),
                format_func=lambda x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"][x-1],
                key="mes1"
            )
        with col2:
            ano1 = st.number_input("Ano 1", value=datetime.now().year, min_value=2020, key="ano1")
        
        st.subheader("Período 2")
        col3, col4 = st.columns(2)
        with col3:
            mes2 = st.selectbox(
                "Mês 2",
                list(range(1, 13)),
                format_func=lambda x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"][x-1],
                key="mes2"
            )
        with col4:
            ano2 = st.number_input("Ano 2", value=datetime.now().year, min_value=2020, key="ano2")

# Tenta carregar dados
try:
    servico = obter_servico_cache()
    
    if modo == "📊 Dashboard Geral":
        # ========== RESUMO GERAL ==========
        st.subheader("📊 Resumo Geral")
        
        resumo = servico.obter_resumo()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📌 Total", formatar_numero(resumo['total']))
        with col2:
            st.metric("✅ Abertos", formatar_numero(resumo['abertos']))
        with col3:
            st.metric("✔️ Fechados", formatar_numero(resumo['fechados']))
        
        st.markdown("---")
        
        # ========== GRÁFICOS INTERATIVOS COM PLOTLY ==========
        
        # Gráfico 1: Status Distribution
        st.subheader("📊 Distribuição de Status")
        resumo_status = servico.obter_resumo_por_status()
        if not resumo_status.empty:
            fig = px.pie(
                resumo_status, 
                values='quantidade', 
                names='status',
                title="Tickets por Status",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico 2: Prioridade Distribution
        st.subheader("🎯 Distribuição por Prioridade")
        resumo_prioridade = servico.obter_resumo_por_prioridade()
        if not resumo_prioridade.empty:
            fig = px.bar(
                resumo_prioridade,
                x='prioridade',
                y='quantidade',
                title="Tickets por Prioridade",
                color='prioridade',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_layout(height=400, xaxis_title="Prioridade", yaxis_title="Quantidade")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico 3: Componentes
        st.subheader("📦 Top 10 Componentes")
        resumo_componentes = servico.obter_resumo_por_componente()
        if not resumo_componentes.empty:
            top10 = resumo_componentes.head(10).sort_values('quantidade')
            fig = px.barh(
                top10,
                x='quantidade',
                y='componente',
                title="Componentes com Mais Tickets",
                color='quantidade',
                color_continuous_scale="Viridis"
            )
            fig.update_layout(height=400, xaxis_title="Quantidade", yaxis_title="Componente")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico 4: Servidores
        st.subheader("🖥️ Top 10 Servidores")
        resumo_servidores = servico.obter_resumo_por_servidor()
        if not resumo_servidores.empty:
            top10 = resumo_servidores.head(10).sort_values('quantidade')
            fig = px.barh(
                top10,
                x='quantidade',
                y='servidor',
                title="Servidores com Mais Tickets",
                color='quantidade',
                color_continuous_scale="Blues"
            )
            fig.update_layout(height=400, xaxis_title="Quantidade", yaxis_title="Servidor")
            st.plotly_chart(fig, use_container_width=True)
    
    elif modo == "📅 Período Específico":
        st.subheader(f"📅 Período: {mes}/{ano}")
        
        # Dados do período
        dados_periodo = servico.obter_tickets_por_mes(mes, ano)
        if not dados_periodo.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", len(dados_periodo))
            with col2:
                st.metric("Abertos", len(dados_periodo[dados_periodo['status'] == 'Aberto']))
            with col3:
                st.metric("Fechados", len(dados_periodo[dados_periodo['status'] == 'Fechado']))
            
            # Gráfico temporal
            fig = px.histogram(
                dados_periodo,
                x='data_criacao',
                nbins=30,
                title=f"Distribuição Temporal - {mes}/{ano}",
                color_discrete_sequence=['#636EFA']
            )
            fig.update_layout(height=400, xaxis_title="Data", yaxis_title="Quantidade")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado disponível para este período")
    
    elif modo == "📈 Comparativo de Meses":
        st.subheader(f"📈 Comparando {mes1}/{ano1} vs {mes2}/{ano2}")
        
        dados1 = servico.obter_tickets_por_mes(mes1, ano1)
        dados2 = servico.obter_tickets_por_mes(mes2, ano2)
        
        if not dados1.empty and not dados2.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"Total {mes1}/{ano1}", len(dados1))
            with col2:
                st.metric(f"Total {mes2}/{ano2}", len(dados2))
            with col3:
                variacao = ((len(dados2) - len(dados1)) / len(dados1) * 100) if len(dados1) > 0 else 0
                st.metric("Variação %", f"{variacao:.1f}%")
            with col4:
                diferenca = len(dados2) - len(dados1)
                st.metric("Diferença", diferenca)
            
            # Gráfico comparativo
            dados_comparacao = pd.DataFrame({
                f'{mes1}/{ano1}': [len(dados1)],
                f'{mes2}/{ano2}': [len(dados2)]
            }).T.reset_index()
            dados_comparacao.columns = ['Período', 'Quantidade']
            
            fig = px.bar(
                dados_comparacao,
                x='Período',
                y='Quantidade',
                title="Comparativo de Períodos",
                color='Período',
                color_discrete_sequence=['#AB63FA', '#FFA15A']
            )
            fig.update_layout(height=400, yaxis_title="Quantidade")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado disponível para os períodos selecionados")

except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.info("Verifique sua conexão com o banco de dados")

st.markdown("---")
st.info("💡 Dashboard criado com Plotly para interatividade total")
