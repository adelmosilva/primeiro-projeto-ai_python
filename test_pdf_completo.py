#!/usr/bin/env python
"""
Teste final com geração de PDF incluindo novas tabelas
"""

import sys
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.utils.jira_parser import parser_jira_csv
from app.services.analysis_service import AnalysisService
from app.services.pdf_report_service import PDFReportService

def test_pdf_completo():
    """Testa geração de PDF com todas as tabelas"""
    
    print("=" * 100)
    print("TESTE FINAL: Geracao de PDF com Tabelas Detalhadas")
    print("=" * 100)
    
    csv_anual = backend_path.parent / "uploads" / "Tickets_JAN-NOV-2025_formatado.csv"
    
    if not csv_anual.exists():
        print(f"[ERRO] Arquivo nao encontrado: {csv_anual}")
        return False
    
    try:
        print("\n[INFO] Carregando CSV anual...")
        tickets_anual = parser_jira_csv(csv_anual)
        print(f"[OK] {len(tickets_anual)} tickets carregados")
        
        # Dividir em períodos
        split_idx = int(len(tickets_anual) * 0.6)
        tickets_ant = tickets_anual[:split_idx]
        tickets_atu = tickets_anual[split_idx:]
        
        print(f"\n[INFO] Período anterior: {len(tickets_ant)} tickets")
        print(f"[INFO] Período atual: {len(tickets_atu)} tickets")
        
        # Calcular análises
        print("\n[INFO] Calculando análises...")
        resumo_ant = AnalysisService.calcular_resumo_executivo(tickets_ant)
        resumo_atu = AnalysisService.calcular_resumo_executivo(tickets_atu)
        resumo_acum = AnalysisService.calcular_resumo_acumulado(tickets_ant, tickets_atu)
        
        analises_tipologia = AnalysisService.analisar_por_tipologia(tickets_atu)
        analises_componente = AnalysisService.analisar_por_componente(tickets_atu)
        analises_origem = AnalysisService.analisar_por_origem(tickets_atu)
        analises_prioridade = AnalysisService.analisar_por_prioridade(tickets_atu)
        analises_servidor = AnalysisService.analisar_por_servidor(tickets_atu)
        
        top_10_atual = AnalysisService.top_10_servidores_por_total(tickets_atu)
        top_10_acum = AnalysisService.top_10_servidores_por_total(tickets_ant + tickets_atu)
        
        # Tabelas
        tabela_tipologia = AnalysisService.tabela_tipologia(tickets_ant, tickets_atu)
        tabela_top10_modulos = AnalysisService.tabela_top10_modulos(tickets_ant, tickets_atu)
        tabela_origem = AnalysisService.tabela_origem(tickets_ant, tickets_atu)
        
        comparativo = {
            'periodo_anterior': 'JAN-JUN',
            'periodo_atual': 'JUL-NOV',
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
        
        # Gerar PDF
        print("\n[INFO] Gerando PDF com tabelas detalhadas...")
        pdf_path = backend_path.parent / "relatorios" / "relatorio_completo_final.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        
        pdf_service = PDFReportService(pdf_path)
        pdf_service.gerar_relatorio(
            periodo="JAN-JUN vs JUL-NOV 2025",
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
            top_10_servidores_acumulado=top_10_acum,
            tabela_tipologia=tabela_tipologia,
            tabela_top10_modulos=tabela_top10_modulos,
            tabela_origem=tabela_origem
        )
        
        tamanho_kb = pdf_path.stat().st_size / 1024
        print(f"[OK] PDF gerado: {pdf_path}")
        print(f"[OK] Tamanho: {tamanho_kb:.1f} KB")
        
        print("\n" + "=" * 100)
        print("[OK] TESTE CONCLUIDO COM SUCESSO!")
        print("=" * 100)
        
        print("\nResumo do PDF gerado:")
        print(f"  - Periodo Anterior: {comparativo['periodo_anterior']} ({resumo_ant['total_geral']} tickets)")
        print(f"  - Periodo Atual: {comparativo['periodo_atual']} ({resumo_atu['total_geral']} tickets)")
        print(f"  - Variacao: {comparativo['variacao_total']:+d} tickets")
        print(f"  - Acumulado: {resumo_acum['total_geral']} tickets no ano")
        print(f"\nSeccoes do PDF:")
        print(f"  1. Resumo Executivo")
        print(f"  2-6. Analises (Tipologia, Componente, Origem, Prioridade, Servidor)")
        print(f"  7. Comparativo com Periodo Anterior")
        print(f"  8. Resumo Acumulado")
        print(f"  9-10. Top 10 Servidores")
        print(f"  11. Analise por Tipologia (TABELA)")
        print(f"  12. Top 10 Modulos (TABELA)")
        print(f"  13. Analise por Origem (TABELA)")
        
        return True
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_completo()
    sys.exit(0 if success else 1)
