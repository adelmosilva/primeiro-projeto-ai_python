"""
Modelo de Ticket
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Ticket:
    """Representa um ticket de atendimento"""
    
    ticket_id: str
    titulo: str
    descricao: str
    tipologia: str  # Support, Tarefa, Incident
    origem: str  # Middleware, Infraestruturas, Database, AD/BI
    componente: str  # Database, PSRM, Portal, Batch Server, Jira Server, Clusters
    servidor: Optional[str]  # Servidor/Cluster específico
    status: str  # Fechada, Aberta, Em Progresso, Cancelado
    data_abertura: datetime
    data_fechamento: Optional[datetime]
    responsavel: Optional[str]
    relator: Optional[str]
    prioridade: Optional[str]  # Low, Medium, High, Critical
    
    @property
    def dias_aberto(self) -> int:
        """Calcula dias em aberto"""
        data_fim = self.data_fechamento or datetime.now()
        return (data_fim - self.data_abertura).days
    
    @property
    def esta_aberto(self) -> bool:
        """Verifica se o ticket está aberto"""
        return self.status.lower() not in ['fechada', 'cancelado']
