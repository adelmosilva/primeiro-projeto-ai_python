"""
Página 1: Dashboard com Banco de Dados - Carregamento Automático
"""

import streamlit as st
import sys
from pathlib import Path

# Configurar página
st.set_page_config(page_title="Dashboard DB", page_icon="📊", layout="wide")

# Adicionar backend ao path
PROJETO_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJETO_DIR))

# Executar o dashboard_db.py
exec(open(PROJETO_DIR / "backend" / "dashboard_db.py").read())
