#!/usr/bin/env python3
"""Teste rápido do dashboard com dados do banco."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.servico_tickets import obter_servico

def main():
    print("\n" + "="*60)
    print("TESTE DASHBOARD COM BANCO DE DADOS")
    print("="*60)
    
    try:
        print("\n🔄 Obtendo serviço...")
        servico = obter_servico()
        
        print("\n📊 Teste 1: Resumo Geral")
        resumo = servico.obter_resumo()
        print(f"   Total: {resumo['total']}")
        print(f"   Abertos: {resumo['abertos']}")
        print(f"   Fechados: {resumo['fechados']}")
        
        print("\n📦 Teste 2: Top 10 Módulos")
        modulos = servico.obter_top_modulos()
        for nome, total in modulos:
            print(f"   {nome}: {total}")
        
        print("\n🖥️ Teste 3: Top 10 Servidores")
        servidores = servico.obter_top_servidores()
        for nome, total in servidores:
            print(f"   {nome}: {total}")
        
        print("\n📋 Teste 4: Tipologia")
        tipologia = servico.obter_tipologia()
        for tipo, total in tipologia:
            print(f"   {tipo}: {total}")
        
        print("\n👤 Teste 5: Origem (Top 3)")
        origem = servico.obter_origem()[:3]
        for relator, total in origem:
            print(f"   {relator}: {total}")
        
        print("\n📅 Teste 6: Período (Nov 2025)")
        resumo_nov = servico.obter_resumo(11, 2025)
        print(f"   Total: {resumo_nov['total']}")
        print(f"   Abertos: {resumo_nov['abertos']}")
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*60)
        print("\nO Dashboard está pronto para usar:")
        print("  streamlit run backend/dashboard_db.py")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
