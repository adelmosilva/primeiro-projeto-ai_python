"""
Sistema de versionamento automático baseado em git commits
"""

import subprocess
from datetime import datetime
import os

def get_version():
    """Obtém versão baseada no git commit hash (curto)"""
    try:
        # Tentar obter o hash do commit atual (curto: 7 caracteres)
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Tentar obter a data do commit
        commit_date = subprocess.check_output(
            ['git', 'log', '-1', '--format=%ai'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        # Formatar data (2024-12-25 12:34:56 +0000 -> 2024-12-25)
        version_date = commit_date.split()[0]
        
        return f"v{version_date} ({commit_hash})"
    except:
        # Fallback: usar timestamp local
        return f"v{datetime.now().strftime('%Y-%m-%d')} (local)"

def get_version_short():
    """Obtém apenas o hash do commit (para uso em badges)"""
    try:
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return commit_hash
    except:
        return "dev"

if __name__ == "__main__":
    print(f"Versão atual: {get_version()}")
