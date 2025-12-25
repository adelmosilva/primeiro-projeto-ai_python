#!/usr/bin/env python3
"""Script para ZERAR o banco de dados completamente."""

import sys
import os
from pathlib import Path
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ssh_tunnel import (
    SSHTunnelManager, POSTGRES_HOST, POSTGRES_PORT, 
    POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
)

def zerar_banco():
    """Deleta todas as tabelas e zera o banco."""
    print("\n" + "="*60)
    print("⚠️  ZERANDO BANCO DE DADOS")
    print("="*60)
    
    tunnel = SSHTunnelManager()
    try:
        print("\n1️⃣ Conectando ao SSH...")
        if not tunnel.conectar():
            print("   ❌ Falha ao conectar SSH")
            return False
        print("   ✅ Conectado")
        
        print("\n2️⃣ Deletando tabelas e recriando estrutura...")
        
        # SQL para zerar e recriar
        sql_statements = """
-- Deletar tabelas
DROP TABLE IF EXISTS ticket_servers CASCADE;
DROP TABLE IF EXISTS ticket_modules CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS reporters CASCADE;
DROP TABLE IF EXISTS modules CASCADE;
DROP TABLE IF EXISTS servers CASCADE;

-- Criar tabelas
CREATE TABLE servers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reporters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    tipo_item VARCHAR(50),
    relator_id INTEGER REFERENCES reporters(id),
    responsavel VARCHAR(100),
    status VARCHAR(50),
    data_criacao TIMESTAMP,
    data_atualizacao TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ticket_modules (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticket_id, module_id)
);

CREATE TABLE ticket_servers (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    server_id INTEGER NOT NULL REFERENCES servers(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticket_id, server_id)
);

-- Criar índices
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_relator ON tickets(relator_id);
CREATE INDEX idx_tickets_data_criacao ON tickets(data_criacao);
CREATE INDEX idx_ticket_modules_ticket ON ticket_modules(ticket_id);
CREATE INDEX idx_ticket_modules_module ON ticket_modules(module_id);
CREATE INDEX idx_ticket_servers_ticket ON ticket_servers(ticket_id);
CREATE INDEX idx_ticket_servers_server ON ticket_servers(server_id);
        """
        
        # Salvar SQL em arquivo temporário
        sql_file = '/tmp/zerar_banco.sql'
        psql_cmd = f"""
cat > {sql_file} << 'EOF'
{sql_statements}
EOF

docker exec python_ai_pythonai_db psql -U {POSTGRES_USER} -d {POSTGRES_DB} -f {sql_file}
rm {sql_file}
        """
        
        print("\n   Executando SQL remotamente via SSH...")
        stdin, stdout, stderr = tunnel.ssh_client.exec_command(psql_cmd)
        stdout_text = stdout.read().decode('utf-8', errors='ignore')
        stderr_text = stderr.read().decode('utf-8', errors='ignore')
        exit_code = stdout.channel.recv_exit_status()
        
        if exit_code == 0 or 'CREATE' in stdout_text:
            print("   ✅ Tabelas deletadas e recriadas com sucesso")
        else:
            print(f"   ⚠️ Aviso: {stderr_text if stderr_text else stdout_text}")
        
        print("\n" + "="*60)
        print("✅ BANCO DE DADOS ZERADO COM SUCESSO!")
        print("="*60)
        print("\n📝 Próximas opções:")
        print("   1. python backend/migrar_corrigido.py  (para remigrar CSVs)")
        print("   2. Usar o dashboard de upload (upload manual)")
        print("\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        tunnel.fechar()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Zerar banco de dados')
    parser.add_argument('--confirmar', action='store_true', 
                       help='Confirmar exclusão sem perguntar')
    args = parser.parse_args()
    
    if not args.confirmar:
        print("\n⚠️  AVISO: Isso vai deletar TODOS os dados do banco!")
        confirmacao = input("Digite 'sim' para confirmar: ").strip().lower()
        if confirmacao != 'sim':
            print("❌ Operação cancelada")
            sys.exit(1)
    
    sucesso = zerar_banco()
    sys.exit(0 if sucesso else 1)
