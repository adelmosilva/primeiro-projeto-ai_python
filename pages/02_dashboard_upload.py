"""
Página 2: Dashboard com Upload de CSV
"""

import streamlit as st
st.set_page_config(page_title="Dashboard Upload", page_icon="📁", layout="wide")

st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h1>📁 Redirecionando...</h1>
    <p>Iniciando Dashboard com Upload de CSV</p>
</div>
""", unsafe_allow_html=True)

from pathlib import Path

PROJETO_DIR = Path(__file__).parent.parent
DASHBOARD_UPLOAD = PROJETO_DIR / "backend" / "dashboard.py"

st.info("O Dashboard será aberto em uma nova aba. Execute o comando abaixo no terminal:")
st.code(f"streamlit run {DASHBOARD_UPLOAD}", language="bash")

st.markdown("---")

st.subheader("✨ Funcionalidades:")
st.write("""
- Fazer upload de arquivos CSV do Jira
- Analisar período específico
- Comparar entre dois períodos
- Gerar relatórios em PDF
""")

st.markdown("---")
st.markdown("Ou use o launcher automático: `python iniciar.py` → Opção 2")
