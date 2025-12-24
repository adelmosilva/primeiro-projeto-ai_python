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
        analises_modulo: Dict[str, Dict[str, int]],
        analises_origem: Dict[str, Dict[str, int]]
    ) -> str:
        """
        Gera relatório em formato texto
        
        Args:
            periodo: Período do relatório
            resumo: Resumo executivo
            analises_tipologia: Análise por tipologia
            analises_modulo: Análise por módulo
            analises_origem: Análise por origem
            
        Returns:
            String com o relatório formatado
        """
        linhas = []
        
        # Header
        linhas.append("=" * 80)
        linhas.append("RELATÓRIO DE MIDDLEWARE E INFRAESTRUTURA - AGT 4.0".center(80))
        linhas.append("=" * 80)
        linhas.append(f"Período: {periodo}".center(80))
        linhas.append(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}".center(80))
        linhas.append("=" * 80)
        
        # Resumo Executivo
        linhas.append("\n1. RESUMO EXECUTIVO\n")
        linhas.append(f"  Total de Tickets Abertos:      {resumo['total_abertos']}")
        linhas.append(f"  Total de Tickets Fechados:     {resumo['total_fechados']}")
        linhas.append(f"  Backlog Final:                 {resumo['backlog_final']}")
        linhas.append(f"  Total Geral:                   {resumo['total_geral']}")
        
        # Análise por Tipologia
        linhas.append("\n2. ANÁLISE POR TIPOLOGIA\n")
        for tipologia, dados in analises_tipologia.items():
            linhas.append(f"  {tipologia}:")
            linhas.append(f"    Total: {dados['total']} | Abertos: {dados['abertos']} | Fechados: {dados['fechados']}")
        
        # Análise por Módulo
        linhas.append("\n3. ANÁLISE POR MÓDULO\n")
        for modulo, dados in analises_modulo.items():
            linhas.append(f"  {modulo}:")
            linhas.append(f"    Total: {dados['total']} | Abertos: {dados['abertos']} | Fechados: {dados['fechados']}")
        
        # Análise por Origem
        linhas.append("\n4. ANÁLISE POR ORIGEM\n")
        for origem, dados in analises_origem.items():
            linhas.append(f"  {origem}:")
            linhas.append(f"    Total: {dados['total']} | Abertos: {dados['abertos']} | Fechados: {dados['fechados']}")
        
        linhas.append("\n" + "=" * 80)
        
        return "\n".join(linhas)
