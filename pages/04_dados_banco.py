"""
Página 4: Ver Dados do Banco
"""

import streamlit as st
import sys
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Dados Banco", page_icon="👀", layout="wide")

# Configurar paths e tema
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.theme_manager import configurar_tema_completo
from backend.footer_helper import exibir_rodape
configurar_tema_completo()

st.title("👀 Dados do Banco de Dados")
st.markdown("Preview dos módulos, servidores e tipologia")
st.markdown("---")

try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from backend.servico_tickets import obter_servico
    
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
            st.metric("Fechados", resumo['fechados'])
        with col4:
            taxa = (resumo['fechados'] / max(1, resumo['total'])) * 100
            st.metric("Taxa de Fechamento", f"{taxa:.1f}%")
    
    with tab2:
        st.subheader("Top 10 Módulos/Componentes")
        modulos = servico.obter_top_modulos()
        if modulos:
            df = pd.DataFrame(modulos, columns=["Componente", "Total"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.bar_chart(df.set_index("Componente"))
    
    with tab3:
        st.subheader("Top 10 Servidores/Clusters")
        servidores = servico.obter_top_servidores()
        if servidores:
            df = pd.DataFrame(servidores, columns=["Servidor", "Total"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.bar_chart(df.set_index("Servidor"))
    
    with tab4:
        st.subheader("Tipologia dos Tickets")
        tipologia = servico.obter_tipologia()
        if tipologia:
            df = pd.DataFrame(tipologia, columns=["Tipo", "Total"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Pie chart com matplotlib
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(df["Total"], labels=df["Tipo"], autopct="%1.1f%%", startangle=90)
            ax.set_title("Distribuição por Tipo")
            st.pyplot(fig)
    
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.exception(e)

st.markdown("---")
st.caption("Dados atualizados em tempo real do PostgreSQL 17")

# Rodapé com versão
exibir_rodape()
