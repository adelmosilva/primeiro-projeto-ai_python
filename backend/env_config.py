"""
Configuração de ambiente para determinar como conectar ao banco de dados
"""

import os
import sys
from pathlib import Path

# Detectar se está rodando no Streamlit Cloud
IS_STREAMLIT_CLOUD = 'STREAMLIT' in os.environ or 'streamlit' in sys.modules

# Configurações do banco de dados
DB_CONFIG = {
    'host': '91.108.124.150',
    'port': 5432,
    'database': 'pythonai_db',
    'user': 'adelmosilva',
    'password': 'Dx220304@',
}

# Configurações SSH (apenas para local)
SSH_CONFIG = {
    'host': '91.108.124.150',
    'port': 22,
    'user': 'root',
    'key_path': Path(__file__).parent / 'vps_key.pem',
}

def get_environment_info() -> dict:
    """Retorna informações do ambiente atual"""
    return {
        'is_streamlit_cloud': IS_STREAMLIT_CLOUD,
        'is_local': not IS_STREAMLIT_CLOUD,
        'platform': sys.platform,
    }
