"""
Página 5: Status do Sistema
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Status", page_icon="📋", layout="wide")

st.title("📋 Status do Sistema AGT 4.0")
st.markdown("---")

# Status de implementação
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Implementado")
    st.write("""
    - ✅ Banco de Dados PostgreSQL 17
    - ✅ SSH Tunnel com Ed25519
    - ✅ Serviço de Tickets (8 métodos)
    - ✅ Dashboard com Banco (3 modos)
    - ✅ Dashboard com Upload (CSV)
    - ✅ 280 Tickets Migrados
    - ✅ Testes Automatizados
    - ✅ Documentação Completa
    - ✅ Página Inicial (Home)
    """)

with col2:
    st.subheader("🔄 Em Andamento / Planejado")
    st.write("""
    - 📋 Integração com API REST
    - 📄 Geração de Relatórios PDF
    - 📧 Alertas por Email
    - 🤖 Machine Learning
    - 📱 App Mobile
    - 📊 Dashboard Power BI
    - 🔔 Notificações em Tempo Real
    """)

st.markdown("---")

st.subheader("📊 Estatísticas")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tickets", "280")
with col2:
    st.metric("Componentes", "4")
with col3:
    st.metric("Servidores", "10+")
with col4:
    st.metric("Relatores", "5+")

st.markdown("---")

st.subheader("🚀 Como Usar")

st.write("""
### Opção 1: Página Inicial (Recomendada)
```bash
streamlit run index.py
```
Abre a página inicial com navegação visual.

### Opção 2: Launcher Automático
```bash
python iniciar.py
```
Menu de linha de comando com 5 opções.

### Opção 3: Dashboards Diretos
```bash
# Dashboard com Banco
streamlit run backend/dashboard_db.py

# Dashboard com Upload
streamlit run backend/dashboard.py
```
""")

st.markdown("---")

st.subheader("📁 Estrutura de Arquivos")

st.code("""
projeto-ai-python/
├── index.py                    # Página inicial
├── iniciar.py                  # Launcher automático
├── pages/                      # Páginas do Streamlit
│   ├── 01_dashboard_db.py
│   ├── 02_dashboard_upload.py
│   ├── 03_teste_conexao.py
│   ├── 04_dados_banco.py
│   └── 05_status.py
├── backend/
│   ├── dashboard_db.py         # Dashboard com banco
│   ├── dashboard.py            # Dashboard com upload
│   ├── servico_tickets.py      # Serviço de dados
│   ├── ssh_tunnel.py           # Gerenciador SSH
│   ├── models.py               # Modelos ORM
│   └── ...
└── uploads/                    # CSVs para upload
""")

st.markdown("---")

st.subheader("🔐 Segurança")
st.write("""
- ✅ SSH Tunnel com chave Ed25519
- ✅ PostgreSQL 17 encriptado
- ✅ Sem exposição direta do banco
- ✅ Acesso controlado via VPS
- ⚠️ Chave SSH em .pem (adicionar .gitignore em produção)
""")

st.markdown("---")

st.caption("AGT 4.0 - Sistema de Análise de Tickets | Database Edition v1.0")
