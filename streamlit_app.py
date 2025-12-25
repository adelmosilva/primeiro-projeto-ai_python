"""
AGT 4.0 - App Principal do Streamlit Cloud
"""

import streamlit as st
from pathlib import Path
import sys

# Adicionar paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

st.set_page_config(
    page_title="AGT 4.0 - Sistema de Análise de Tickets",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
