"""
Serviço de geração de relatórios
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportService:
    """Serviço responsável pela geração de relatórios"""
    
    @staticmethod
    def gerar_relatorio_texto(
        periodo: str,
        resumo: Dict[str, Any],
        analises_tipologia: Dict[str, Dict[str, int]],
        analises_componente: Dict[str, Dict[str, int]],
        analises_origem: Dict[str, Dict[str, int]],
        analises_prioridade: Dict[str, Dict[str, int]] = None
    ) -> str:
        """
        Gera relatório em formato texto
        
        Args:
            periodo: Período do relatório
            resumo: Resumo executivo
            analises_tipologia: Análise por tipologia
            analises_componente: Análise por componente
            analises_origem: Análise por origem
            analises_prioridade: Análise por prioridade (opcional)
            
        Returns:
            String com o relatório formatado
        """
        linhas = []
        
        # Header
        linhas.append("=" * 90)
        linhas.append("RELATÓRIO DE MIDDLEWARE E INFRAESTRUTURA - AGT 4.0".center(90))
        linhas.append("=" * 90)
        linhas.append(f"Período: {periodo}".center(90))
        linhas.append(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}".center(90))
        linhas.append("=" * 90)
        
        # Resumo Executivo
        linhas.append("\n1. RESUMO EXECUTIVO\n")
        linhas.append(f"  Total de Tickets Abertos:      {resumo['total_abertos']:>4}")
        linhas.append(f"  Total de Tickets Fechados:     {resumo['total_fechados']:>4}")
        linhas.append(f"  Backlog Final:                 {resumo['backlog_final']:>4}")
        linhas.append(f"  Total Geral:                   {resumo['total_geral']:>4}")
        
        # Análise por Tipologia
        linhas.append("\n2. ANÁLISE POR TIPOLOGIA\n")
        linhas.append(f"  {'Tipologia':<15} {'Total':>6} {'Abertos':>8} {'Fechados':>8}")
        linhas.append("  " + "-" * 40)
        for tipologia, dados in sorted(analises_tipologia.items()):
            linhas.append(
                f"  {tipologia:<15} {dados['total']:>6} {dados['abertos']:>8} {dados['fechados']:>8}"
            )
        
        # Análise por Componente
        linhas.append("\n3. ANÁLISE POR COMPONENTE\n")
        linhas.append(f"  {'Componente':<30} {'Total':>6} {'Abertos':>8} {'Fechados':>8}")
        linhas.append("  " + "-" * 60)
        for componente, dados in sorted(analises_componente.items()):
            linhas.append(
                f"  {componente:<30} {dados['total']:>6} {dados['abertos']:>8} {dados['fechados']:>8}"
            )
        
        # Análise por Origem
        linhas.append("\n4. ANÁLISE POR ORIGEM\n")
        linhas.append(f"  {'Origem':<30} {'Total':>6} {'Abertos':>8} {'Fechados':>8}")
        linhas.append("  " + "-" * 60)
        for origem, dados in sorted(analises_origem.items()):
            linhas.append(
                f"  {origem:<30} {dados['total']:>6} {dados['abertos']:>8} {dados['fechados']:>8}"
            )
        
        # Análise por Prioridade
        if analises_prioridade:
            linhas.append("\n5. ANÁLISE POR PRIORIDADE\n")
            linhas.append(f"  {'Prioridade':<30} {'Total':>6} {'Abertos':>8} {'Fechados':>8}")
            linhas.append("  " + "-" * 60)
            for prioridade, dados in sorted(analises_prioridade.items()):
                linhas.append(
                    f"  {prioridade:<30} {dados['total']:>6} {dados['abertos']:>8} {dados['fechados']:>8}"
                )
        
        linhas.append("\n" + "=" * 90)
        
        return "\n".join(linhas)
