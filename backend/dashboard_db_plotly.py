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
        
        # Gráfico 1: Tipologia Distribution
        st.subheader("📊 Distribuição por Tipologia")
        tipologia = servico.obter_tipologia()
        if tipologia:
            df_tipo = pd.DataFrame(tipologia, columns=['status', 'quantidade'])
            fig = px.pie(
                df_tipo, 
                values='quantidade', 
                names='status',
                title="Tickets por Status",
                color_discrete_sequence=px.colors.sequential.Blues
            )
            fig.update_traces(textposition='outside', textinfo='label+percent', 
                            textfont=dict(size=14, weight='bold'))
            fig.update_layout(height=750, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico 2: Relator Distribution
        st.subheader("👤 Distribuição por Relator")
        origem = servico.obter_origem()
        if origem:
            df_origem = pd.DataFrame(origem, columns=['relator', 'quantidade'])
            fig = px.bar(
                df_origem,
                x='relator',
                y='quantidade',
                title="Tickets por Relator",
                color='relator',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_layout(height=400, xaxis_title="Relator", yaxis_title="Quantidade")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico 3: Top Responsáveis
        st.subheader("👤 Top 10 Responsáveis")
        responsaveis = servico.obter_top_responsaveis()
        if responsaveis:
            df_responsaveis = pd.DataFrame(responsaveis[:10], columns=['responsavel', 'quantidade']).sort_values('quantidade')
            fig = px.bar(
                df_responsaveis,
                x='quantidade',
                y='responsavel',
                orientation='h',
                title="Responsáveis com Mais Tickets",
                color='quantidade',
                color_continuous_scale="Blues"
            )
            fig.update_layout(height=400, xaxis_title="Quantidade", yaxis_title="Responsável")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Gráfico 4: Top Servidores
        st.subheader("🖥️ Top 10 Servidores")
        servidores = servico.obter_top_servidores()
        if servidores:
            df_servidores = pd.DataFrame(servidores[:10], columns=['servidor', 'quantidade']).sort_values('quantidade')
            fig = px.bar(
                df_servidores,
                x='quantidade',
                y='servidor',
                orientation='h',
                title="Servidores com Mais Tickets",
                color='quantidade',
                color_continuous_scale="Blues"
            )
            fig.update_layout(height=400, xaxis_title="Quantidade", yaxis_title="Servidor")
            st.plotly_chart(fig, use_container_width=True)
    
    elif modo == "📅 Período Específico":
        st.subheader(f"📅 Período: {mes}/{ano}")
        
        # Dados do período
        dados_periodo = servico.obter_tickets_por_periodo(mes, ano)
        if not dados_periodo.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", len(dados_periodo))
            with col2:
                st.metric("Abertos", len(dados_periodo[dados_periodo['status'] != 'Fechado']))
            
            # Gráfico temporal
            if 'data_criacao' in dados_periodo.columns:
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
        
        dados1 = servico.obter_tickets_por_periodo(mes1, ano1)
        dados2 = servico.obter_tickets_por_periodo(mes2, ano2)
        
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
                color_discrete_sequence=['#0D47A1', '#42A5F5']
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
