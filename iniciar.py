#!/usr/bin/env python3
"""
Inicializador da AGT 4.0 com Banco de Dados
Gerencia SSH tunnel e inicia o Dashboard
"""

import os
import sys
import subprocess
from pathlib import Path
from time import sleep

# Configurações
PROJETO_DIR = Path(__file__).parent
BACKEND_DIR = PROJETO_DIR / "backend"
DASHBOARD_NOVO = BACKEND_DIR / "dashboard_db.py"
DASHBOARD_ANTIGO = BACKEND_DIR / "dashboard.py"

def banner():
    """Exibe banner de boas-vindas."""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                     AGT 4.0 - Dashboard                        ║
    ║            Sistema de Análise de Tickets v4.0 (DB)            ║
    ║                                                                ║
    ║  📊 Dashboard Integrado com PostgreSQL 17 via SSH Tunnel       ║
    ╚════════════════════════════════════════════════════════════════╝
    """)

def menu():
    """Menu de opções."""
    print("\n🎯 Selecione uma opção:\n")
    print("  1️⃣  Dashboard com Banco de Dados (PostgreSQL) - RECOMENDADO")
    print("     → Dados em tempo real, sem limites")
    print()
    print("  2️⃣  Dashboard com Upload de Novos CSVs")
    print("     → Importar e analisar arquivos CSV do Jira")
    print("     → Comparativo entre períodos")
    print()
    print("  3️⃣  Testar Conexão com Banco")
    print("     → Verificar acesso ao PostgreSQL via SSH")
    print()
    print("  4️⃣  Ver Dados do Banco")
    print("     → Preview dos módulos, servidores e tipologia")
    print()
    print("  5️⃣  Sair")
    print()
    
    escolha = input("👉 Digite sua escolha (1-5): ").strip()
    return escolha

def teste_conexao():
    """Testa conexão com banco de dados."""
    print("\n🔍 Testando conexão com banco de dados...")
    print("   Conectando via SSH tunnel a 91.108.124.150...")
    
    try:
        # Importar o serviço
        sys.path.insert(0, str(PROJETO_DIR))
        from backend.servico_tickets import obter_servico
        
        servico = obter_servico()
        resumo = servico.obter_resumo()
        
        print(f"   ✅ Conexão bem-sucedida!")
        print(f"   📊 Total de tickets: {resumo['total']}")
        print(f"   ✅ Abertos: {resumo['abertos']}")
        print(f"   ✔️  Fechados: {resumo['fechados']}")
        
        return True
    except Exception as e:
        print(f"   ❌ Erro na conexão: {e}")
        return False

def ver_dados():
    """Exibe dados do banco."""
    print("\n📊 Dados do Banco de Dados\n")
    
    try:
        sys.path.insert(0, str(PROJETO_DIR))
        from backend.servico_tickets import obter_servico
        
        servico = obter_servico()
        
        print("📦 TOP 10 MÓDULOS:")
        modulos = servico.obter_top_modulos()
        for i, (nome, total) in enumerate(modulos, 1):
            print(f"   {i:2d}. {nome:25s} → {total:3d}")
        
        print("\n🖥️  TOP 10 SERVIDORES:")
        servidores = servico.obter_top_servidores()
        for i, (nome, total) in enumerate(servidores, 1):
            print(f"   {i:2d}. {nome:25s} → {total:3d}")
        
        print("\n📋 TIPOLOGIA:")
        tipologia = servico.obter_tipologia()
        for tipo, total in tipologia:
            pct = (total / sum(t for _, t in tipologia)) * 100
            print(f"   • {tipo:20s} → {total:3d} ({pct:5.1f}%)")
        
        print("\n👤 ORIGEM (Top 5):")
        origem = servico.obter_origem()[:5]
        for relator, total in origem:
            print(f"   • {relator:30s} → {total:3d}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def iniciar_dashboard(modo):
    """Inicia o dashboard."""
    if modo == "1":
        print("\n🚀 Iniciando Dashboard com Banco de Dados...")
        print("   Abrindo em http://localhost:8501")
        print("   ")
        print("   ✨ Funcionalidades:")
        print("      • Dados em tempo real do PostgreSQL")
        print("      • 3 modos: Geral, Período, Comparativo")
        print("      • Sem limites de dados")
        print("      • Carregamento rápido com cache")
        print("   ")
        print("   Pressione Ctrl+C para encerrar\n")
        
        try:
            subprocess.run(
                ["streamlit", "run", str(DASHBOARD_NOVO), "--logger.level=error"],
                cwd=str(PROJETO_DIR)
            )
        except KeyboardInterrupt:
            print("\n\n✅ Dashboard encerrado.")
        except FileNotFoundError:
            print("❌ Streamlit não encontrado. Instale com: pip install streamlit")
    
    elif modo == "2":
        print("\n🚀 Iniciando Dashboard com Upload de CSVs...")
        print("   Abrindo em http://localhost:8501")
        print("   ")
        print("   ✨ Funcionalidades:")
        print("      • Fazer upload de novos CSVs do Jira")
        print("      • Analisar período específico")
        print("      • Comparar entre dois períodos")
        print("      • Gerar relatórios em PDF")
        print("   ")
        print("   Pressione Ctrl+C para encerrar\n")
        
        try:
            subprocess.run(
                ["streamlit", "run", str(DASHBOARD_ANTIGO), "--logger.level=error"],
                cwd=str(PROJETO_DIR)
            )
        except KeyboardInterrupt:
            print("\n\n✅ Dashboard encerrado.")
        except FileNotFoundError:
            print("❌ Streamlit não encontrado. Instale com: pip install streamlit")

def main():
    """Função principal."""
    os.chdir(PROJETO_DIR)
    
    banner()
    
    while True:
        escolha = menu()
        
        if escolha == "1":
            teste_conexao()
            sleep(2)
            iniciar_dashboard("1")
        
        elif escolha == "2":
            iniciar_dashboard("2")
        
        elif escolha == "3":
            teste_conexao()
            input("\n👉 Pressione Enter para continuar...")
        
        elif escolha == "4":
            ver_dados()
            input("\n👉 Pressione Enter para continuar...")
        
        elif escolha == "5":
            print("\n👋 Encerrando... Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando...")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
