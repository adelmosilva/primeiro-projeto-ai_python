#!/usr/bin/env python
"""
Teste dos novos métodos de análise para o relatório detalhado
"""

import sys
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.utils.jira_parser import parser_jira_csv
from app.services.analysis_service import AnalysisService

def test_novos_metodos():
    """Testa os novos métodos de análise"""
    
    print("=" * 100)
    print("TESTE: Novos Metodos de Analise com CSV Anual")
    print("=" * 100)
    
    # Caminho do CSV anual
    csv_anual = backend_path.parent / "uploads" / "Tickets_JAN-NOV-2025_formatado.csv"
    
    if not csv_anual.exists():
        print(f"[ERRO] Arquivo nao encontrado: {csv_anual}")
        return False
    
    try:
        # Carregar CSV anual
        print("\n[INFO] Carregando CSV anual (JAN-NOV 2025)...")
        tickets_anual = parser_jira_csv(csv_anual)
        print(f"[OK] {len(tickets_anual)} tickets carregados")
        
        # Teste 1: Tabela de Tipologia
        print("\n" + "=" * 100)
        print("1. TABELA DE TIPOLOGIA (Suporte, Tarefa, Incidente)")
        print("=" * 100)
        
        # Simulando período anterior (primeiros 60%) e período atual (últimos 40%)
        split_idx = int(len(tickets_anual) * 0.6)
        tickets_ant = tickets_anual[:split_idx]
        tickets_atu = tickets_anual[split_idx:]
        
        print(f"\nPeríodo Anterior: {len(tickets_ant)} tickets")
        print(f"Período Atual: {len(tickets_atu)} tickets\n")
        
        tabela_tipologia = AnalysisService.tabela_tipologia(tickets_ant, tickets_atu)
        print("TIPOLOGIA | Abertos Ant | Abertos Atu | Fechados Ant | Fechados Atu | Total Ant | Total Atu")
        print("-" * 100)
        for row in tabela_tipologia:
            print(f"{row['tipologia']:<15} | {row['abertos_anterior']:<11} | {row['abertos_atual']:<11} | {row['fechados_anterior']:<12} | {row['fechados_atual']:<12} | {row['total_anterior']:<9} | {row['total_atual']:<9}")
        
        # Teste 2: Tabela de Top 10 Módulos
        print("\n" + "=" * 100)
        print("2. TABELA TOP 10 MÓDULOS (Servidores/Clusters)")
        print("=" * 100)
        
        tabela_modulos = AnalysisService.tabela_top10_modulos(tickets_ant, tickets_atu)
        print("\nMÓDULO | Abertos Ant | Abertos Atu | Fechados Ant | Fechados Atu")
        print("-" * 100)
        for row in tabela_modulos:
            print(f"{row['modulo']:<30} | {row['abertos_anterior']:<11} | {row['abertos_atual']:<11} | {row['fechados_anterior']:<12} | {row['fechados_atual']:<12}")
        
        # Teste 3: Tabela de Origem
        print("\n" + "=" * 100)
        print("3. TABELA DE ORIGEM (Database, Middleware, Infra)")
        print("=" * 100)
        
        tabela_origem = AnalysisService.tabela_origem(tickets_ant, tickets_atu)
        print("\nORIGEM | Abertos Ant | Abertos Atu | Fechados Ant | Fechados Atu | Total Ant | Total Atu | % Ant | % Atu")
        print("-" * 120)
        for row in tabela_origem:
            print(f"{row['origem']:<15} | {row['abertos_anterior']:<11} | {row['abertos_atual']:<11} | {row['fechados_anterior']:<12} | {row['fechados_atual']:<12} | {row['total_anterior']:<9} | {row['total_atual']:<9} | {row['percentual_anterior']:<5} | {row['percentual_atual']:<5}")
        
        # Teste 4: Resumo executivo
        print("\n" + "=" * 100)
        print("4. RESUMO EXECUTIVO")
        print("=" * 100)
        
        resumo_ant = AnalysisService.calcular_resumo_executivo(tickets_ant)
        resumo_atu = AnalysisService.calcular_resumo_executivo(tickets_atu)
        resumo_acum = AnalysisService.calcular_resumo_acumulado(tickets_ant, tickets_atu)
        
        print(f"\nPeríodo Anterior:")
        print(f"  - Total: {resumo_ant['total_geral']}")
        print(f"  - Abertos: {resumo_ant['total_abertos']}")
        print(f"  - Fechados: {resumo_ant['total_fechados']}")
        print(f"  - Backlog: {resumo_ant['backlog_final']}")
        
        print(f"\nPeríodo Atual:")
        print(f"  - Total: {resumo_atu['total_geral']}")
        print(f"  - Abertos: {resumo_atu['total_abertos']}")
        print(f"  - Fechados: {resumo_atu['total_fechados']}")
        print(f"  - Backlog: {resumo_atu['backlog_final']}")
        
        print(f"\nAcumulado:")
        print(f"  - Total: {resumo_acum['total_geral']}")
        print(f"  - Abertos: {resumo_acum['total_abertos']}")
        print(f"  - Fechados: {resumo_acum['total_fechados']}")
        
        print("\n" + "=" * 100)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 100)
        return True
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_novos_metodos()
    sys.exit(0 if success else 1)
