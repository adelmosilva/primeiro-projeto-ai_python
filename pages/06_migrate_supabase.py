"""
Script para preparar migração via Streamlit Cloud
Executa no Streamlit Cloud e tem acesso a DNS funcional
"""

import streamlit as st
import psycopg2
import pandas as pd
from pathlib import Path
import paramiko
from datetime import datetime
import sys

st.set_page_config(page_title="Migração Supabase", layout="wide")

st.title("📊 Migração: VPS → Supabase")
st.markdown("Migrar 755 tickets do PostgreSQL VPS para Supabase Cloud")
st.markdown("---")

# Credenciais
SUPABASE_HOST = "db.nmsarhysujzhpjbpnqtl.supabase.co"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Dx220304@28010"
SUPABASE_DB = "postgres"
SUPABASE_PORT = 5432

VPS_HOST = "91.108.124.150"
VPS_USER = "root"
VPS_KEY_PATH = Path(__file__).parent / "backend" / "vps_key.pem"

POSTGRES_USER = "adelmosilva"
POSTGRES_PASSWORD = "Dx220304@"
POSTGRES_DB = "pythonai_db"

# Estados
if 'migration_status' not in st.session_state:
    st.session_state.migration_status = "ready"

# ============= FUNÇÕES =============

def test_supabase_connection():
    """Testa conexão ao Supabase"""
    try:
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            database=SUPABASE_DB,
            connect_timeout=10
        )
        conn.close()
        return True, "✅ Conectado ao Supabase!"
    except Exception as e:
        return False, f"❌ Erro: {e}"

def create_tables():
    """Cria tabelas no Supabase"""
    try:
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            database=SUPABASE_DB
        )
        cursor = conn.cursor()
        
        sql = """
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
        
        CREATE INDEX IF NOT EXISTS idx_status ON tickets(status);
        CREATE INDEX IF NOT EXISTS idx_componente ON tickets(componente);
        CREATE INDEX IF NOT EXISTS idx_servidor ON tickets(servidor);
        CREATE INDEX IF NOT EXISTS idx_data_criacao ON tickets(data_criacao);
        """
        
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return True, "✅ Tabelas criadas!"
    except Exception as e:
        return False, f"❌ Erro ao criar tabelas: {e}"

def export_from_vps():
    """Exporta dados do VPS via SSH"""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            hostname=VPS_HOST,
            port=22,
            username=VPS_USER,
            key_filename=str(VPS_KEY_PATH),
            timeout=15
        )
        
        # Obter container ID
        stdin, stdout, stderr = ssh.exec_command("docker ps | grep postgres")
        container_id = stdout.read().decode().split()[0]
        
        # Exportar dados
        sql_export = f"""
        docker exec {container_id} psql -U {POSTGRES_USER} -d {POSTGRES_DB} -c "
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
        
        if csv_data:
            return True, csv_data
        else:
            return False, "Nenhum dado exportado"
            
    except Exception as e:
        return False, f"Erro ao conectar ao VPS: {e}"

def import_to_supabase(csv_data):
    """Importa dados para Supabase"""
    try:
        from io import StringIO
        df = pd.read_csv(StringIO(csv_data))
        
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            database=SUPABASE_DB
        )
        cursor = conn.cursor()
        
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
            except Exception as e:
                st.warning(f"Erro na linha {idx}: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, f"{inserted}/{len(df)} registros inseridos"
        
    except Exception as e:
        return False, f"Erro ao importar: {e}"

# ============= INTERFACE =============

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1️⃣ Testar Conexão")
    if st.button("🧪 Testar Supabase", key="test"):
        with st.spinner("Testando..."):
            success, msg = test_supabase_connection()
            if success:
                st.success(msg)
            else:
                st.error(msg)

with col2:
    st.subheader("2️⃣ Criar Tabelas")
    if st.button("📋 Criar Tabelas", key="create"):
        with st.spinner("Criando tabelas..."):
            success, msg = create_tables()
            if success:
                st.success(msg)
            else:
                st.error(msg)

with col3:
    st.subheader("3️⃣ Executar Migração")
    if st.button("🚀 Migrar Dados", key="migrate"):
        st.session_state.migration_status = "running"

# Executar migração
if st.session_state.migration_status == "running":
    st.markdown("---")
    st.subheader("🔄 Processando Migração...")
    
    progress_bar = st.progress(0)
    status_box = st.empty()
    
    # Step 1: Exportar do VPS
    status_box.info("📤 Exportando dados do VPS...")
    progress_bar.progress(25)
    success, result = export_from_vps()
    
    if not success:
        st.error(f"❌ Erro na exportação: {result}")
        st.session_state.migration_status = "error"
    else:
        csv_data = result
        status_box.success(f"✅ {len(csv_data)} bytes exportados")
        progress_bar.progress(50)
        
        # Step 2: Criar tabelas
        status_box.info("📋 Criando tabelas...")
        progress_bar.progress(60)
        success, msg = create_tables()
        if not success:
            st.error(f"❌ Erro: {msg}")
            st.session_state.migration_status = "error"
        else:
            status_box.success(msg)
            progress_bar.progress(75)
            
            # Step 3: Importar dados
            status_box.info("💾 Importando dados...")
            progress_bar.progress(85)
            success, msg = import_to_supabase(csv_data)
            
            if not success:
                st.error(f"❌ Erro: {msg}")
                st.session_state.migration_status = "error"
            else:
                st.success(f"✅ {msg}")
                progress_bar.progress(100)
                
                st.markdown("---")
                st.success("""
                ### 🎉 Migração Concluída!
                
                ✅ Seus 755 tickets foram migrados para Supabase com sucesso!
                
                **Próximos passos:**
                1. Verificar dados no Supabase: https://app.supabase.com
                2. Fazer deploy da aplicação no Streamlit Cloud
                3. Acessar o dashboard em produção
                """)
                
                st.session_state.migration_status = "done"
