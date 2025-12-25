"""
Gerenciador de temas (Claro e Escuro) para Streamlit
"""

import streamlit as st

# CSS customizado para modo claro
LIGHT_THEME_CSS = """
<style>
:root {
    --primary-color: #0068C9;
    --background-color: #FFFFFF;
    --secondary-background-color: #F0F2F6;
    --text-color: #31333F;
    --text-secondary-color: #6C7680;
    --border-color: #D3D8DF;
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
}

.stMetric {
    background-color: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 15px;
}

.stDataFrame {
    background-color: var(--secondary-background-color);
}

.stTabs [data-baseweb="tab-list"] {
    background-color: var(--secondary-background-color);
}
</style>
"""

# CSS customizado para modo escuro
DARK_THEME_CSS = """
<style>
:root {
    --primary-color: #0084FF;
    --background-color: #0E1117;
    --secondary-background-color: #161B22;
    --text-color: #E6EDF3;
    --text-secondary-color: #8B949E;
    --border-color: #30363D;
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
}

.stMetric {
    background-color: var(--secondary-background-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 15px;
}

.stDataFrame {
    background-color: var(--secondary-background-color);
}

.stTabs [data-baseweb="tab-list"] {
    background-color: var(--secondary-background-color);
}

/* Customizar inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stNumberInput > div > div > input {
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    border-color: var(--border-color);
}

/* Customizar botões */
.stButton > button {
    background-color: var(--primary-color);
    color: white;
}

/* Customizar sidebar */
.css-1d391kg {
    background-color: var(--secondary-background-color);
}
</style>
"""

def inicializar_tema():
    """Inicializa o gerenciador de tema"""
    if 'tema' not in st.session_state:
        st.session_state.tema = 'claro'

def obter_tema():
    """Retorna o tema atual"""
    return st.session_state.get('tema', 'claro')

def mudar_tema(novo_tema):
    """Muda o tema (claro ou escuro)"""
    st.session_state.tema = novo_tema

def seletor_tema_sidebar():
    """
    Adiciona seletor de tema no sidebar
    Retorna: 'claro' ou 'escuro'
    """
    inicializar_tema()
    
    with st.sidebar:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("☀️ Claro", use_container_width=True):
                mudar_tema('claro')
                st.rerun()
        
        with col2:
            if st.button("🌙 Escuro", use_container_width=True):
                mudar_tema('escuro')
                st.rerun()
        
        tema_atual = obter_tema()
        st.markdown(f"**Tema**: {tema_atual.capitalize()}")
    
    return obter_tema()

def aplicar_tema():
    """Aplica o CSS do tema selecionado"""
    tema = obter_tema()
    
    if tema == 'escuro':
        st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    else:
        st.markdown(LIGHT_THEME_CSS, unsafe_allow_html=True)

def configurar_tema_completo():
    """
    Configuração completa de tema com seletor no sidebar
    Deve ser chamado no início de cada página
    """
    inicializar_tema()
    aplicar_tema()
    return seletor_tema_sidebar()
