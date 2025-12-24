"""
Validação de dados de tickets
"""

import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)


def validar_tickets(dados: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Valida dados de tickets
    
    Args:
        dados: Lista de dicionários com dados de tickets
        
    Returns:
        Tupla (dados_validos, erros)
    """
    dados_validos = []
    erros = []
    
    campos_obrigatorios = [
        'ticket_id', 'titulo', 'descricao', 'tipologia', 
        'origem', 'modulo', 'status', 'data_abertura'
    ]
    
    for idx, linha in enumerate(dados):
        erros_linha = []
        
        # Verificar campos obrigatórios
        for campo in campos_obrigatorios:
            if campo not in linha or not str(linha.get(campo, ')).strip():
                erros_linha.append(f"Campo obrigatório ausente: {campo}")
        
        if erros_linha:
            erros.append({
                'linha': idx + 2,  # +2 porque header é linha 1
                'ticket_id': linha.get('ticket_id', 'N/A'),
                'erros': erros_linha
            })
        else:
            dados_validos.append(linha)
    
    if erros:
        logger.warning(f"Encontrados {len(erros)} registros com erros durante validação")
    
    return dados_validos, erros
