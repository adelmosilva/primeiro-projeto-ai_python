"""
Página 2: Dashboard com Upload de CSV
"""

import streamlit as st
from pathlib import Path
import sys

# Configurar página
st.set_page_config(
    page_title="Dashboard Upload",
    page_icon="📁",
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
    # Importar direto os módulos necessários
    from app.utils.jira_parser import parser_jira_csv
    from app.services.ticket_service import TicketService
    from app.services.analysis_service import AnalysisService
    from app.services.pdf_report_service import PDFReportService
    from app.config import REPORTS_OUTPUT_DIR, UPLOADS_DIR
    from backend.auto_migrar import migrar_csv_para_banco
    import pandas as pd
    import matplotlib.pyplot as plt
    from datetime import datetime
    import hashlib
    import json
    
    # Agora carregar o dashboard
    exec(open(PROJECT_ROOT / "backend" / "dashboard.py", encoding='utf-8').read())
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulo: {e}")
    st.info("Verifique se todos os arquivos estão no lugar correto:")
    st.code(f"""
backend/
  ├── dashboard.py
  ├── auto_migrar.py
  └── app/
      ├── utils/
      │   └── jira_parser.py
      ├── services/
      │   ├── ticket_service.py
      │   ├── analysis_service.py
      │   └── pdf_report_service.py
      └── config.py
    """)
except Exception as e:
    st.error(f"❌ Erro ao carregar dashboard: {e}")
    import traceback
    st.code(traceback.format_exc())

# Rodapé com versão
exibir_rodape()
