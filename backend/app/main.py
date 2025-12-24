"""
Ponto de entrada da aplicação
"""

import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Função principal"""
    logger.info("Iniciando AGT 4.0 - Relatório de Middleware e Infraestrutura")
    # TODO: Implementar lógica principal


if __name__ == "__main__":
    main()
