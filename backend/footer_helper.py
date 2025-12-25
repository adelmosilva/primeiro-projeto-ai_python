"""
Helper para exibir rodapé com versão em todas as páginas
"""

import streamlit as st
from backend.version import get_version

def exibir_rodape():
    """Exibe rodapé padrão com versão em todas as páginas"""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"<p style='text-align: center; color: gray; font-size: 12px;'>AGT 4.0 {get_version()}</p>",
            unsafe_allow_html=True
        )
