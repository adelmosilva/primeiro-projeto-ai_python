"""
Página 1: Dashboard - Visão Geral - Todos os Tickets
Visualizações interativas com Plotly
"""

# ⚠️ IMPORTAR PRIMEIRO - FORÇA IPv4 GLOBALMENTE
from backend import ipv4_socket_wrapper

import streamlit as st
from pathlib import Path
import sys

# Configurar página
st.set_page_config(
    page_title="Visão Geral - Todos os Tickets",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

# Importar tema manager
from backend.theme_manager import configurar_tema_completo
from backend.footer_helper import exibir_rodape

# Configurar tema
configurar_tema_completo()

try:
    # Importar do unified_db_service em vez de servico_tickets diretamente
    from backend.unified_db_service import obter_servico
    from app.services.analysis_service import AnalysisService
    from app.config import REPORTS_OUTPUT_DIR
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime
    
    # Agora carregar o dashboard
    exec(open(PROJECT_ROOT / "backend" / "dashboard_db_plotly.py", encoding='utf-8').read())
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulo: {e}")
    st.info("Verifique se todos os arquivos estão no lugar correto:")
    st.code(f"""
backend/
  dashboard_db_plotly.py
  unified_db_service.py
  servico_tickets.py
""")

# Rodapé
exibir_rodape()
