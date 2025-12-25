"""
Script de teste - Comparativo entre períodos (Outubro vs Novembro 2025)
Gera relatórios em PDF com análises e comparativos
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


def processar_periodo(csv_filename: str, periodo: str):
    """
    Processa um período específico
    
    Args:
        csv_filename: Nome do arquivo CSV
        periodo: Nome do período
        
    Returns:
        Dicionário com tickets e análises
    """
    csv_path = INPUT_DIR / csv_filename
    
    if not csv_path.exists():
        logger.error(f"Arquivo não encontrado: {csv_path}")
        return None
    
    logger.info(f"Processando {periodo}...")
    
    # Parser
    tickets = parser_jira_csv(csv_path)
    
    # Serviço
    service = TicketService()
    service.carregar_tickets(tickets)
    
    # Análises
    resumo = AnalysisService.calcular_resumo_executivo(tickets)
    analises_tipologia = AnalysisService.analisar_por_tipologia(tickets)
    analises_componente = AnalysisService.analisar_por_componente(tickets)
    analises_origem = AnalysisService.analisar_por_origem(tickets)
    analises_prioridade = AnalysisService.analisar_por_prioridade(tickets)
    
    return {
        'periodo': periodo,
        'tickets': tickets,
        'resumo': resumo,
        'analises_tipologia': analises_tipologia,
        'analises_componente': analises_componente,
        'analises_origem': analises_origem,
        'analises_prioridade': analises_prioridade
    }


def gerar_comparativo(dados_outubro, dados_novembro):
    """
    Gera dados de comparativo entre os dois períodos
    
    Args:
        dados_outubro: Dados processados de outubro
        dados_novembro: Dados processados de novembro
        
    Returns:
        Dicionário com comparativas
    """
    res_out = dados_outubro['resumo']
    res_nov = dados_novembro['resumo']
    
    return {
        'periodo_anterior': dados_outubro['periodo'],
        'periodo_atual': dados_novembro['periodo'],
        'total_anterior': res_out['total_geral'],
        'total_atual': res_nov['total_geral'],
        'variacao_total': res_nov['total_geral'] - res_out['total_geral'],
        'abertos_anterior': res_out['total_abertos'],
        'abertos_atual': res_nov['total_abertos'],
        'variacao_abertos': res_nov['total_abertos'] - res_out['total_abertos'],
        'fechados_anterior': res_out['total_fechados'],
        'fechados_atual': res_nov['total_fechados'],
        'variacao_fechados': res_nov['total_fechados'] - res_out['total_fechados'],
        'backlog_anterior': res_out['backlog_final'],
        'backlog_atual': res_nov['backlog_final'],
        'variacao_backlog': res_nov['backlog_final'] - res_out['backlog_final']
    }


def main():
    """Função principal"""
    
    logger.info("=" * 90)
    logger.info("TESTE 2: GERAÇÃO DE RELATÓRIOS EM PDF COM COMPARATIVOS")
    logger.info("=" * 90)
    
    try:
        # Processar Outubro
        logger.info("\n[1/4] Processando Outubro 2025...")
        dados_outubro = processar_periodo("JIRAS_OUT2025_formatado.csv", "Outubro de 2025")
        if not dados_outubro:
            return
        logger.info(f"✓ Outubro processado: {len(dados_outubro['tickets'])} tickets\n")
        
        # Processar Novembro
        logger.info("[2/4] Processando Novembro 2025...")
        dados_novembro = processar_periodo("JIRAS_NOV2025_formatado.csv", "Novembro de 2025")
        if not dados_novembro:
            return
        logger.info(f"✓ Novembro processado: {len(dados_novembro['tickets'])} tickets\n")
        
        # Gerar Comparativo
        logger.info("[3/4] Gerando dados de comparativo...")
        comparativo = gerar_comparativo(dados_outubro, dados_novembro)
        
        logger.info("✓ Comparativo gerado:")
        logger.info(f"  Outubro:  {comparativo['total_anterior']} tickets")
        logger.info(f"  Novembro: {comparativo['total_atual']} tickets")
        logger.info(f"  Variação: {comparativo['variacao_total']:+.0f}")
        logger.info("")
        
        # Gerar PDFs
        logger.info("[4/4] Gerando relatórios em PDF...\n")
        
        REPORTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # PDF Outubro
        pdf_outubro = PDFReportService(
            REPORTS_OUTPUT_DIR / "relatorio_AGT40_Outubro_2025.pdf"
        )
        path_out = pdf_outubro.gerar_relatorio(
            periodo="Outubro de 2025",
            resumo=dados_outubro['resumo'],
            analises_tipologia=dados_outubro['analises_tipologia'],
            analises_componente=dados_outubro['analises_componente'],
            analises_origem=dados_outubro['analises_origem'],
            analises_prioridade=dados_outubro['analises_prioridade']
        )
        logger.info(f"✓ PDF Outubro gerado: {path_out.name}")
        
        # PDF Novembro
        pdf_novembro = PDFReportService(
            REPORTS_OUTPUT_DIR / "relatorio_AGT40_Novembro_2025.pdf"
        )
        path_nov = pdf_novembro.gerar_relatorio(
            periodo="Novembro de 2025",
            resumo=dados_novembro['resumo'],
            analises_tipologia=dados_novembro['analises_tipologia'],
            analises_componente=dados_novembro['analises_componente'],
            analises_origem=dados_novembro['analises_origem'],
            analises_prioridade=dados_novembro['analises_prioridade']
        )
        logger.info(f"✓ PDF Novembro gerado: {path_nov.name}")
        
        # PDF Comparativo
        pdf_comparativo = PDFReportService(
            REPORTS_OUTPUT_DIR / "relatorio_AGT40_Comparativo_OutNov_2025.pdf"
        )
        path_comp = pdf_comparativo.gerar_relatorio(
            periodo="Outubro vs Novembro de 2025",
            resumo=dados_novembro['resumo'],
            analises_tipologia=dados_novembro['analises_tipologia'],
            analises_componente=dados_novembro['analises_componente'],
            analises_origem=dados_novembro['analises_origem'],
            analises_prioridade=dados_novembro['analises_prioridade'],
            comparativo=comparativo
        )
        logger.info(f"✓ PDF Comparativo gerado: {path_comp.name}\n")
        
        # Resumo de Comparativos
        logger.info("=" * 90)
        logger.info("RESUMO DE COMPARATIVOS - OUTUBRO vs NOVEMBRO")
        logger.info("=" * 90)
        logger.info(f"\n{'Métrica':<30} {'Outubro':>12} {'Novembro':>12} {'Variação':>12}")
        logger.info("-" * 70)
        logger.info(f"{'Total de Tickets':<30} {comparativo['total_anterior']:>12} {comparativo['total_atual']:>12} {comparativo['variacao_total']:>+12.0f}")
        logger.info(f"{'Tickets Abertos':<30} {comparativo['abertos_anterior']:>12} {comparativo['abertos_atual']:>12} {comparativo['variacao_abertos']:>+12.0f}")
        logger.info(f"{'Tickets Fechados':<30} {comparativo['fechados_anterior']:>12} {comparativo['fechados_atual']:>12} {comparativo['variacao_fechados']:>+12.0f}")
        logger.info(f"{'Backlog':<30} {comparativo['backlog_anterior']:>12} {comparativo['backlog_atual']:>12} {comparativo['variacao_backlog']:>+12.0f}")
        logger.info("=" * 90)
        
        logger.info("\n✓ TESTE COMPLETADO COM SUCESSO!")
        logger.info(f"\nArquivos gerados em: {REPORTS_OUTPUT_DIR}")
        logger.info("- relatorio_AGT40_Outubro_2025.pdf")
        logger.info("- relatorio_AGT40_Novembro_2025.pdf")
        logger.info("- relatorio_AGT40_Comparativo_OutNov_2025.pdf")
        
    except Exception as e:
        logger.error(f"✗ ERRO: {e}", exc_info=True)


if __name__ == "__main__":
    main()
