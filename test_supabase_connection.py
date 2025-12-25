#!/usr/bin/env python
"""
Teste de conexão ao Supabase
"""

import psycopg2
import sys

print("🧪 Testando conexão com Supabase...\n")

config = {
    'host': 'db.nmsarhysujzhpjbpnqtl.supabase.co',
    'port': 5432,
    'user': 'postgres',
    'password': 'Dx220304@28010',
    'database': 'postgres',
    'connect_timeout': 15
}

try:
    print(f"Conectando a: {config['host']}:{config['port']}")
    print(f"User: {config['user']}")
    print(f"DB: {config['database']}\n")
    
    conn = psycopg2.connect(**config)
    
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    
    print("✅ Conexão bem-sucedida!")
    print(f"PostgreSQL: {version[0]}\n")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"❌ Erro de conexão: {e}\n")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro: {type(e).__name__}: {e}\n")
    sys.exit(1)
