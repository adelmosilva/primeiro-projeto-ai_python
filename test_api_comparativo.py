#!/usr/bin/env python
"""
Teste de funcionamento da API comparativo com novas tabelas
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Adicionar backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.utils.jira_parser import parser_jira_csv
from app.services.analysis_service import AnalysisService
from app.services.pdf_report_service import PDFReportService

def teste_api_comparativo():
    """Simula o comportamento da API /upload-comparativo"""
    
    print("=" * 100)
    print("TESTE: Simulação da API /upload-comparativo com Novas Tabelas")
    print("=" * 100)
    
    uploads_dir = Path(__file__).parent / "uploads"
    
    # Procurar CSVs
    csvs = sorted(uploads_dir.glob("*.csv"))
    if len(csvs) < 2:
        print(f"[ERRO] Encontrados apenas {len(csvs)} CSV(s). Precisa de 2 para comparativo.")
        return False
    
    arquivo_anterior = csvs[-2]
    arquivo_atual = csvs[-1]
    
    print(f"\n[INFO] Arquivo Anterior: {arquivo_anterior.name}")
    print(f"[INFO] Arquivo Atual: {arquivo_atual.name}")
    
    try:
        # Parse (simulando upload da API)
        print("\n[INFO] Parseando CSV anterior...")
        tickets_ant = parser_jira_csv(arquivo_anterior)
        print(f"[OK] {len(tickets_ant)} tickets carregados")
        
        print("[INFO] Parseando CSV atual...")
        tickets_atu = parser_jira_csv(arquivo_atual)
        print(f"[OK] {len(tickets_atu)} tickets carregados")
        
        # Cálculos de análises (como na API)
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
        
        # NOVAS TABELAS (Seções 11-13)
        print("\n[INFO] Calculando novas tabelas...")
        tabela_tipologia = AnalysisService.tabela_tipologia(tickets_ant, tickets_atu)
        print(f"[OK] Tipologia: {len(tabela_tipologia)} tipos encontrados")
        
        tabela_top10_modulos = AnalysisService.tabela_top10_modulos(tickets_ant, tickets_atu)
        print(f"[OK] Top 10 Módulos: {len(tabela_top10_modulos)} servidores")
        
        tabela_origem = AnalysisService.tabela_origem(tickets_ant, tickets_atu)
        print(f"[OK] Origem: {len(tabela_origem)} categorias")
        
        # Preparar comparativo (como na API)
        periodo_ant_nome = arquivo_anterior.stem.split('_')[0] if '_' in arquivo_anterior.stem else "Anterior"
        periodo_atu_nome = arquivo_atual.stem.split('_')[0] if '_' in arquivo_atual.stem else "Atual"
        
        comparativo = {
            'periodo_anterior': periodo_ant_nome,
            'periodo_atual': periodo_atu_nome,
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
        }
        
        # Gerar PDF (como na API)
        print("\n[INFO] Gerando PDF...")
        reports_dir = Path(__file__).parent / "relatorios"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"relatorio_api_test_{timestamp}.pdf"
        pdf_path = reports_dir / pdf_filename
        
        pdf_service = PDFReportService(pdf_path)
        pdf_service.gerar_relatorio(
            periodo=f"{arquivo_anterior.stem} vs {arquivo_atual.stem}",
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
            # NOVOS PARÂMETROS
            tabela_tipologia=tabela_tipologia,
            tabela_top10_modulos=tabela_top10_modulos,
            tabela_origem=tabela_origem
        )
        
        tamanho_kb = pdf_path.stat().st_size / 1024
        print(f"[OK] PDF gerado: {pdf_path}")
        print(f"[OK] Tamanho: {tamanho_kb:.1f} KB")
        
        # Exibir dados das novas tabelas
        print("\n" + "=" * 100)
        print("NOVAS TABELAS GERADAS")
        print("=" * 100)
        
        print("\n[TIPOLOGIA] - Distribuição por Tipo de Ticket")
        print("-" * 100)
        for row in tabela_tipologia:
            print(f"  {row['tipologia']:15} | "
                  f"Abertos: {row['abertos_anterior']:3}/{row['abertos_atual']:3} | "
                  f"Fechados: {row['fechados_anterior']:3}/{row['fechados_atual']:3} | "
                  f"Total: {row['total_anterior']:3}/{row['total_atual']:3}")
        
        print("\n[TOP 10 MÓDULOS] - Servidores/Clusters com Mais Tickets")
        print("-" * 100)
        for i, row in enumerate(tabela_top10_modulos, 1):
            print(f"  {i:2}. {row['modulo']:20} | "
                  f"Abertos: {row['abertos_anterior']:2}/{row['abertos_atual']:2} | "
                  f"Fechados: {row['fechados_anterior']:3}/{row['fechados_atual']:3}")
        
        print("\n[ORIGEM] - Distribuição por Origem com Percentuais")
        print("-" * 100)
        for row in tabela_origem:
            pct_ant = f"{row['percentual_anterior']:.1f}%"
            pct_atu = f"{row['percentual_atual']:.1f}%"
            print(f"  {row['origem']:20} | "
                  f"Abertos: {row['abertos_anterior']:2}/{row['abertos_atual']:2} | "
                  f"Fechados: {row['fechados_anterior']:3}/{row['fechados_atual']:3} | "
                  f"% {pct_ant:>5}/{pct_atu:>5}")
        
        # Resumo final
        print("\n" + "=" * 100)
        print("✅ TESTE DA API CONCLUÍDO COM SUCESSO!")
        print("=" * 100)
        print(f"\nResumo do Comparativo:")
        print(f"  Período Anterior: {len(tickets_ant)} tickets")
        print(f"  Período Atual: {len(tickets_atu)} tickets")
        print(f"  Variação: {comparativo['variacao_total']:+d} tickets")
        print(f"\n  Abertos - Anterior: {comparativo['abertos_anterior']}, Atual: {comparativo['abertos_atual']}")
        print(f"  Fechados - Anterior: {comparativo['fechados_anterior']}, Atual: {comparativo['fechados_atual']}")
        print(f"\nPDF Salvo: {pdf_path}")
        
        return True
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = teste_api_comparativo()
    sys.exit(0 if success else 1)
