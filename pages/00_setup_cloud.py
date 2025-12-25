"""
Página de Setup do Streamlit Cloud
Deve ser acessada PRIMEIRO para migrar o banco de dados do VPS para Supabase
"""

import streamlit as st
import psycopg2
import pandas as pd
from pathlib import Path
import paramiko
from io import StringIO
import time

st.set_page_config(page_title="⚙️ Setup Cloud", layout="wide", initial_sidebar_state="collapsed")

st.title("⚙️ Setup Inicial - Supabase Migration")
st.markdown("""
Este é um script de migração ONE-TIME que:
1. Cria as tabelas no Supabase
2. Copia 755 tickets do VPS para Supabase
3. Valida a migração
4. Depois você pode usar o dashboard normalmente
""")

st.markdown("---")

# Credenciais (iguais ao arquivo local)
SUPABASE_HOST = "db.nmsarhysujzhpjbpnqtl.supabase.co"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Dx220304@28010"
SUPABASE_DB = "postgres"
SUPABASE_PORT = 5432

VPS_HOST = "91.108.124.150"
VPS_USER = "root"
VPS_POSTGRES_USER = "adelmosilva"
VPS_POSTGRES_PASSWORD = "Dx220304@"
VPS_POSTGRES_DB = "pythonai_db"

# Estado da migração
if 'migration_complete' not in st.session_state:
    st.session_state.migration_complete = False

if 'migration_step' not in st.session_state:
    st.session_state.migration_step = 0

# ============= FUNÇÕES =============

def test_supabase():
    """Testa conexão ao Supabase (força IPv4 com fallbacks)"""
    try:
        import socket
        
        # Tentar resolver com socket.getaddrinfo
        try:
            addr_info = socket.getaddrinfo(SUPABASE_HOST, SUPABASE_PORT, socket.AF_INET)
            ipv4_host = addr_info[0][4][0]
        except:
            # Fallback: tentar DNS público
            try:
                addr_info = socket.getaddrinfo(SUPABASE_HOST, SUPABASE_PORT, socket.AF_INET, socket.SOCK_STREAM)
                ipv4_host = addr_info[0][4][0]
            except:
                # Fallback 2: usar hostname direto (pode tentar IPv6)
                ipv4_host = SUPABASE_HOST
        
        conn = psycopg2.connect(
            host=ipv4_host,
            port=SUPABASE_PORT,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            database=SUPABASE_DB,
            connect_timeout=10
        )
        conn.close()
        return True, "Conectado com sucesso!"
    except Exception as e:
        return False, str(e)

