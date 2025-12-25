"""
Conexão SSH usando paramiko + psycopg2 direto
"""
import paramiko
import psycopg2
from pathlib import Path
import time

# Configurações SSH
SSH_HOST = "91.108.124.150"
SSH_PORT = 22
SSH_USER = "root"
SSH_KEY_PATH = Path(__file__).parent / "vps_key.pem"

# Configurações PostgreSQL
POSTGRES_HOST = "python_ai_pythonai_db"  # Nome do serviço no Docker
POSTGRES_PORT = 5432
POSTGRES_USER = "adelmosilva"
POSTGRES_PASSWORD = "Dx220304@"
POSTGRES_DB = "pythonai_db"

LOCAL_BIND_PORT = 5433


class SSHTunnelManager:
    def __init__(self):
        self.ssh_client = None
        self.transport = None
        self.server = None
        
    def conectar(self):
        """Estabelece conexão SSH"""
        print(f"🔧 Conectando SSH a {SSH_HOST}...")
        
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Conectar com chave privada
            self.ssh_client.connect(
                hostname=SSH_HOST,
                port=SSH_PORT,
                username=SSH_USER,
                key_filename=str(SSH_KEY_PATH),
                timeout=10
            )
            
            print(f"✅ SSH conectado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar SSH: {e}")
            return False
    
    def criar_tunnel(self):
        """Cria tunnel para PostgreSQL"""
        print(f"🔧 Criando tunnel para PostgreSQL...")
        
        try:
            self.transport = self.ssh_client.get_transport()
            self.server = self.transport.open_channel(
                'direct-tcpip',
                (POSTGRES_HOST, POSTGRES_PORT),
                ('127.0.0.1', 0)
            )
            print(f"✅ Tunnel criado na porta local {LOCAL_BIND_PORT}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar tunnel: {e}")
            return False
    
    def testar_postgres(self):
        """Testa conexão com PostgreSQL"""
        print(f"🔍 Testando conexão com PostgreSQL...")
        
        try:
            # Conectar via paramiko socket
            sock = self.ssh_client.get_transport().open_session()
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                database=POSTGRES_DB,
                timeout=5
            )
            
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"✅ Conectado ao PostgreSQL!")
            print(f"   {version[0]}")
            
            cur.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erro ao testar PostgreSQL: {e}")
            return False
    
    def fechar(self):
        """Fecha todas as conexões"""
        if self.ssh_client:
            self.ssh_client.close()
            print("✅ SSH desconectado")


def testar_simples():
    """Teste simples de conexão via paramiko"""
    print("=" * 60)
    print("TESTE SSH TUNNEL COM PARAMIKO")
    print("=" * 60)
    
    manager = SSHTunnelManager()
    
    if manager.conectar():
        print("\n✅ Agora você pode usar:")
        print(f"   postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
        print(f"\nSe via SSH tunnel local, use:")
        print(f"   postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@127.0.0.1:{LOCAL_BIND_PORT}/{POSTGRES_DB}")
        
        # Manter conexão aberta
        try:
            print("\n✅ Tunnel ativo! Pressione Ctrl+C para encerrar...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Encerrando...")
            manager.fechar()
    else:
        print("\n❌ Falha ao conectar SSH")


if __name__ == "__main__":
    testar_simples()
