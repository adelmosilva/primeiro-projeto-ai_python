"""
Serviço de análise de tickets
"""

import logging
from typing import List, Dict, Any
from ..models.ticket import Ticket

logger = logging.getLogger(__name__)


class AnalysisService:
    """Serviço responsável por análises e cálculos de métricas"""
    
    @staticmethod
    def calcular_resumo_executivo(tickets: List[Ticket]) -> Dict[str, Any]:
        """
        Calcula resumo executivo
        
        Args:
            tickets: Lista de Tickets
            
        Returns:
            Dicionário com métricas do resumo
        """
        abertos = sum(1 for t in tickets if t.esta_aberto)
        fechados = sum(1 for t in tickets if not t.esta_aberto)
        
        return {
            'total_abertos': abertos,
            'total_fechados': fechados,
            'total_geral': len(tickets),
            'backlog_final': abertos
        }
    
    @staticmethod
    def analisar_por_tipologia(tickets: List[Ticket]) -> Dict[str, Dict[str, int]]:
        """
        Análise detalhada por tipologia
        
        Args:
            tickets: Lista de Tickets
            
        Returns:
            Dicionário com análises por tipologia
        """
        resultado = {}
        tipologias = set(t.tipologia for t in tickets)
        
        for tipologia in tipologias:
            tickets_tipo = [t for t in tickets if t.tipologia == tipologia]
            resultado[tipologia] = {
                'total': len(tickets_tipo),
                'abertos': sum(1 for t in tickets_tipo if t.esta_aberto),
                'fechados': sum(1 for t in tickets_tipo if not t.esta_aberto)
            }
        
        return resultado
    
    @staticmethod
    def analisar_por_componente(tickets: List[Ticket]) -> Dict[str, Dict[str, int]]:
        """Análise detalhada por componente"""
        resultado = {}
        componentes = set(t.componente for t in tickets)
        
        for componente in componentes:
            tickets_componente = [t for t in tickets if t.componente == componente]
            resultado[componente] = {
                'total': len(tickets_componente),
                'abertos': sum(1 for t in tickets_componente if t.esta_aberto),
                'fechados': sum(1 for t in tickets_componente if not t.esta_aberto)
            }
        
        return resultado
    
    @staticmethod
    def analisar_por_origem(tickets: List[Ticket]) -> Dict[str, Dict[str, int]]:
        """Análise detalhada por origem"""
        resultado = {}
        origens = set(t.origem for t in tickets)
        
        for origem in origens:
            tickets_origem = [t for t in tickets if t.origem == origem]
            resultado[origem] = {
                'total': len(tickets_origem),
                'abertos': sum(1 for t in tickets_origem if t.esta_aberto),
                'fechados': sum(1 for t in tickets_origem if not t.esta_aberto)
            }
        
        return resultado
    
    @staticmethod
    def analisar_por_prioridade(tickets: List[Ticket]) -> Dict[str, Dict[str, int]]:
        """Análise detalhada por prioridade"""
        resultado = {}
        prioridades = set(t.prioridade or "Não especificada" for t in tickets)
        
        for prioridade in prioridades:
            tickets_prioridade = [t for t in tickets if (t.prioridade or "Não especificada") == prioridade]
            resultado[prioridade] = {
                'total': len(tickets_prioridade),
                'abertos': sum(1 for t in tickets_prioridade if t.esta_aberto),
                'fechados': sum(1 for t in tickets_prioridade if not t.esta_aberto)
            }
        
        return resultado
    
    @staticmethod
    def analisar_por_responsavel(tickets: List[Ticket]) -> Dict[str, Dict[str, int]]:
        """Análise detalhada por responsável"""
        resultado = {}
        responsaveis = set(t.responsavel or "Não atribuído" for t in tickets)
        
        for responsavel in responsaveis:
            tickets_resp = [t for t in tickets if (t.responsavel or "Não atribuído") == responsavel]
            resultado[responsavel] = {
                'total': len(tickets_resp),
                'abertos': sum(1 for t in tickets_resp if t.esta_aberto),
                'fechados': sum(1 for t in tickets_resp if not t.esta_aberto)
            }
        
        return resultado
    
    @staticmethod
    def analisar_por_servidor(tickets: List[Ticket]) -> Dict[str, Dict[str, int]]:
        """Análise detalhada por servidor/cluster"""
        resultado = {}
        servidores = set(t.servidor or "Não especificado" for t in tickets)
        
        for servidor in servidores:
            tickets_servidor = [t for t in tickets if (t.servidor or "Não especificado") == servidor]
            resultado[servidor] = {
                'total': len(tickets_servidor),
                'abertos': sum(1 for t in tickets_servidor if t.esta_aberto),
                'fechados': sum(1 for t in tickets_servidor if not t.esta_aberto)
            }
        
        return resultado
    
    @staticmethod
    def top_10_servidores_abertos(tickets: List[Ticket]) -> List[tuple]:
        """
        Retorna top 10 servidores com mais tickets ABERTOS
        
        Args:
            tickets: Lista de Tickets
            
        Returns:
            Lista de tuplas (servidor, count) ordenada decrescente
        """
        abertos = [t for t in tickets if t.esta_aberto]
        servidor_count = {}
        
        for ticket in abertos:
            serv = ticket.servidor or "Não especificado"
            servidor_count[serv] = servidor_count.get(serv, 0) + 1
        
        # Ordenar e retornar top 10
        top_10 = sorted(servidor_count.items(), key=lambda x: x[1], reverse=True)[:10]
        return top_10
    
    @staticmethod
    def calcular_resumo_acumulado(tickets_periodo1: List[Ticket], tickets_periodo2: List[Ticket]) -> Dict[str, Any]:
        """
        Calcula resumo acumulado entre dois períodos
        
        Args:
            tickets_periodo1: Tickets do período anterior
            tickets_periodo2: Tickets do período atual
            
        Returns:
            Dicionário com métricas acumuladas
        """
        # Combinar tickets de ambos períodos
        todos_tickets = tickets_periodo1 + tickets_periodo2
        
        abertos = sum(1 for t in todos_tickets if t.esta_aberto)
        fechados = sum(1 for t in todos_tickets if not t.esta_aberto)
        
        return {
            'total_abertos': abertos,
            'total_fechados': fechados,
            'total_geral': len(todos_tickets)
        }