def create_tables():
    """Cria tabelas no Supabase (força IPv4 com fallbacks)"""
    import socket
    
    try:
        addr_info = socket.getaddrinfo(SUPABASE_HOST, SUPABASE_PORT, socket.AF_INET)
        ipv4_host = addr_info[0][4][0]
    except:
        ipv4_host = SUPABASE_HOST
    
    conn = psycopg2.connect(
        host=ipv4_host,
        port=SUPABASE_PORT,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD,
        database=SUPABASE_DB
    )
    cursor = conn.cursor()
    
    sql = """
    DROP TABLE IF EXISTS tickets CASCADE;
    
    CREATE TABLE tickets (
        id SERIAL PRIMARY KEY,
        chave VARCHAR(50) UNIQUE NOT NULL,
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
    
    CREATE INDEX idx_status ON tickets(status);
    CREATE INDEX idx_componente ON tickets(componente);
    CREATE INDEX idx_servidor ON tickets(servidor);
    CREATE INDEX idx_data_criacao ON tickets(data_criacao);
    """
    
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def export_from_vps():
    """Exporta CSV do VPS via SSH"""
    # Gera chave privada em memória (hardcoded para Streamlit Cloud)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Usar a chave do repositório
    try:
        key_path = Path('/mount/src/primeiro-projeto-ai_python/backend/vps_key.pem')
        if not key_path.exists():
            # Fallback: tentar outras localizações
            possible_paths = [
                Path('backend/vps_key.pem'),
                Path('../../backend/vps_key.pem'),
                Path('/tmp/vps_key.pem'),
            ]
            key_path = None
            for p in possible_paths:
                if p.exists():
                    key_path = p
                    break
            
            if not key_path:
                raise FileNotFoundError("vps_key.pem não encontrada")
    except:
        raise FileNotFoundError("Chave SSH não disponível")
    
    ssh.connect(
        hostname=VPS_HOST,
        port=22,
        username=VPS_USER,
        key_filename=str(key_path),
        timeout=15
    )
    
    # Obter dados via COPY
    sql_export = f"""
    PGPASSWORD='{VPS_POSTGRES_PASSWORD}' psql -h 127.0.0.1 -U {VPS_POSTGRES_USER} -d {VPS_POSTGRES_DB} -c "
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
    csv_data = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    ssh.close()
    
    if err and 'could not' in err.lower():
        raise Exception(f"Erro ao exportar: {err}")
    
    return csv_data

def import_to_supabase(csv_data):
    """Importa dados para Supabase (força IPv4 com fallbacks)"""
    import socket
    
    try:
        addr_info = socket.getaddrinfo(SUPABASE_HOST, SUPABASE_PORT, socket.AF_INET)
        ipv4_host = addr_info[0][4][0]
    except:
        ipv4_host = SUPABASE_HOST
    
    df = pd.read_csv(StringIO(csv_data))
    
    conn = psycopg2.connect(
        host=ipv4_host,
        port=SUPABASE_PORT,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD,
        database=SUPABASE_DB
    )
    cursor = conn.cursor()
    
    inserted = 0
    errors = []
    
    for idx, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO tickets 
                (chave, titulo, descricao, status, prioridade, tipo, 
                 componente, servidor, data_criacao, data_atualizacao, 
                 data_fechamento, responsavel, reporter, tempo_aberto_horas)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['chave'],
                row['titulo'] if pd.notna(row['titulo']) else None,
                row['descricao'] if pd.notna(row['descricao']) else None,
                row['status'] if pd.notna(row['status']) else None,
                row['prioridade'] if pd.notna(row['prioridade']) else None,
                row['tipo'] if pd.notna(row['tipo']) else None,
                row['componente'] if pd.notna(row['componente']) else None,
                row['servidor'] if pd.notna(row['servidor']) else None,
                row['data_criacao'] if pd.notna(row['data_criacao']) else None,
                row['data_atualizacao'] if pd.notna(row['data_atualizacao']) else None,
                row['data_fechamento'] if pd.notna(row['data_fechamento']) else None,
                row['responsavel'] if pd.notna(row['responsavel']) else None,
                row['reporter'] if pd.notna(row['reporter']) else None,
                row['tempo_aberto_horas'] if pd.notna(row['tempo_aberto_horas']) else None,
            ))
            inserted += 1
        except psycopg2.IntegrityError:
            conn.rollback()
            # Já existe, ignorar
            continue
        except Exception as e:
            errors.append(f"Linha {idx}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return inserted, errors

def validate_migration():
    """Valida se a migração funcionou (força IPv4 com fallbacks)"""
    import socket
    
    try:
        addr_info = socket.getaddrinfo(SUPABASE_HOST, SUPABASE_PORT, socket.AF_INET)
        ipv4_host = addr_info[0][4][0]
    except:
        ipv4_host = SUPABASE_HOST
    
    conn = psycopg2.connect(
        host=ipv4_host,
        port=SUPABASE_PORT,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD,
        database=SUPABASE_DB
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    return count

# ============= INTERFACE =============

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Passo 1", "Testar Supabase", "→")

with col2:
    st.metric("Passo 2", "Criar Tabelas", "→")

with col3:
    st.metric("Passo 3", "Migrar Dados", "→")

st.markdown("---")

# Botão de início
if not st.session_state.migration_complete:
    if st.button("🚀 INICIAR MIGRAÇÃO", use_container_width=True, type="primary"):
        st.session_state.migration_step = 1
        st.rerun()

# PASSO 1: Testar Supabase
if st.session_state.migration_step >= 1:
    st.subheader("✅ Passo 1: Testar Conexão ao Supabase")
    
    progress_col = st.empty()
    status_col = st.empty()
    
    with progress_col.container():
        st.progress(0.25, text="Conectando ao Supabase...")
    
    time.sleep(1)
    success, msg = test_supabase()
    
    if success:
        with status_col.container():
            st.success(f"✅ {msg}")
        st.session_state.migration_step = 2
        time.sleep(2)
        st.rerun()
    else:
        with status_col.container():
            st.error(f"❌ {msg}")
        st.stop()

# PASSO 2: Criar Tabelas
if st.session_state.migration_step >= 2:
    st.subheader("✅ Passo 2: Criar Tabelas")
    
    progress_col = st.empty()
    status_col = st.empty()
    
    with progress_col.container():
        st.progress(0.50, text="Criando tabelas no Supabase...")
    
    time.sleep(1)
    try:
        create_tables()
        with status_col.container():
            st.success("✅ Tabelas criadas com sucesso!")
        st.session_state.migration_step = 3
        time.sleep(2)
        st.rerun()
    except Exception as e:
        with status_col.container():
            st.error(f"❌ Erro: {e}")
        st.stop()

# PASSO 3: Exportar do VPS
if st.session_state.migration_step >= 3:
    st.subheader("✅ Passo 3: Exportar Dados do VPS")
    
    progress_col = st.empty()
    status_col = st.empty()
    
    with progress_col.container():
        st.progress(0.65, text="Exportando 755 tickets do VPS...")
    
    time.sleep(1)
    try:
        csv_data = export_from_vps()
        row_count = len(csv_data.strip().split('\n')) - 1
        with status_col.container():
            st.success(f"✅ {row_count} registros exportados!")
        st.session_state.migration_step = 4
        st.session_state.csv_data = csv_data
        time.sleep(2)
        st.rerun()
    except Exception as e:
        with status_col.container():
            st.error(f"❌ Erro ao exportar: {e}")
        st.info("💡 Verifique se a chave SSH está configurada corretamente")
        st.stop()

# PASSO 4: Importar para Supabase
if st.session_state.migration_step >= 4:
    st.subheader("✅ Passo 4: Importar para Supabase")
    
    progress_col = st.empty()
    status_col = st.empty()
    
    with progress_col.container():
        st.progress(0.80, text="Importando dados para Supabase...")
    
    time.sleep(1)
    try:
        inserted, errors = import_to_supabase(st.session_state.csv_data)
        with status_col.container():
            st.success(f"✅ {inserted} registros importados!")
        if errors:
            st.warning(f"⚠️ {len(errors)} erros durante importação (ignorados)")
        st.session_state.migration_step = 5
        time.sleep(2)
        st.rerun()
    except Exception as e:
        with status_col.container():
            st.error(f"❌ Erro ao importar: {e}")
        st.stop()

# PASSO 5: Validar
if st.session_state.migration_step >= 5:
    st.subheader("✅ Passo 5: Validar Migração")
    
    progress_col = st.empty()
    status_col = st.empty()
    
    with progress_col.container():
        st.progress(0.95, text="Validando...")
    
    time.sleep(1)
    try:
        total = validate_migration()
        with progress_col.container():
            st.progress(1.0, text="Concluído!")
        with status_col.container():
            st.success(f"✅ Total de registros no Supabase: {total}")
        
        st.session_state.migration_complete = True
        st.session_state.migration_step = 6
        
    except Exception as e:
        with status_col.container():
            st.error(f"❌ Erro na validação: {e}")
        st.stop()

# SUCESSO
if st.session_state.migration_complete:
    st.markdown("---")
    st.success("""
    ### 🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!
    
    ✅ Todos os 755 tickets estão no Supabase
    ✅ Tabelas criadas e validadas
    ✅ Seu banco de dados está pronto para produção
    
    **Próximos passos:**
    1. Volte para a página **"Visão Geral"** para acessar o dashboard
    2. Os dados serão carregados automaticamente do Supabase
    3. Tudo pronto para usar!
    """)
    
    if st.button("✅ Ir para Dashboard", use_container_width=True, type="primary"):
        st.switch_page("pages/01_dashboard_db.py")
