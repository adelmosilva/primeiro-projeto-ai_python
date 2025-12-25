"""
Serviço unificado que detecta o ambiente e usa Supabase ou SSH
"""

import os
import sys
from pathlib import Path

# ⚠️ FORÇA APENAS IPv4 GLOBALMENTE
os.environ['PSYCOPG2_DISABLE_IPV6'] = '1'

# Detectar se está no Streamlit Cloud
IS_CLOUD = 'STREAMLIT' in os.environ or 'streamlit.io' in os.getenv('HOSTNAME', '')

def obter_servico():
    """
    Retorna o serviço apropriado baseado no ambiente
    - Streamlit Cloud: Supabase
    - Local: SSH Tunnel
    """
    if IS_CLOUD:
        # Cloud: usar Supabase
        try:
            from backend.supabase_service import obter_servico_supabase
            return obter_servico_supabase()
        except ImportError:
            raise ImportError("Supabase não está configurado. Verifique SUPABASE_SETUP.md")
    else:
        # Local: usar SSH (original)
        try:
            from backend.servico_tickets import obter_servico as obter_servico_ssh
            return obter_servico_ssh()
        except ImportError:
            raise ImportError("Serviço SSH não está disponível")

def esta_em_cloud():
    """Verifica se está rodando em Streamlit Cloud"""
    return IS_CLOUD

def info_conexao():
    """Retorna informações sobre qual serviço está sendo usado"""
    return {
        'ambiente': 'Streamlit Cloud' if IS_CLOUD else 'Local',
        'servico': 'Supabase' if IS_CLOUD else 'SSH Tunnel',
        'banco': 'PostgreSQL (Supabase)' if IS_CLOUD else 'PostgreSQL (VPS Privado)',
    }
