"""
Página 1: Dashboard com Banco de Dados
"""

import streamlit as st
st.set_page_config(page_title="Dashboard DB", page_icon="📊", layout="wide")

st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h1>📊 Redirecionando...</h1>
    <p>Iniciando Dashboard com Banco de Dados</p>
</div>
""", unsafe_allow_html=True)

import subprocess
import sys
from pathlib import Path

PROJETO_DIR = Path(__file__).parent.parent
DASHBOARD_DB = PROJETO_DIR / "backend" / "dashboard_db.py"

st.info("O Dashboard será aberto em uma nova aba. Execute o comando abaixo no terminal:")
st.code(f"streamlit run {DASHBOARD_DB}", language="bash")

st.markdown("---")
st.markdown("Ou use o launcher automático: `python iniciar.py` → Opção 1")
