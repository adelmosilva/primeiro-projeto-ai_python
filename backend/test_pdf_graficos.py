"""
Script de teste - PDF com gráficos
"""

import logging
from pathlib import Path
import sys

# Adicionar pasta ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.jira_parser import parser_jira_csv
from app.services.ticket_service import TicketService
from app.services.analysis_service import AnalysisService
from app.services.pdf_report_service import PDFReportService
from app.config import INPUT_DIR, REPORTS_OUTPUT_DIR

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Função principal"""
    
    logger.info("=" * 90)
    logger.info("TESTE 3: GERAÇÃO DE PDF COM GRÁFICOS")
    logger.info("=" * 90)
    
    try:
        # Carregar e processar
        logger.info("\n[1/3] Processando arquivo...")
        csv_path = INPUT_DIR / "JIRAS_NOV2025_formatado.csv"
        
        tickets = parser_jira_csv(csv_path)
        service = TicketService()
        service.carregar_tickets(tickets)
        
        resumo = AnalysisService.calcular_resumo_executivo(tickets)
        analises_tipologia = AnalysisService.analisar_por_tipologia(tickets)
        analises_componente = AnalysisService.analisar_por_componente(tickets)
        analises_origem = AnalysisService.analisar_por_origem(tickets)
        analises_prioridade = AnalysisService.analisar_por_prioridade(tickets)
        analises_servidor = AnalysisService.analisar_por_servidor(tickets)
        
        logger.info(f"✓ {len(tickets)} tickets processados\n")
        
        # Gerar PDF com gráficos
        logger.info("[2/3] Gerando PDF com gráficos...")
        REPORTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        pdf_path = REPORTS_OUTPUT_DIR / "relatorio_AGT40_Novembro_Com_Graficos.pdf"
        
        pdf_service = PDFReportService(pdf_path)
        pdf_service.gerar_relatorio(
            periodo="Novembro de 2025",
            resumo=resumo,
            analises_tipologia=analises_tipologia,
            analises_componente=analises_componente,
            analises_origem=analises_origem,
            analises_prioridade=analises_prioridade,
            analises_servidor=analises_servidor
        )
        
        logger.info(f"✓ PDF gerado: {pdf_path.name}\n")
        
        # Resumo
        logger.info("[3/3] Resumo da análise:")
        logger.info("=" * 90)
        logger.info(f"Total de Tickets: {resumo['total_geral']}")
        logger.info(f"Abertos: {resumo['total_abertos']}")
        logger.info(f"Fechados: {resumo['total_fechados']}")
        logger.info(f"Backlog: {resumo['backlog_final']}")
        logger.info("\nAnálises:")
        logger.info(f"  Tipologias: {len(analises_tipologia)}")
        logger.info(f"  Componentes: {len(analises_componente)}")
        logger.info(f"  Origens: {len(analises_origem)}")
        logger.info(f"  Prioridades: {len(analises_prioridade)}")
        logger.info(f"  Servidores: {len(analises_servidor)}")
        logger.info("=" * 90)
        
        logger.info("\n✓ TESTE COMPLETADO COM SUCESSO!")
        logger.info(f"Arquivo salvo em: {pdf_path}")
        
    except Exception as e:
        logger.error(f"✗ ERRO: {e}", exc_info=True)


if __name__ == "__main__":
    main()
