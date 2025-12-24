"""
Serviço de análise de tickets
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class AnalysisService:
    """Serviço responsável por análises e cálculos de métricas"""
    
    @staticmethod
    def calcular_resumo_executivo(tickets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula resumo executivo
        
        Args:
            tickets: Lista de tickets
            
        Returns:
            Dicionário com métricas do resumo
        """
        abertos = sum(1 for t in tickets if t.get('status') == 'Aberto')
        fechados = sum(1 for t in tickets if t.get('status') == 'Fechado')
        
        return {
            'total_abertos': abertos,
            'total_fechados': fechados,
            'total_geral': len(tickets),
            'backlog_final': abertos
        }
    
    @staticmethod
    def analisar_por_tipologia(tickets: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """
        Análise detalhada por tipologia
        
        Args:
            tickets: Lista de tickets
            
        Returns:
            Dicionário com análises por tipologia
        """
        resultado = {}
        tipologias = set(t.get('tipologia') for t in tickets)
        
        for tipologia in tipologias:
            tickets_tipo = [t for t in tickets if t.get('tipologia') == tipologia]
            resultado[tipologia] = {
                'total': len(tickets_tipo),
                'abertos': sum(1 for t in tickets_tipo if t.get('status') == 'Aberto'),
                'fechados': sum(1 for t in tickets_tipo if t.get('status') == 'Fechado')
            }
        
        return resultado
    
    @staticmethod
    def analisar_por_modulo(tickets: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """Análise detalhada por módulo"""
        resultado = {}
        modulos = set(t.get('modulo') for t in tickets)
        
        for modulo in modulos:
            tickets_modulo = [t for t in tickets if t.get('modulo') == modulo]
            resultado[modulo] = {
                'total': len(tickets_modulo),
                'abertos': sum(1 for t in tickets_modulo if t.get('status') == 'Aberto'),
                'fechados': sum(1 for t in tickets_modulo if t.get('status') == 'Fechado')
            }
        
        return resultado
    
    @staticmethod
    def analisar_por_origem(tickets: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
        """Análise detalhada por origem"""
        resultado = {}
        origens = set(t.get('origem') for t in tickets)
        
        for origem in origens:
            tickets_origem = [t for t in tickets if t.get('origem') == origem]
            resultado[origem] = {
                'total': len(tickets_origem),
                'abertos': sum(1 for t in tickets_origem if t.get('status') == 'Aberto'),
                'fechados': sum(1 for t in tickets_origem if t.get('status') == 'Fechado')
            }
        
        return resultado
