"""
Helper para carregar dashboards via exec() com paths corretos
"""

import sys
from pathlib import Path
import streamlit as st

def load_dashboard(dashboard_file):
    """
    Carrega um arquivo de dashboard com sys.path configurado corretamente
    
    Args:
        dashboard_file: Nome do arquivo (ex: 'dashboard.py' ou 'dashboard_db.py')
    """
    # Obter diretórios
    PROJETO_DIR = Path(__file__).parent.parent
    BACKEND_DIR = PROJETO_DIR / "backend"
    
    # Adicionar ao sys.path (ANTES de fazer exec)
    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))
    if str(PROJETO_DIR) not in sys.path:
        sys.path.insert(0, str(PROJETO_DIR))
    
    # Ler e executar o arquivo
    dashboard_path = BACKEND_DIR / dashboard_file
    with open(dashboard_path, "r", encoding="utf-8") as f:
        code = f.read()
        
        # Preparar namespace com os paths corretos
        namespace = {
            '__name__': '__main__',
            '__file__': str(dashboard_path),
            '__builtins__': __builtins__,
            'PROJETO_DIR': PROJETO_DIR,
            'BACKEND_DIR': BACKEND_DIR
        }
        
        # Executar o código
        try:
            exec(code, namespace)
        except ModuleNotFoundError as e:
            st.error(f"❌ Erro ao carregar dashboard: {e}")
            st.info(f"Paths configurados:\n- Projeto: {PROJETO_DIR}\n- Backend: {BACKEND_DIR}")
            import traceback
            st.code(traceback.format_exc())
