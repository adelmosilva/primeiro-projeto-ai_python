#!/usr/bin/env python3
"""Script para inicializar estrutura de diretórios do projeto."""

import sys
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.config import UPLOADS_DIR, RELATORIOS_DIR, DATA_DIR, INPUT_DIR, PROCESSED_DIR, HISTORICAL_DIR

def criar_diretorios():
    """Cria todos os diretórios necessários."""
    
    diretorios = [
        (UPLOADS_DIR, "CSVs enviados"),
        (RELATORIOS_DIR, "Relatórios PDF"),
        (DATA_DIR, "Dados processados"),
        (INPUT_DIR, "Dados de entrada"),
        (PROCESSED_DIR, "Dados processados"),
        (HISTORICAL_DIR, "Dados históricos"),
    ]
    
    print("\n" + "="*60)
    print("INICIALIZANDO ESTRUTURA DE DIRETÓRIOS")
    print("="*60)
    
    for caminho, descricao in diretorios:
        try:
            caminho.mkdir(parents=True, exist_ok=True)
            print(f"✅ {descricao:.<40} {caminho}")
        except Exception as e:
            print(f"❌ {descricao:.<40} ERRO: {e}")
    
    print("\n" + "="*60)
    print("✅ ESTRUTURA PRONTA!")
    print("="*60)

if __name__ == "__main__":
    criar_diretorios()
