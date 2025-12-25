"""
Migrar dados dos CSVs para PostgreSQL
"""
import pandas as pd
import paramiko
import json
from pathlib import Path
from datetime import datetime, timedelta
import calendar

# Configurações SSH
SSH_HOST = "91.108.124.150"
SSH_USER = "root"
SSH_KEY_PATH = Path(__file__).parent / "vps_key.pem"

POSTGRES_USER = "adelmosilva"
POSTGRES_PASSWORD = "Dx220304@"
POSTGRES_DB = "pythonai_db"

# Arquivos de entrada
DATA_INPUT_DIR = Path(__file__).parent / "data" / "input"
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"

class MigradorCSVParaPG:
    def __init__(self):
        self.ssh = None
        self.container_id = None
        
    def conectar_ssh(self):
        """Conecta ao SSH da VPS"""
        print("🔧 Conectando SSH...")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            hostname=SSH_HOST,
            port=22,
            username=SSH_USER,
            key_filename=str(SSH_KEY_PATH),
            timeout=10
        )
        print("✅ SSH conectado!")
        
    def descobrir_container(self):
        """Descobre o ID do container PostgreSQL"""
        stdin, stdout, stderr = self.ssh.exec_command("docker ps | grep postgres")
        output = stdout.read().decode()
        if output:
            self.container_id = output.split()[0]
            print(f"✅ Container: {self.container_id}")
        else:
            raise Exception("Container PostgreSQL não encontrado!")
            
    def executar_sql(self, sql):
        """Executa comando SQL via SSH"""
        sql_escaped = sql.replace("'", "'\\''")
        cmd = f"docker exec {self.container_id} psql -U {POSTGRES_USER} -d {POSTGRES_DB} -c '{sql_escaped}'"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.read().decode(), stderr.read().decode()
    
    def ler_csvs(self):
        """Lê todos os CSVs"""
        arquivos = []
        
        # Procurar em ambas as pastas
        for diretorio in [DATA_INPUT_DIR, UPLOADS_DIR]:
            if diretorio.exists():
                arquivos.extend(diretorio.glob("*.csv"))
        
        if not arquivos:
            print("⚠️  Nenhum CSV encontrado!")
            return []
        
        print(f"📁 Encontrados {len(arquivos)} CSVs:")
        for arq in arquivos:
            print(f"   - {arq.name}")
        
        return arquivos
    
    def processar_e_inserir(self, arquivo_csv):
        """Processa CSV e insere no banco"""
        print(f"\n📄 Processando: {arquivo_csv.name}")
        
        try:
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            df = None
            
            for enc in encodings:
                try:
                    df = pd.read_csv(arquivo_csv, encoding=enc)
                    print(f"   Encoding: {enc} ✓")
                    break
                except:
                    continue
            
            if df is None:
                print(f"   ❌ Nenhum encoding funcionou!")
                return 0
            
            print(f"   Linhas: {len(df)}")
            
            # Colunas esperadas
            colunas_mapeamento = {
                'Tipo de item Responsável': 'tipo_item',  # Ou Tipo de it em
                'Tipo de it em': 'tipo_item',
                'Relator': 'relator',
                'Componentes': 'componente',
                'Prioridade': 'prioridade',
                'Status': 'status',
                'Criado': 'data_criacao',
                'Atualizado(a)': 'data_atualizacao',
                'Servidores / Cluster': 'servidor_cluster'
            }
            
            # Normalizar colunas
            df.columns = [col.strip() for col in df.columns]
            
            # Inserir cada linha
            inseridos = 0
            erros = 0
            
            for idx, row in df.iterrows():
                try:
                    # Mapear dados
                    tipo_item = str(row.get('Tipo de it em', row.get('Tipo de item Responsável', 'N/A')))
                    relator = str(row.get('Relator', ''))
                    componente = str(row.get('Componentes', 'N/A'))
                    prioridade = str(row.get('Prioridade', ''))
                    status = str(row.get('Status', 'Aberto'))
                    servidor = str(row.get('Servidores / Cluster', 'N/A'))
                    responsavel = str(row.get('Responsável', ''))
                    
                    # Tentar parsear datas
                    try:
                        data_criacao = pd.to_datetime(row.get('Criado', datetime.now())).strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    try:
                        data_atualizacao = pd.to_datetime(row.get('Atualizado(a)', datetime.now())).strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Montar SQL INSERT
                    sql = f"""
                    INSERT INTO tickets (
                        tipo_item, responsavel, relator, componente, prioridade,
                        status, data_criacao, data_atualizacao, servidor_cluster
                    ) VALUES (
                        '{tipo_item.replace("'", "''")}',
                        '{responsavel.replace("'", "''")}',
                        '{relator.replace("'", "''")}',
                        '{componente.replace("'", "''")}',
                        '{prioridade.replace("'", "''")}',
                        '{status.replace("'", "''")}',
                        '{data_criacao}',
                        '{data_atualizacao}',
                        '{servidor.replace("'", "''")}'
                    );
                    """
                    
                    out, err = self.executar_sql(sql)
                    if "ERROR" not in err.upper():
                        inseridos += 1
                    else:
                        erros += 1
                        
                except Exception as e:
                    erros += 1
                    if erros <= 3:  # Mostrar primeiros 3 erros
                        print(f"   ⚠️  Erro na linha {idx}: {str(e)[:100]}")
            
            print(f"   ✅ Inseridos: {inseridos} | ❌ Erros: {erros}")
            return inseridos
            
        except Exception as e:
            print(f"   ❌ Erro ao processar: {e}")
            return 0
    
    def criar_snapshots(self):
        """Cria snapshots mensais"""
        print("\n📸 Criando snapshots mensais...")
        
        # Pegar meses dos dados
        ano_atual = datetime.now().year
        mes_atual = datetime.now().month
        
        for mes in range(1, mes_atual + 1):
            # Contar tickets do mês
            data_inicio = datetime(ano_atual, mes, 1)
            if mes == 12:
                data_fim = datetime(ano_atual + 1, 1, 1) - timedelta(days=1)
            else:
                data_fim = datetime(ano_atual, mes + 1, 1) - timedelta(days=1)
            
            sql = f"""
            INSERT INTO snapshots (mes, ano, data_snapshot, total_geral)
            SELECT
                {mes},
                {ano_atual},
                '{data_inicio.date()}',
                COUNT(*)
            FROM tickets
            WHERE data_criacao >= '{data_inicio}' AND data_criacao <= '{data_fim}'
            ON CONFLICT (data_snapshot) DO NOTHING;
            """
            
            out, err = self.executar_sql(sql)
            if "ERROR" not in err.upper():
                print(f"   ✅ Snapshot {mes}/{ano_atual} criado")
    
    def migrar(self):
        """Executa migração completa"""
        print("=" * 60)
        print("MIGRAÇÃO CSV → PostgreSQL")
        print("=" * 60)
        
        try:
            self.conectar_ssh()
            self.descobrir_container()
            
            # Ler CSVs
            csvs = self.ler_csvs()
            total_inseridos = 0
            
            # Processar cada CSV
            for csv in csvs:
                inseridos = self.processar_e_inserir(csv)
                total_inseridos += inseridos
            
            # Criar snapshots
            self.criar_snapshots()
            
            print(f"\n✅ Migração concluída! Total: {total_inseridos} tickets inseridos")
            
        except Exception as e:
            print(f"\n❌ Erro na migração: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            if self.ssh:
                self.ssh.close()
                print("\n🔒 SSH desconectado")


if __name__ == "__main__":
    migrador = MigradorCSVParaPG()
    migrador.migrar()
