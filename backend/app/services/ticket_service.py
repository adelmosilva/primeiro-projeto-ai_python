"""
Serviço de processamento de tickets
"""

import logging
from typing import List, Dict, Any
from datetime import datetime
from ..models.ticket import Ticket

logger = logging.getLogger(__name__)


class TicketService:
    """Serviço responsável pelo processamento de tickets"""
    
    def __init__(self):
        self.tickets: List[Ticket] = []
    
    def carregar_tickets(self, tickets: List[Ticket]) -> int:
        """
        Carrega tickets
        
        Args:
            tickets: Lista de objetos Ticket
            
        Returns:
            Quantidade de tickets carregados
        """
        self.tickets = tickets
        logger.info(f"Carregados {len(self.tickets)} tickets")
        return len(self.tickets)
    
    def contar_por_status(self) -> Dict[str, int]:
        """Conta tickets por status"""
        contagem = {}
        for ticket in self.tickets:
            status = ticket.status
            contagem[status] = contagem.get(status, 0) + 1
        return contagem
    
    def contar_por_tipologia(self) -> Dict[str, int]:
        """Conta tickets por tipologia (Support, Task, Incident, Bug)"""
        contagem = {}
        for ticket in self.tickets:
            tipologia = ticket.tipologia
            contagem[tipologia] = contagem.get(tipologia, 0) + 1
        return contagem
    
    def contar_por_componente(self) -> Dict[str, int]:
        """Conta tickets por componente/módulo"""
        contagem = {}
        for ticket in self.tickets:
            componente = ticket.componente
            contagem[componente] = contagem.get(componente, 0) + 1
        return contagem
    
    def contar_por_origem(self) -> Dict[str, int]:
        """Conta tickets por origem"""
        contagem = {}
        for ticket in self.tickets:
            origem = ticket.origem
            contagem[origem] = contagem.get(origem, 0) + 1
        return contagem
    
    def contar_por_prioridade(self) -> Dict[str, int]:
        """Conta tickets por prioridade"""
        contagem = {}
        for ticket in self.tickets:
            prioridade = ticket.prioridade or "Não especificada"
            contagem[prioridade] = contagem.get(prioridade, 0) + 1
        return contagem
    
    def obter_tickets_abertos(self) -> List[Ticket]:
        """Retorna apenas tickets abertos"""
        return [t for t in self.tickets if t.esta_aberto]
    
    def obter_tickets_fechados(self) -> List[Ticket]:
        """Retorna apenas tickets fechados"""
        return [t for t in self.tickets if not t.esta_aberto]
    
    def contar_tickets(self) -> Dict[str, int]:
        """Retorna contagem geral de tickets"""
        total = len(self.tickets)
        abertos = len(self.obter_tickets_abertos())
        fechados = len(self.obter_tickets_fechados())
        
        return {
            'total': total,
            'abertos': abertos,
            'fechados': fechados
        }
