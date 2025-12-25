"""
Página 2: Dashboard com Upload de CSV - Carregamento Automático
"""

import streamlit as st
from pathlib import Path
import sys

# Configurar página
st.set_page_config(page_title="Dashboard Upload", page_icon="📁", layout="wide")

# Adicionar pages ao path para importar o loader
PAGES_DIR = Path(__file__).parent
sys.path.insert(0, str(PAGES_DIR))

# Importar e usar o loader
from _dashboard_loader import load_dashboard

# Carregar o dashboard
load_dashboard("dashboard.py")
