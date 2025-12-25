"""
Página 1: Dashboard com Banco de Dados PostgreSQL
"""

# ⚠️ IMPORTAR PRIMEIRO - FORÇA IPv4 GLOBALMENTE
from backend import ipv4_socket_wrapper

import streamlit as st
from pathlib import Path
import sys

# Configurar página
st.set_page_config(
    page_title="Dashboard DB",
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
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    # Agora carregar o dashboard
    exec(open(PROJECT_ROOT / "backend" / "dashboard_db.py", encoding='utf-8').read())
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulo: {e}")
    st.info("Verifique se todos os arquivos estão no lugar correto:")
    st.code(f"""
backend/
  ├── servico_tickets.py
  ├── dashboard_db.py
  └── app/
      ├── services/
      │   └── analysis_service.py
      └── config.py
    """)
except Exception as e:
    st.error(f"❌ Erro ao carregar dashboard: {e}")
    import traceback
    st.code(traceback.format_exc())

# Rodapé com versão
exibir_rodape()
