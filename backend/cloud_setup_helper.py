"""
Componente para mostrar mensagem de setup do banco de dados
"""

import streamlit as st

def mostrar_alerta_banco_cloud():
    """Mostra alerta quando não conseguir conectar ao banco no Streamlit Cloud"""
    with st.sidebar:
        st.warning("""
        ⚠️ **Banco de Dados**
        
        O banco está em servidor privado.
        Consulte `DATABASE_CLOUD_SETUP.md` para configurar acesso na nuvem.
        
        **Opções:**
        1. Usar Supabase (gratuito)
        2. Usar ngrok (tunnel)
        3. Criar API intermediária
        """)
