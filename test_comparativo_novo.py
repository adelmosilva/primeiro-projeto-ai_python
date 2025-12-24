#!/usr/bin/env python
"""
Teste das novas funcionalidades de comparativo com Top 10 e Acumulado
"""

import sys
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.utils.jira_parser import parser_jira_csv
from app.services.analysis_service import AnalysisService
from app.services.ticket_service import TicketService
from app.services.pdf_report_service import PDFReportService

def test_novo_comparativo():
    """Testa as novas funcionalidades de Top 10 e Acumulado"""
    
    print("=" * 80)
    print("TESTE: Comparativo com Top 10 e Acumulado")
    print("=" * 80)
    
    # Caminhos dos CSVs
    csv_ant = backend_path.parent / "uploads" / "JIRAS_OUT2025_formatado.csv"
    csv_atu = backend_path.parent / "uploads" / "JIRAS_NOV2025_formatado.csv"
    
    if not csv_ant.exists():
        print(f"❌ Arquivo não encontrado: {csv_ant}")
        return False
    
    if not csv_atu.exists():
        print(f"❌ Arquivo não encontrado: {csv_atu}")
        return False
    
    try:
        # Carregar período anterior
        print("\n📂 Carregando período anterior...")
        tickets_ant = parser_jira_csv(csv_ant)
        print(f"✓ {len(tickets_ant)} tickets carregados de OUT2025")
        
        resumo_ant = AnalysisService.calcular_resumo_executivo(tickets_ant)
        print(f"  - Total: {resumo_ant['total_geral']}")
        print(f"  - Abertos: {resumo_ant['total_abertos']}")
        print(f"  - Fechados: {resumo_ant['total_fechados']}")
        
        # Carregar período atual
        print("\n📂 Carregando período atual...")
        tickets_atu = parser_jira_csv(csv_atu)
        print(f"✓ {len(tickets_atu)} tickets carregados de NOV2025")
        
        resumo_atu = AnalysisService.calcular_resumo_executivo(tickets_atu)
        print(f"  - Total: {resumo_atu['total_geral']}")
        print(f"  - Abertos: {resumo_atu['total_abertos']}")
        print(f"  - Fechados: {resumo_atu['total_fechados']}")
        
        # Testar Top 10 Servidores Atual
        print("\n🏢 Top 10 Servidores - Período Atual:")
        top_10_atual = AnalysisService.top_10_servidores_abertos(tickets_atu)
        if top_10_atual:
            for servidor, count in top_10_atual:
                print(f"  • {servidor}: {count} tickets abertos")
        else:
            print("  (Nenhum servidor com tickets abertos)")
        
        # Testar Top 10 Servidores Acumulado
        print("\n🏢 Top 10 Servidores - Acumulado:")
        top_10_acum = AnalysisService.top_10_servidores_abertos(tickets_ant + tickets_atu)
        if top_10_acum:
            for servidor, count in top_10_acum:
                print(f"  • {servidor}: {count} tickets abertos")
        else:
            print("  (Nenhum servidor com tickets abertos)")
        
        # Testar Resumo Acumulado
        print("\n📊 Resumo Acumulado:")
        resumo_acum = AnalysisService.calcular_resumo_acumulado(tickets_ant, tickets_atu)
        print(f"  - Total Geral: {resumo_acum.get('total_geral', 0)}")
        print(f"  - Total Abertos: {resumo_acum.get('total_abertos', 0)}")
        print(f"  - Total Fechados: {resumo_acum.get('total_fechados', 0)}")
        
        # Gerar outras análises
        print("\n📈 Gerando análises...")
        analises_tipologia = AnalysisService.analisar_por_tipologia(tickets_atu)
        analises_componente = AnalysisService.analisar_por_componente(tickets_atu)
        analises_origem = AnalysisService.analisar_por_origem(tickets_atu)
        analises_prioridade = AnalysisService.analisar_por_prioridade(tickets_atu)
        analises_servidor = AnalysisService.analisar_por_servidor(tickets_atu)
        
        # Preparar comparativo
        comparativo = {
            'periodo_anterior': 'OUT2025',
            'periodo_atual': 'NOV2025',
            'total_anterior': resumo_ant['total_geral'],
            'total_atual': resumo_atu['total_geral'],
            'variacao_total': resumo_atu['total_geral'] - resumo_ant['total_geral'],
            'abertos_anterior': resumo_ant['total_abertos'],
            'abertos_atual': resumo_atu['total_abertos'],
            'variacao_abertos': resumo_atu['total_abertos'] - resumo_ant['total_abertos'],
            'fechados_anterior': resumo_ant['total_fechados'],
            'fechados_atual': resumo_atu['total_fechados'],
            'variacao_fechados': resumo_atu['total_fechados'] - resumo_ant['total_fechados'],
            'backlog_anterior': resumo_ant['backlog_final'],
            'backlog_atual': resumo_atu['backlog_final'],
            'variacao_backlog': resumo_atu['backlog_final'] - resumo_ant['backlog_final'],
            'top_10_servidores_atual': top_10_atual,
            'top_10_servidores_acumulado': top_10_acum,
            'resumo_acumulado': resumo_acum
        }
        
        # Gerar PDF com novas seções
        print("\n📄 Gerando PDF com novas seções...")
        pdf_path = backend_path.parent / "relatorios" / "teste_comparativo_novo.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        
        pdf_service = PDFReportService(pdf_path)
        pdf_service.gerar_relatorio(
            periodo="OUT2025 vs NOV2025",
            resumo=resumo_atu,
            analises_tipologia=analises_tipologia,
            analises_componente=analises_componente,
            analises_origem=analises_origem,
            analises_prioridade=analises_prioridade,
            analises_servidor=analises_servidor,
            comparativo=comparativo,
            resumo_anterior=resumo_ant,
            resumo_acumulado=resumo_acum,
            top_10_servidores_atual=top_10_atual,
            top_10_servidores_acumulado=top_10_acum
        )
        
        print(f"✓ PDF gerado com sucesso: {pdf_path}")
        print(f"  Tamanho: {pdf_path.stat().st_size / 1024:.1f} KB")
        
        print("\n" + "=" * 80)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_novo_comparativo()
    sys.exit(0 if success else 1)
