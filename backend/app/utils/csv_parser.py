"""
Parser para leitura e processamento de arquivos CSV
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def ler_csv(caminho: Path) -> List[Dict[str, Any]]:
    """
    Lê um arquivo CSV e retorna uma lista de dicionários
    
    Args:
        caminho: Caminho do arquivo CSV
        
    Returns:
        Lista de dicionários com os dados
    """
    try:
        dados = []
        with open(caminho, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            dados = list(reader)
        
        logger.info(f"CSV lido com sucesso: {caminho} ({len(dados)} linhas)")
        return dados
    
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {caminho}")
        raise
    except Exception as e:
        logger.error(f"Erro ao ler CSV: {e}")
        raise


def escrever_csv(caminho: Path, dados: List[Dict[str, Any]], colunas: List[str]) -> None:
    """
    Escreve dados em um arquivo CSV
    
    Args:
        caminho: Caminho de destino
        dados: Lista de dicionários
        colunas: Lista de colunas a escrever
    """
    try:
        with open(caminho, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            writer.writeheader()
            writer.writerows(dados)
        
        logger.info(f"CSV escrito com sucesso: {caminho}")
    except Exception as e:
        logger.error(f"Erro ao escrever CSV: {e}")
        raise
