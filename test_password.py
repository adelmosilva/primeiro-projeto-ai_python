#!/usr/bin/env python3
"""
Teste rápido da senha do Supabase
Se der erro aqui, a migração vai falhar
"""

import psycopg2
import sys

SUPABASE_HOST = "db.nmsarhysujzhpjbpnqtl.supabase.co"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Dx220304@28010"
SUPABASE_DB = "postgres"
SUPABASE_PORT = 5432

print("=" * 60)
print("🧪 Teste de Conexão Supabase")
print("=" * 60)
print(f"Host: {SUPABASE_HOST}")
print(f"User: {SUPABASE_USER}")
print(f"Port: {SUPABASE_PORT}")
print(f"Database: {SUPABASE_DB}")
print("=" * 60)

try:
    print("\n⏳ Conectando ao Supabase...")
    conn = psycopg2.connect(
        host=SUPABASE_HOST,
        port=SUPABASE_PORT,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD,
        database=SUPABASE_DB,
        connect_timeout=15,
        application_name="test_connection"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    
    print(f"✅ Conexão bem-sucedida!")
    print(f"   PostgreSQL: {version[:50]}...")
    
    # Testar criação de tabela
    print("\n⏳ Testando criação de tabela...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_migration (
            id SERIAL PRIMARY KEY,
            test_data VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Tabela criada com sucesso!")
    
    # Inserir teste
    print("\n⏳ Testando inserção...")
    cursor.execute(
        "INSERT INTO test_migration (test_data) VALUES (%s) RETURNING id",
        ("teste de conexão",)
    )
    test_id = cursor.fetchone()[0]
    conn.commit()
    print(f"✅ Dado inserido com ID: {test_id}")
    
    # Limpar
    cursor.execute("DROP TABLE IF EXISTS test_migration CASCADE")
    conn.commit()
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("   Pronto para migração: python run_migration.py")
    print("=" * 60)
    sys.exit(0)
    
except psycopg2.OperationalError as e:
    if "resolve" in str(e).lower() or "name" in str(e).lower():
        print(f"\n❌ ERRO DE DNS: {e}")
        print("\n   Solução: Execute em Streamlit Cloud ou verifique DNS local")
    else:
        print(f"\n❌ ERRO DE CONEXÃO: {e}")
        print("\n   Verifique:")
        print("   - Host correto?")
        print("   - Porta 5432 acessível?")
        print("   - Credentials corretas?")
    sys.exit(1)
    
except psycopg2.ProgrammingError as e:
    print(f"\n❌ ERRO SQL: {e}")
    print("   Há um problema com as credenciais ou permissões")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ERRO INESPERADO: {e}")
    sys.exit(1)
