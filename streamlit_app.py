"""
AGT 4.0 - App Principal do Streamlit Cloud
"""

# ⚠️ IMPORTAR PRIMEIRO - FORÇA IPv4 GLOBALMENTE
from backend import ipv4_socket_wrapper

import streamlit as st
from pathlib import Path
import sys

# Adicionar paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

# Importar tema manager e versão
from backend.theme_manager import configurar_tema_completo
from backend.version import get_version

st.set_page_config(
    page_title="AGT 4.0 - Sistema de Análise de Tickets",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar tema
configurar_tema_completo()

st.title("📊 AGT 4.0 - Sistema de Análise de Tickets")
st.info("""
Bem-vindo ao AGT 4.0!

Selecione uma opção no menu lateral para começar:
- **Dashboard DB**: Análise integrada com banco de dados PostgreSQL
- **Dashboard Upload**: Análise de arquivos CSV locais
- **Teste de Conexão**: Verificar status da conexão com o banco
- **Dados do Banco**: Visualizar dados armazenados
- **Status**: Status do sistema
""")

# Rodapé com versão
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"<p style='text-align: center; color: gray; font-size: 12px;'>AGT 4.0 {get_version()}</p>", unsafe_allow_html=True)
