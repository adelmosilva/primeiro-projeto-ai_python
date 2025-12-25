"""
Página 2: Dashboard com Upload de CSV - Carregamento Automático
"""

import streamlit as st
import sys
from pathlib import Path

# Configurar página
st.set_page_config(page_title="Dashboard Upload", page_icon="📁", layout="wide")

# Adicionar backend ao path
PROJETO_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJETO_DIR))

# Executar o dashboard.py com encoding utf-8
with open(PROJETO_DIR / "backend" / "dashboard.py", "r", encoding="utf-8") as f:
    exec(f.read())
