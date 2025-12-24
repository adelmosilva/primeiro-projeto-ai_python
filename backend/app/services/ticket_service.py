"""
Serviço de processamento de tickets
"""

import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class TicketService:
    """Serviço responsável pelo processamento de tickets"""
    
    def __init__(self):
        self.tickets = []
    
    def carregar_tickets(self, dados: List[Dict[str, Any]]) -> int:
        """
        Carrega tickets dos dados processados
        
        Args:
            dados: Lista de dicionários com dados de tickets
            
        Returns:
            Quantidade de tickets carregados
        """
        self.tickets = dados
        logger.info(f"Carregados {len(self.tickets)} tickets")
        return len(self.tickets)
    
    def contar_por_status(self) -> Dict[str, int]:
        """Conta tickets por status"""
        contagem = {}
        for ticket in self.tickets:
            status = ticket.get('status', 'Desconhecido')
            contagem[status] = contagem.get(status, 0) + 1
        return contagem
    
    def contar_por_tipologia(self) -> Dict[str, int]:
        """Conta tickets por tipologia (Incident, Support, Task)"""
        contagem = {}
        for ticket in self.tickets:
            tipologia = ticket.get('tipologia', 'Desconhecida')
            contagem[tipologia] = contagem.get(tipologia, 0) + 1
        return contagem
    
    def contar_por_modulo(self) -> Dict[str, int]:
        """Conta tickets por módulo/ambiente"""
        contagem = {}
        for ticket in self.tickets:
            modulo = ticket.get('modulo', 'Desconhecido')
            contagem[modulo] = contagem.get(modulo, 0) + 1
        return contagem
    
    def contar_por_origem(self) -> Dict[str, int]:
        """Conta tickets por origem"""
        contagem = {}
        for ticket in self.tickets:
            origem = ticket.get('origem', 'Desconhecida')
            contagem[origem] = contagem.get(origem, 0) + 1
        return contagem
