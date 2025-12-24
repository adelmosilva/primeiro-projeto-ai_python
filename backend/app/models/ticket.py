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
    tipologia: str  # Incident, Support, Task
    origem: str  # Middleware, Infraestrutura, Database, AD/BI
    modulo: str  # Database, PSRM, Portal, Batch Server, Jira Server, Clusters
    ambiente: Optional[str]  # Produção, Teste, Desenvolvimento
    status: str  # Aberto, Fechado, Em Progresso
    data_abertura: datetime
    data_fechamento: Optional[datetime]
    assignee: Optional[str]
    prioridade: Optional[str]
    
    @property
    def dias_aberto(self) -> int:
        """Calcula dias em aberto"""
        data_fim = self.data_fechamento or datetime.now()
        return (data_fim - self.data_abertura).days
