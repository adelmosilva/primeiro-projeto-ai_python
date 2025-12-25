"""
AGT 4.0 - Página Inicial / Home
Sistema de Análise de Tickets com Navegação estilo Website
"""

import streamlit as st
from pathlib import Path
import sys

# Configurar página
st.set_page_config(
    page_title="AGT 4.0 - Home",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
<style>
    /* Remover sidebar no home */
    [data-testid="collapsedControl"] {
        display: none
    }
    
    /* Card styling */
    .card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        transition: transform 0.3s;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .card-title {
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .card-desc {
        font-size: 1em;
        opacity: 0.9;
        line-height: 1.6;
    }
    
    .features {
        font-size: 0.9em;
        text-align: left;
        margin-top: 1rem;
        opacity: 0.8;
    }
    
    /* Header styling */
    .header-main {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 3rem;
    }
    
    .header-title {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2em;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-main">
    <div class="header-title">📊 AGT 4.0</div>
    <div class="header-subtitle">Sistema de Análise de Tickets</div>
    <div style="margin-top: 1rem; font-size: 0.95em; opacity: 0.8;">
        Gerenciamento inteligente de tickets com PostgreSQL 17 e SSH Tunnel
    </div>
</div>
""", unsafe_allow_html=True)

# Informações principais
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📦 Total de Tickets", "280")
with col2:
    st.metric("✅ Abertos", "280")
with col3:
    st.metric("📈 Taxa de Fechamento", "0%")

st.markdown("---")

# Seção de Dashboards
st.header("🎯 Escolha sua Forma de Análise")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Dashboard com Banco</div>
        <div class="card-desc">
            Dados em tempo real do PostgreSQL
        </div>
        <div class="features">
            ✅ Dados em tempo real<br>
            ✅ 3 modos de visualização<br>
            ✅ Sem limites de dados<br>
            ✅ Performance otimizada<br>
            ✅ Gráficos interativos
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("🚀 Abrir Dashboard com Banco", key="btn_db", use_container_width=True):
        st.switch_page("pages/01_dashboard_db.py")

with col2:
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <div class="card-title">📁 Dashboard com Upload</div>
        <div class="card-desc">
            Importar e analisar novos CSVs
        </div>
        <div class="features">
            ✅ Upload de CSV do Jira<br>
            ✅ Análise por período<br>
            ✅ Comparativo entre períodos<br>
            ✅ Geração de PDF<br>
            ✅ Dados flexíveis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("📤 Abrir Dashboard Upload", key="btn_upload", use_container_width=True):
        st.switch_page("pages/02_dashboard_upload.py")

st.markdown("---")

# Seção de Ferramentas
st.header("🔧 Ferramentas e Utilitários")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    if st.button("🧪 Testar Conexão", key="btn_teste", use_container_width=True):
        st.switch_page("pages/03_teste_conexao.py")
    st.caption("Verificar acesso ao PostgreSQL")

with col2:
    if st.button("👀 Ver Dados do Banco", key="btn_dados", use_container_width=True):
        st.switch_page("pages/04_dados_banco.py")
    st.caption("Preview de módulos e servidores")

with col3:
    if st.button("📋 Status do Sistema", key="btn_status", use_container_width=True):
        st.switch_page("pages/05_status.py")
    st.caption("Informações de implementação")

st.markdown("---")

# Seção de informações
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Estatísticas")
    st.write("""
    - **280 Tickets** migrados
    - **4 Componentes**: Middleware, Database, Infraestruturas, MFT Server
    - **10+ Servidores**: PSRM, Batch Server, Portal, etc.
    - **4 Tipos**: Support, Tarefa, Incident, Iniciativa
    - **5+ Relatores**: Abraão, Souleimar, Octavio, etc.
    """)

with col2:
    st.subheader("🔐 Segurança")
    st.write("""
    - ✅ Conexão via SSH Tunnel
    - ✅ Chave Ed25519
    - ✅ PostgreSQL 17 encriptado
    - ✅ Sem exposição direta do banco
    - ✅ Acesso controlado via VPS
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; opacity: 0.6; font-size: 0.9em;">
    <p>AGT 4.0 - Sistema de Análise de Tickets | Versão Database Edition v1.0</p>
    <p>Desenvolvido com ❤️ usando Streamlit + PostgreSQL 17</p>
</div>
""", unsafe_allow_html=True)
