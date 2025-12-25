"""
Inicializar banco de dados via SSH Tunnel
"""
import paramiko
import psycopg2
from pathlib import Path
import time

# Configurações
SSH_HOST = "91.108.124.150"
SSH_USER = "root"
SSH_KEY_PATH = Path(__file__).parent / "vps_key.pem"

POSTGRES_HOST = "localhost"  # Usar localhost da VPS
POSTGRES_PORT = 5432
POSTGRES_USER = "adelmosilva"
POSTGRES_PASSWORD = "Dx220304@"
POSTGRES_DB = "pythonai_db"

def criar_tabelas_via_ssh():
    """Cria tabelas no PostgreSQL via SSH"""
    
    print("🔧 Conectando SSH...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname=SSH_HOST,
            port=22,
            username=SSH_USER,
            key_filename=str(SSH_KEY_PATH),
            timeout=10
        )
        print("✅ SSH conectado!")
        
        # SQL para criar tabelas
        sql_commands = [
            """CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                tipo_item VARCHAR(100) NOT NULL,
                responsavel VARCHAR(255),
                relator VARCHAR(255),
                componente VARCHAR(255) NOT NULL,
                prioridade VARCHAR(50),
                status VARCHAR(50) NOT NULL,
                data_criacao TIMESTAMP NOT NULL DEFAULT NOW(),
                data_atualizacao TIMESTAMP NOT NULL DEFAULT NOW(),
                servidor_cluster VARCHAR(255) NOT NULL,
                criado_em TIMESTAMP DEFAULT NOW(),
                atualizado_em TIMESTAMP DEFAULT NOW(),
                snapshot_id INTEGER
            );""",
            """CREATE TABLE IF NOT EXISTS snapshots (
                id SERIAL PRIMARY KEY,
                mes INTEGER NOT NULL,
                ano INTEGER NOT NULL,
                data_snapshot DATE NOT NULL UNIQUE,
                total_tickets_abertos INTEGER DEFAULT 0,
                total_tickets_fechados INTEGER DEFAULT 0,
                total_geral INTEGER DEFAULT 0,
                criado_em TIMESTAMP DEFAULT NOW(),
                atualizado_em TIMESTAMP DEFAULT NOW()
            );""",
            """CREATE TABLE IF NOT EXISTS analises (
                id SERIAL PRIMARY KEY,
                snapshot_id INTEGER NOT NULL REFERENCES snapshots(id),
                tipo_analise VARCHAR(50) NOT NULL,
                dados TEXT NOT NULL,
                total_registros INTEGER DEFAULT 0,
                total_abertos INTEGER DEFAULT 0,
                total_fechados INTEGER DEFAULT 0,
                criado_em TIMESTAMP DEFAULT NOW(),
                atualizado_em TIMESTAMP DEFAULT NOW()
            );""",
            """CREATE TABLE IF NOT EXISTS configuracoes_periodo (
                id SERIAL PRIMARY KEY,
                mes_atual INTEGER NOT NULL,
                ano_atual INTEGER NOT NULL,
                data_inicio_ano TIMESTAMP NOT NULL,
                mes_inicio INTEGER DEFAULT 1,
                criado_em TIMESTAMP DEFAULT NOW(),
                atualizado_em TIMESTAMP DEFAULT NOW()
            );"""
        ]
        
        print("📋 Criando tabelas...")
        
        # Primeiro, descobrir o nome do container PostgreSQL
        print("🔍 Procurando container PostgreSQL...")
        stdin, stdout, stderr = ssh.exec_command("docker ps | grep postgres")
        output = stdout.read().decode()
        
        if not output:
            print("⚠️  Container não encontrado, listando todos...")
            stdin, stdout, stderr = ssh.exec_command("docker ps -a")
            print(stdout.read().decode())
            raise Exception("Container PostgreSQL não encontrado!")
        
        # Extrair nome do container
        container_name = output.split()[0] if output else None
        if not container_name or container_name == "CONTAINER":
            # Tentar formato alternativo
            parts = output.split()
            container_name = parts[-1] if parts else None
        
        print(f"✅ Container encontrado: {container_name}")
        
        # Executar cada comando via psql através de SSH
        for i, sql in enumerate(sql_commands, 1):
            # Escapar aspas para usar em bash
            sql_escaped = sql.replace("'", "'\\''")
            cmd = f"docker exec {container_name} psql -U {POSTGRES_USER} -d {POSTGRES_DB} -c '{sql_escaped}'"
            
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode()
            err = stderr.read().decode()
            
            if "ERROR" in err.upper() or ("error" in err.lower() and "already exists" not in err):
                print(f"⚠️  Comando {i}: {err}")
            else:
                print(f"✅ Tabela {i}/4 criada")
        
        print("\n✅ Todas as tabelas criadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        ssh.close()
        print("🔒 SSH desconectado")


if __name__ == "__main__":
    criar_tabelas_via_ssh()
