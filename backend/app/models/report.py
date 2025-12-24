"""
Modelo de Relatório
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any


@dataclass
class ResumoExecutivo:
    """Resumo executivo do relatório"""
    total_tickets_abertos: int
    total_tickets_fechados: int
    backlog_final: int
    data_geracao: datetime = field(default_factory=datetime.now)


@dataclass
class AnalisePorTipologia:
    """Análise de tickets por tipologia"""
    tipologia: str
    total: int
    abertos: int
    fechados: int
    percentual: float


@dataclass
class RelatorioAGT40:
    """Relatório completo AGT 4.0"""
    periodo: str
    data_geracao: datetime = field(default_factory=datetime.now)
    resumo_executivo: ResumoExecutivo = field(default_factory=ResumoExecutivo)
    analises_tipologia: List[AnalisePorTipologia] = field(default_factory=list)
    analises_modulo: Dict[str, Any] = field(default_factory=dict)
    analises_origem: Dict[str, Any] = field(default_factory=dict)
    indicadores: Dict[str, Any] = field(default_factory=dict)
