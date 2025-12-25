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
    def top_10_servidores_por_total(tickets: List[Ticket]) -> List[tuple]:
        """
        Retorna top 10 servidores com MAIS TICKETS NO TOTAL
        (Útil para ver quais servidores mais geraram tickets)
        
        Args:
            tickets: Lista de Tickets
            
        Returns:
            Lista de tuplas (servidor, count) ordenada decrescente
        """
        servidor_count = {}
        
        for ticket in tickets:
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
    @staticmethod
    def analisar_por_origem(tickets: List[Ticket]) -> Dict[str, Dict[str, int]]:
        """
        Análise detalhada por origem (Database, Middleware, Infra)
        
        Args:
            tickets: Lista de Tickets
            
        Returns:
            Dicionário com análises por origem
        """
        resultado = {}
        
        # Mapear componentes para origens
        origem_map = {
            'Database': 'Database',
            'Middleware': 'Middleware',
            'Infraestruturas': 'Infra'
        }
        
        origens = set()
        for t in tickets:
            componente = t.componente or "Não especificado"
            origem = origem_map.get(componente, componente)
            origens.add(origem)
        
        for origem in origens:
            tickets_origem = [t for t in tickets 
                            if origem_map.get(t.componente or "Não especificado", t.componente or "Não especificado") == origem]
            resultado[origem] = {
                'total': len(tickets_origem),
                'abertos': sum(1 for t in tickets_origem if t.esta_aberto),
                'fechados': sum(1 for t in tickets_origem if not t.esta_aberto)
            }
        
        return resultado
    
    @staticmethod
    def tabela_tipologia(tickets_periodo1: List[Ticket], tickets_periodo2: List[Ticket]) -> List[Dict[str, Any]]:
        """
        Gera tabela de tipologia com comparativo mês anterior vs atual
        
        Args:
            tickets_periodo1: Tickets do período anterior
            tickets_periodo2: Tickets do período atual
            
        Returns:
            Lista de dicts com dados de tipologia
        """
        resultado = []
        tipologias_set = set()
        
        # Coletar todas as tipologias
        for t in tickets_periodo1 + tickets_periodo2:
            if t.tipologia:
                tipologias_set.add(t.tipologia)
        
        for tipologia in sorted(tipologias_set):
            # Período 1 (anterior)
            tickets_t1 = [t for t in tickets_periodo1 if t.tipologia == tipologia]
            abertos_p1 = sum(1 for t in tickets_t1 if t.esta_aberto)
            fechados_p1 = sum(1 for t in tickets_t1 if not t.esta_aberto)
            
            # Período 2 (atual)
            tickets_t2 = [t for t in tickets_periodo2 if t.tipologia == tipologia]
            abertos_p2 = sum(1 for t in tickets_t2 if t.esta_aberto)
            fechados_p2 = sum(1 for t in tickets_t2 if not t.esta_aberto)
            
            resultado.append({
                'tipologia': tipologia,
                'abertos_anterior': abertos_p1,
                'abertos_atual': abertos_p2,
                'fechados_anterior': fechados_p1,
                'fechados_atual': fechados_p2,
                'total_anterior': len(tickets_t1),
                'total_atual': len(tickets_t2)
            })
        
        return resultado
    
    @staticmethod
    def tabela_top10_modulos(tickets_periodo1: List[Ticket], tickets_periodo2: List[Ticket]) -> List[Dict[str, Any]]:
        """
        Gera tabela dos 10 módulos (servidores) com mais tickets
        
        Args:
            tickets_periodo1: Tickets do período anterior
            tickets_periodo2: Tickets do período atual
            
        Returns:
            Lista de dicts com top 10 módulos
        """
        resultado = []
        
        # Top 10 do período anterior
        top10_p1 = AnalysisService.top_10_servidores_por_total(tickets_periodo1)
        top10_p1_dict = dict(top10_p1)
        
        # Top 10 do período atual
        top10_p2 = AnalysisService.top_10_servidores_por_total(tickets_periodo2)
        top10_p2_dict = dict(top10_p2)
        
        # Coletar todos os servidores de ambos períodos
        todos_servidores = set(list(top10_p1_dict.keys()) + list(top10_p2_dict.keys()))
        
        # Análise detalhada por servidor para cada período
        for servidor in sorted(todos_servidores)[:10]:
            # Período anterior
            tickets_srv_p1 = [t for t in tickets_periodo1 if (t.servidor or "Não especificado") == servidor]
            abertos_p1 = sum(1 for t in tickets_srv_p1 if t.esta_aberto)
            fechados_p1 = sum(1 for t in tickets_srv_p1 if not t.esta_aberto)
            
            # Período atual
            tickets_srv_p2 = [t for t in tickets_periodo2 if (t.servidor or "Não especificado") == servidor]
            abertos_p2 = sum(1 for t in tickets_srv_p2 if t.esta_aberto)
            fechados_p2 = sum(1 for t in tickets_srv_p2 if not t.esta_aberto)
            
            resultado.append({
                'modulo': servidor,
                'abertos_anterior': abertos_p1,
                'abertos_atual': abertos_p2,
                'fechados_anterior': fechados_p1,
                'fechados_atual': fechados_p2
            })
        
        return resultado
    
    @staticmethod
    def tabela_origem(tickets_periodo1: List[Ticket], tickets_periodo2: List[Ticket]) -> List[Dict[str, Any]]:
        """
        Gera tabela de origem com comparativo mês anterior vs atual
        
        Args:
            tickets_periodo1: Tickets do período anterior
            tickets_periodo2: Tickets do período atual
            
        Returns:
            Lista de dicts com dados de origem
        """
        resultado = []
        
        # Mapear componentes para origens
        origem_map = {
            'Database': 'Database',
            'Middleware': 'Middleware',
            'Infraestruturas': 'Infra'
        }
        
        # Coletar todas as origens
        origens_set = set()
        for t in tickets_periodo1 + tickets_periodo2:
            componente = t.componente or "Não especificado"
            origem = origem_map.get(componente, componente)
            origens_set.add(origem)
        
        for origem in sorted(origens_set):
            # Período 1
            tickets_o1 = [t for t in tickets_periodo1 
                         if origem_map.get(t.componente or "Não especificado", t.componente or "Não especificado") == origem]
            abertos_p1 = sum(1 for t in tickets_o1 if t.esta_aberto)
            fechados_p1 = sum(1 for t in tickets_o1 if not t.esta_aberto)
            total_p1 = len(tickets_o1)
            
            # Período 2
            tickets_o2 = [t for t in tickets_periodo2 
                         if origem_map.get(t.componente or "Não especificado", t.componente or "Não especificado") == origem]
            abertos_p2 = sum(1 for t in tickets_o2 if t.esta_aberto)
            fechados_p2 = sum(1 for t in tickets_o2 if not t.esta_aberto)
            total_p2 = len(tickets_o2)
            
            # Calcular percentuais
            pct_p1 = (total_p1 / len(tickets_periodo1) * 100) if tickets_periodo1 else 0
            pct_p2 = (total_p2 / len(tickets_periodo2) * 100) if tickets_periodo2 else 0
            
            resultado.append({
                'origem': origem,
                'abertos_anterior': abertos_p1,
                'abertos_atual': abertos_p2,
                'fechados_anterior': fechados_p1,
                'fechados_atual': fechados_p2,
                'total_anterior': total_p1,
                'total_atual': total_p2,
                'percentual_anterior': round(pct_p1, 1),
                'percentual_atual': round(pct_p2, 1)
            })
        
        return resultado