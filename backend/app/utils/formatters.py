"""
Formatadores para saídas de dados
"""

from typing import Dict, List, Any


def formatar_percentual(valor: float, casas_decimais: int = 2) -> str:
    """Formata um valor em percentual"""
    return f"{valor:.{casas_decimais}f}%"


def formatar_numero(valor: int) -> str:
    """Formata um número com separador de milhares"""
    return f"{valor:,}".replace(',', '.')


def formatar_tabela(dados: List[Dict[str, Any]], colunas: List[str]) -> str:
    """
    Formata dados em uma tabela de texto
    
    Args:
        dados: Lista de dicionários
        colunas: Colunas a exibir
        
    Returns:
        String formatada como tabela
    """
    # Calcular larguras das colunas
    larguras = {col: len(str(col)) for col in colunas}
    
    for linha in dados:
        for col in colunas:
            larguras[col] = max(larguras[col], len(str(linha.get(col, ''))))
    
    # Construir tabela
    linhas = []
    
    # Header
    header = " | ".join(str(col).ljust(larguras[col]) for col in colunas)
    linhas.append(header)
    linhas.append("-" * len(header))
    
    # Dados
    for linha in dados:
        row = " | ".join(str(linha.get(col, '')).ljust(larguras[col]) for col in colunas)
        linhas.append(row)
    
    return "\n".join(linhas)
