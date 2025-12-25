"""
Página 4: Resumo Geral - Ver Dados do Banco
Versão interativa com Plotly
"""

# ⚠️ IMPORTAR PRIMEIRO - FORÇA IPv4 GLOBALMENTE
from backend import ipv4_socket_wrapper

import streamlit as st
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Resumo Geral", page_icon="👀", layout="wide")

# Configurar paths e tema
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.theme_manager import configurar_tema_completo
from backend.footer_helper import exibir_rodape
configurar_tema_completo()

st.title("👀 Resumo Geral")
st.markdown("Visualizações interativas do banco de dados com Plotly")
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
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", resumo['total'])
        with col2:
            st.metric("Abertos", resumo['abertos'])
        with col3:
            st.metric("Fechados", resumo['fechados'])
        
        st.markdown("---")
        
        # Gráfico de Status com mais detalhes
        st.subheader("📊 Distribuição de Status")
        tipologia = servico.obter_tipologia()
        if tipologia:
            df_tipo = pd.DataFrame(tipologia, columns=['status', 'quantidade'])
            # Gráfico de barras horizontal com mais informações
            fig = px.bar(
                df_tipo.sort_values('quantidade', ascending=True),
                x='quantidade',
                y='status',
                orientation='h',
                title="Distribuição por Tipologia",
                color='quantidade',
                color_continuous_scale="Blues",
                text='quantidade',
                hover_data={'quantidade': True, 'status': True}
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                height=450,
                showlegend=False,
                xaxis_title="Quantidade de Tickets",
                yaxis_title="Tipo/Status"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🧑 Top 20 em Atendimento")
        responsaveis = servico.obter_top_responsaveis()
        
        if responsaveis:
            df_responsaveis = pd.DataFrame(responsaveis[:20], columns=['responsavel', 'total']).sort_values('total')
            
            fig = px.bar(
                df_responsaveis,
                x='total',
                y='responsavel',
                orientation='h',
                title="Responsáveis em Atendimento",
                color='total',
                color_continuous_scale="Blues",
                hover_data={'total': True}
            )
            fig.update_layout(
                height=600,
                xaxis_title="Quantidade de Tickets",
                yaxis_title="Responsável"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela com números
            st.markdown("---")
            st.subheader("Dados Tabulares")
            st.dataframe(pd.DataFrame(responsaveis[:20], columns=['Responsável', 'Total']), use_container_width=True)
        else:
            st.warning("Nenhum dado de responsáveis disponível")
    
    with tab3:
        st.subheader("🖥️ Top 20 Servidores")
        servidores = servico.obter_top_servidores()
        
        if servidores:
            df_servidores = pd.DataFrame(servidores[:20], columns=['servidor', 'quantidade']).sort_values('quantidade')
            
            fig = px.bar(
                df_servidores,
                x='quantidade',
                y='servidor',
                orientation='h',
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
            st.dataframe(pd.DataFrame(servidores[:20], columns=['Servidor', 'Quantidade']), use_container_width=True)
        else:
            st.warning("Nenhum dado de servidores disponível")
    
    with tab4:
        st.subheader("📋 Tipologia de Tickets")
        
        st.subheader("Por Origem")
        origem = servico.obter_origem()
        if origem:
            df_origem = pd.DataFrame(origem, columns=['origem', 'quantidade'])
            fig = px.bar(
                df_origem,
                x='origem',
                y='quantidade',
                title="Tickets por Origem",
                color='origem',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Erro: {e}")
    st.info("Verifique sua conexão com o banco de dados")

st.markdown("---")
exibir_rodape()
