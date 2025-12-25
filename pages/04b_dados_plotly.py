"""
Página 4B: Ver Dados do Banco com Plotly
Versão interativa com Plotly em vez de Streamlit charts
"""

# ⚠️ IMPORTAR PRIMEIRO - FORÇA IPv4 GLOBALMENTE
from backend import ipv4_socket_wrapper

import streamlit as st
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Dados Banco (Plotly)", page_icon="👀", layout="wide")

# Configurar paths e tema
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.theme_manager import configurar_tema_completo
from backend.footer_helper import exibir_rodape
configurar_tema_completo()

st.title("👀 Dados do Banco de Dados (Plotly)")
st.markdown("Preview com visualizações interativas via Plotly")
st.markdown("---")

try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from backend.unified_db_service import obter_servico
    
    servico = obter_servico()
    
    # Abas
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumo", "📦 Módulos", "🖥️ Servidores", "📋 Tipologia"])
    
    with tab1:
        st.subheader("Resumo Geral")
        resumo = servico.obter_resumo()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", resumo['total'])
        with col2:
            st.metric("Abertos", resumo['abertos'])
        with col3:
            st.metric("Em Progresso", resumo['em_progresso'])
        with col4:
            st.metric("Fechados", resumo['fechados'])
        
        st.markdown("---")
        
        # Gráfico de Status
        st.subheader("Status Distribution")
        status_data = servico.obter_resumo_por_status()
        if not status_data.empty:
            fig = px.pie(
                status_data,
                values='quantidade',
                names='status',
                title="Distribuição de Status",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📦 Top 20 Módulos/Componentes")
        componentes = servico.obter_resumo_por_componente()
        
        if not componentes.empty:
            top20 = componentes.head(20).sort_values('quantidade')
            
            fig = px.barh(
                top20,
                x='quantidade',
                y='componente',
                title="Componentes mais acionados",
                color='quantidade',
                color_continuous_scale="Viridis",
                hover_data={'quantidade': True}
            )
            fig.update_layout(
                height=600,
                xaxis_title="Quantidade de Tickets",
                yaxis_title="Componente"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela com números
            st.markdown("---")
            st.subheader("Dados Tabulares")
            st.dataframe(componentes.head(20), use_container_width=True)
        else:
            st.warning("Nenhum dado de componentes disponível")
    
    with tab3:
        st.subheader("🖥️ Top 20 Servidores")
        servidores = servico.obter_resumo_por_servidor()
        
        if not servidores.empty:
            top20 = servidores.head(20).sort_values('quantidade')
            
            fig = px.barh(
                top20,
                x='quantidade',
                y='servidor',
                title="Servidores mais acionados",
                color='quantidade',
                color_continuous_scale="Blues",
                hover_data={'quantidade': True}
            )
            fig.update_layout(
                height=600,
                xaxis_title="Quantidade de Tickets",
                yaxis_title="Servidor"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela com números
            st.markdown("---")
            st.subheader("Dados Tabulares")
            st.dataframe(servidores.head(20), use_container_width=True)
        else:
            st.warning("Nenhum dado de servidores disponível")
    
    with tab4:
        st.subheader("📋 Tipologia de Tickets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Por Status")
            status_data = servico.obter_resumo_por_status()
            if not status_data.empty:
                fig = px.bar(
                    status_data,
                    x='status',
                    y='quantidade',
                    title="Tickets por Status",
                    color='status',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Por Prioridade")
            prioridade_data = servico.obter_resumo_por_prioridade()
            if not prioridade_data.empty:
                fig = px.bar(
                    prioridade_data,
                    x='prioridade',
                    y='quantidade',
                    title="Tickets por Prioridade",
                    color='prioridade',
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Erro: {e}")
    st.info("Verifique sua conexão com o banco de dados")

st.markdown("---")
exibir_rodape()
