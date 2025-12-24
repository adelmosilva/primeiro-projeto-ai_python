"""
Configurações da aplicação
"""

import os
from pathlib import Path

# Diretórios principais
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "processed"
HISTORICAL_DIR = DATA_DIR / "historical"
REPORTS_OUTPUT_DIR = BASE_DIR / "app" / "reports" / "output"

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configurações de processamento
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

# Períodos para análise
CURRENT_PERIOD = "Outubro de 2025"
PREVIOUS_PERIOD = "Setembro de 2025"
