"""
Script para migrar dados do VPS PostgreSQL para Supabase
"""

import psycopg2
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime

# Configurações VPS (original)
VPS_CONFIG = {
    'host': '91.108.124.150',
    'port': 22,
    'user': 'root',
    'key_path': Path(__file__).parent / 'vps_key.pem',
}

# Configurações Supabase (destino)
SUPABASE_CONFIG = {
    'host': 'db.nmsarhysujzhpjbpnqtl.supabase.co',
    'port': 5432,
    'user': 'postgres',
    'password': 'Dx220304@28010',
    'database': 'postgres',
}

# Configurações PostgreSQL VPS (via SSH)
POSTGRES_CONFIG = {
    'user': 'adelmosilva',
    'password': 'Dx220304@',
    'database': 'pythonai_db',
}

def conectar_supabase():
    """Conecta ao Supabase"""
    try:
        conn = psycopg2.connect(
            host=SUPABASE_CONFIG['host'],
            port=SUPABASE_CONFIG['port'],
            user=SUPABASE_CONFIG['user'],
            password=SUPABASE_CONFIG['password'],
            database=SUPABASE_CONFIG['database']
        )
        print("✅ Conectado ao Supabase!")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {e}")
        return None

def executar_query_supabase(conn, sql):
    """Executa query no Supabase"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao executar query: {e}")
        conn.rollback()
        return False

def criar_tabelas_supabase(conn):
    """Cria tabelas no Supabase"""
    
    # Tabela principal de tickets
    sql_tickets = """
    CREATE TABLE IF NOT EXISTS tickets (
        id SERIAL PRIMARY KEY,
        chave VARCHAR(50) UNIQUE,
        titulo TEXT,
        descricao TEXT,
        status VARCHAR(50),
        prioridade VARCHAR(20),
        tipo VARCHAR(50),
        componente VARCHAR(100),
        servidor VARCHAR(100),
        data_criacao TIMESTAMP,
        data_atualizacao TIMESTAMP,
        data_fechamento TIMESTAMP,
        responsavel VARCHAR(100),
        reporter VARCHAR(100),
        tempo_aberto_horas FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Índices para performance
    sql_indices = """
    CREATE INDEX IF NOT EXISTS idx_status ON tickets(status);
    CREATE INDEX IF NOT EXISTS idx_componente ON tickets(componente);
    CREATE INDEX IF NOT EXISTS idx_servidor ON tickets(servidor);
    CREATE INDEX IF NOT EXISTS idx_data_criacao ON tickets(data_criacao);
    """
    
    print("📝 Criando tabelas...")
    if executar_query_supabase(conn, sql_tickets):
        print("✅ Tabela tickets criada!")
    
    if executar_query_supabase(conn, sql_indices):
        print("✅ Índices criados!")

def migrar_dados_via_ssh():
    """Migra dados do VPS para Supabase via SSH"""
    try:
        import paramiko
        
        # Conectar ao VPS via SSH
        print("🔌 Conectando ao VPS via SSH...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=VPS_CONFIG['host'],
            port=VPS_CONFIG['port'],
            username=VPS_CONFIG['user'],
            key_filename=str(VPS_CONFIG['key_path']),
            timeout=10
        )
        print("✅ Conectado ao VPS!")
        
        # Obter container ID
        stdin, stdout, stderr = ssh.exec_command("docker ps | grep postgres")
        container_id = stdout.read().decode().split()[0]
        print(f"📦 Container: {container_id}")
        
        # Exportar dados do VPS como CSV
        print("📤 Exportando dados do VPS...")
        sql_export = f"""
        docker exec {container_id} psql -U {POSTGRES_CONFIG['user']} -d {POSTGRES_CONFIG['database']} -c "
        COPY (
            SELECT 
                chave,
                titulo,
                descricao,
                status,
                prioridade,
                tipo,
                componente,
                servidor,
                data_criacao,
                data_atualizacao,
                data_fechamento,
                responsavel,
                reporter,
                tempo_aberto_horas
            FROM tickets
            ORDER BY id
        ) TO STDOUT WITH CSV HEADER;"
        """
        
        stdin, stdout, stderr = ssh.exec_command(sql_export)
        csv_data = stdout.read().decode()
        ssh.close()
        
        if not csv_data:
            print("❌ Nenhum dado exportado!")
            return False
        
        print(f"✅ Dados exportados! ({len(csv_data)} bytes)")
        
        # Salvar em arquivo temporário
        csv_file = Path(__file__).parent / 'tickets_export.csv'
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write(csv_data)
        
        return csv_file
        
    except Exception as e:
        print(f"❌ Erro na exportação: {e}")
        return None

def importar_dados_supabase(conn, csv_file):
    """Importa dados do CSV para Supabase"""
    try:
        print("📥 Lendo CSV...")
        df = pd.read_csv(csv_file)
        print(f"✅ {len(df)} registros lidos")
        
        cursor = conn.cursor()
        
        # Inserir dados
        print("💾 Inserindo dados no Supabase...")
        inserted = 0
        
        for idx, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO tickets 
                    (chave, titulo, descricao, status, prioridade, tipo, 
                     componente, servidor, data_criacao, data_atualizacao, 
                     data_fechamento, responsavel, reporter, tempo_aberto_horas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (chave) DO UPDATE SET
                    titulo = EXCLUDED.titulo,
                    status = EXCLUDED.status,
                    data_atualizacao = EXCLUDED.data_atualizacao
                """, (
                    row['chave'],
                    row['titulo'],
                    row['descricao'],
                    row['status'],
                    row['prioridade'],
                    row['tipo'],
                    row['componente'],
                    row['servidor'],
                    row['data_criacao'],
                    row['data_atualizacao'],
                    row['data_fechamento'] if pd.notna(row['data_fechamento']) else None,
                    row['responsavel'] if pd.notna(row['responsavel']) else None,
                    row['reporter'] if pd.notna(row['reporter']) else None,
                    row['tempo_aberto_horas'] if pd.notna(row['tempo_aberto_horas']) else None,
                ))
                inserted += 1
                
                if inserted % 100 == 0:
                    print(f"  ↳ {inserted}/{len(df)} registros inseridos...")
                    
            except Exception as e:
                print(f"⚠️  Erro ao inserir linha {idx}: {e}")
        
        conn.commit()
        cursor.close()
        print(f"✅ {inserted}/{len(df)} registros inseridos com sucesso!")
        
        return inserted == len(df)
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

def validar_migracao(conn):
    """Valida se a migração foi bem-sucedida"""
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tickets;")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status != 'Fechado';")
        abertos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Fechado';")
        fechados = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT componente) FROM tickets;")
        componentes = cursor.fetchone()[0]
        
        cursor.close()
        
        print("\n" + "="*50)
        print("📊 RESUMO DA MIGRAÇÃO")
        print("="*50)
        print(f"✅ Total de tickets: {total}")
        print(f"📖 Abertos: {abertos}")
        print(f"✔️  Fechados: {fechados}")
        print(f"📦 Componentes únicos: {componentes}")
        print("="*50)
        
        return total > 0
        
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False

def main():
    """Executa a migração completa"""
    print("\n" + "="*50)
    print("🚀 MIGRAÇÃO VPS → SUPABASE")
    print("="*50)
    
    # Conectar ao Supabase
    conn = conectar_supabase()
    if not conn:
        return False
    
    # Criar tabelas
    criar_tabelas_supabase(conn)
    
    # Migrar dados
    csv_file = migrar_dados_via_ssh()
    if not csv_file:
        conn.close()
        return False
    
    # Importar dados
    if not importar_dados_supabase(conn, csv_file):
        conn.close()
        return False
    
    # Validar
    validar_migracao(conn)
    
    # Limpar
    csv_file.unlink()
    conn.close()
    
    print("\n✅ Migração concluída com sucesso!")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
