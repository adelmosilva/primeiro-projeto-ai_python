"""
Exemplo de uso do serviço de tickets
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.servico_tickets import obter_servico

def testar_servico():
    """Testa o serviço"""
    print("=" * 60)
    print("TESTE SERVIÇO TICKETS DATABASE")
    print("=" * 60)
    
    servico = obter_servico()
    
    try:
        # Resumo geral
        print("\n📊 RESUMO GERAL:")
        resumo = servico.obter_resumo()
        print(f"   Total: {resumo['total']}")
        print(f"   Abertos: {resumo['abertos']}")
        print(f"   Fechados: {resumo['fechados']}")
        
        # Top 10 módulos
        print("\n📦 TOP 10 MÓDULOS:")
        modulos = servico.obter_top_modulos()
        for modulo, count in modulos[:5]:
            print(f"   {modulo}: {count}")
        
        # Top 10 servidores
        print("\n🖥️  TOP 10 SERVIDORES:")
        servidores = servico.obter_top_servidores()
        for servidor, count in servidores[:5]:
            print(f"   {servidor}: {count}")
        
        # Tipologia
        print("\n📋 TIPOLOGIA:")
        tipologia = servico.obter_tipologia()
        for tipo, count in tipologia[:5]:
            print(f"   {tipo}: {count}")
        
        # Origem
        print("\n👤 ORIGEM (TOP 5):")
        origem = servico.obter_origem()
        for relator, count in origem[:5]:
            print(f"   {relator}: {count}")
        
        # Por período (Novembro 2025)
        print("\n📅 PERÍODO (NOV 2025):")
        resumo_nov = servico.obter_resumo(mes=11, ano=2025)
        print(f"   Total: {resumo_nov['total']}")
        print(f"   Abertos: {resumo_nov['abertos']}")
        
        print("\n✅ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        servico.desconectar()


if __name__ == "__main__":
    testar_servico()
