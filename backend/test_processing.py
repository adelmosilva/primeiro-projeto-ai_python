"""
Script de teste - Processamento de CSV do Jira e geração de relatório
"""

import logging
from pathlib import Path
import sys

# Adicionar pasta ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.jira_parser import parser_jira_csv
from app.services.ticket_service import TicketService
from app.services.analysis_service import AnalysisService
from app.services.report_service import ReportService
from app.config import INPUT_DIR, REPORTS_OUTPUT_DIR, CURRENT_PERIOD

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Função principal de teste"""
    
    logger.info("=" * 80)
    logger.info("TESTE 1: Carregamento e Processamento do CSV Jira")
    logger.info("=" * 80)
    
    try:
        # 1. Carregar CSV
        csv_path = INPUT_DIR / "JIRAS_NOV2025_formatado.csv"
        
        if not csv_path.exists():
            logger.error(f"Arquivo não encontrado: {csv_path}")
            return
        
        logger.info(f"Carregando arquivo: {csv_path}")
        tickets = parser_jira_csv(csv_path)
        logger.info(f"✓ {len(tickets)} tickets carregados com sucesso\n")
        
        # 2. Processar tickets
        logger.info("Processando tickets...")
        ticket_service = TicketService()
        total_carregados = ticket_service.carregar_tickets(tickets)
        logger.info(f"✓ {total_carregados} tickets processados\n")
        
        # 3. Gerar análises
        logger.info("Gerando análises...")
        
        resumo = AnalysisService.calcular_resumo_executivo(tickets)
        logger.info(f"✓ Resumo executivo gerado")
        logger.info(f"  - Abertos: {resumo['total_abertos']}")
        logger.info(f"  - Fechados: {resumo['total_fechados']}")
        logger.info(f"  - Total: {resumo['total_geral']}\n")
        
        analises_tipologia = AnalysisService.analisar_por_tipologia(tickets)
        logger.info(f"✓ Análise por tipologia ({len(analises_tipologia)} tipos)")
        for tipo, dados in analises_tipologia.items():
            logger.info(f"  - {tipo}: {dados['total']} tickets")
        logger.info("")
        
        analises_componente = AnalysisService.analisar_por_componente(tickets)
        logger.info(f"✓ Análise por componente ({len(analises_componente)} componentes)")
        for comp, dados in analises_componente.items():
            logger.info(f"  - {comp}: {dados['total']} tickets")
        logger.info("")
        
        analises_origem = AnalysisService.analisar_por_origem(tickets)
        logger.info(f"✓ Análise por origem ({len(analises_origem)} origens)")
        for orig, dados in analises_origem.items():
            logger.info(f"  - {orig}: {dados['total']} tickets")
        logger.info("")
        
        analises_prioridade = AnalysisService.analisar_por_prioridade(tickets)
        logger.info(f"✓ Análise por prioridade ({len(analises_prioridade)} prioridades)")
        for prio, dados in analises_prioridade.items():
            logger.info(f"  - {prio}: {dados['total']} tickets")
        logger.info("")
        
        # 4. Gerar relatório
        logger.info("Gerando relatório texto...")
        relatorio = ReportService.gerar_relatorio_texto(
            periodo=CURRENT_PERIOD,
            resumo=resumo,
            analises_tipologia=analises_tipologia,
            analises_componente=analises_componente,
            analises_origem=analises_origem,
            analises_prioridade=analises_prioridade
        )
        logger.info("✓ Relatório gerado com sucesso\n")
        
        # 5. Salvar relatório
        REPORTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        relatorio_path = REPORTS_OUTPUT_DIR / f"relatorio_AGT40_{CURRENT_PERIOD.replace(' ', '_')}.txt"
        
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        logger.info(f"✓ Relatório salvo em: {relatorio_path}\n")
        
        # 6. Exibir relatório
        logger.info("RELATÓRIO GERADO:")
        logger.info("=" * 90)
        print(relatorio)
        logger.info("=" * 90)
        
        logger.info("\n✓ TESTE COMPLETADO COM SUCESSO!")
        
    except Exception as e:
        logger.error(f"✗ ERRO: {e}", exc_info=True)


if __name__ == "__main__":
    main()
