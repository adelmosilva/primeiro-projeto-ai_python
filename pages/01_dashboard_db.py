"""
Página 1: Dashboard com Banco de Dados - Carregamento Automático
"""

import streamlit as st
import sys
from pathlib import Path

# Configurar página
st.set_page_config(page_title="Dashboard DB", page_icon="📊", layout="wide")

# Adicionar backend ao path (IMPORTANTE: antes de fazer exec)
PROJETO_DIR = Path(__file__).parent.parent
BACKEND_DIR = PROJETO_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(PROJETO_DIR))

# Executar o dashboard_db.py com encoding utf-8
with open(BACKEND_DIR / "dashboard_db.py", "r", encoding="utf-8") as f:
    # Substituir o sys.path.insert para usar os caminhos corretos
    code = f.read()
    code = code.replace('sys.path.insert(0, str(Path(__file__).parent.parent))', 
                        f'sys.path.insert(0, "{BACKEND_DIR}")\nsys.path.insert(0, "{PROJETO_DIR}")')
    exec(code)
