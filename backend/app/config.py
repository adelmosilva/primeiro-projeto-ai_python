"""
Configurações da aplicação
"""

import os
from pathlib import Path

# Diretórios principais
BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
PROJECT_ROOT = BASE_DIR.parent  # Raiz do projeto

# Diretórios de dados
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "processed"
HISTORICAL_DIR = DATA_DIR / "historical"

# Diretórios de uploads e relatórios (na raiz do projeto)
UPLOADS_DIR = PROJECT_ROOT / "uploads"
RELATORIOS_DIR = PROJECT_ROOT / "relatorios"

# Diretório de outputs de relatórios PDF
REPORTS_OUTPUT_DIR = RELATORIOS_DIR

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configurações de processamento
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

# Períodos para análise
CURRENT_PERIOD = "Outubro de 2025"
PREVIOUS_PERIOD = "Setembro de 2025"
