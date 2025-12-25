"""
Página 3: Teste de Conexão
"""

# ⚠️ IMPORTAR PRIMEIRO - FORÇA IPv4 GLOBALMENTE
from backend import ipv4_socket_wrapper

import streamlit as st
import sys
from pathlib import Path

st.set_page_config(page_title="Teste Conexão", page_icon="🧪", layout="wide")

# Configurar paths e tema
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from backend.theme_manager import configurar_tema_completo
from backend.footer_helper import exibir_rodape
configurar_tema_completo()

st.title("🧪 Teste de Conexão com Banco de Dados")
st.markdown("Verificar acesso ao PostgreSQL 17 via SSH Tunnel")
st.markdown("---")

if st.button("▶️ Executar Teste", use_container_width=True, type="primary"):
    with st.spinner("Testando conexão..."):
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from backend.unified_db_service import obter_servico
            
            servico = obter_servico()
            resumo = servico.obter_resumo()
            
            st.success("✅ Conexão bem-sucedida!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total de Tickets", resumo['total'])
            with col2:
                st.metric("✅ Abertos", resumo['abertos'])
            with col3:
                st.metric("✔️ Fechados", resumo['fechados'])
            
            st.markdown("---")
            st.subheader("📊 Dados do Banco:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Top 5 Módulos:**")
                modulos = servico.obter_top_modulos()[:5]
                for nome, total in modulos:
                    st.write(f"• {nome}: {total}")
            
            with col2:
                st.write("**Top 5 Servidores:**")
                servidores = servico.obter_top_servidores()[:5]
                for nome, total in servidores:
                    st.write(f"• {nome}: {total}")
            
        except Exception as e:
            st.error(f"❌ Erro na conexão: {e}")
            st.exception(e)

st.markdown("---")
st.info("💡 Se o teste falhar, verifique:\n1. SSH key em `backend/vps_key.pem`\n2. VPS IP: 91.108.124.150\n3. Porta: 5432")

# Rodapé com versão
exibir_rodape()
