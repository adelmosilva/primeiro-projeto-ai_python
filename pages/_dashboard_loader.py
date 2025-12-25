"""
Helper para carregar dashboards via exec() com paths corretos
"""

import sys
from pathlib import Path

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
        
        # Executar o código com a namespace correta
        namespace = {'__name__': '__main__', '__file__': str(dashboard_path)}
        exec(code, namespace)
