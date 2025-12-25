"""
Serviços para consultar dados do PostgreSQL
"""
import paramiko
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# Configurações SSH
SSH_HOST = "91.108.124.150"
SSH_USER = "root"
SSH_KEY_PATH = Path(__file__).parent / "vps_key.pem"

POSTGRES_USER = "adelmosilva"
POSTGRES_PASSWORD = "Dx220304@"
POSTGRES_DB = "pythonai_db"


class ServicoTicketDB:
    """Serviço para acessar tickets do banco via SSH"""
    
    def __init__(self):
        self.ssh = None
        self.container_id = None
        self._conectar()
    
    def _conectar(self):
        """Conecta ao SSH e descobre container"""
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname=SSH_HOST,
                port=22,
                username=SSH_USER,
                key_filename=str(SSH_KEY_PATH),
                timeout=10
            )
            
            # Descobrir container
            stdin, stdout, stderr = self.ssh.exec_command("docker ps | grep postgres")
            output = stdout.read().decode()
            if output:
                self.container_id = output.split()[0]
        except Exception as e:
            print(f"⚠️  Conexão SSH falhou: {e}")
    
    def _executar_query(self, sql: str) -> pd.DataFrame:
        """Executa query SQL e retorna DataFrame"""
        if not self.ssh or not self.container_id:
            # Retornar mensagem útil ao usuário
            import streamlit as st
            st.error("""
            ❌ **Banco de Dados Indisponível no Streamlit Cloud**
            
            O banco de dados está em um servidor privado e não é acessível 
            do Streamlit Cloud. Há 3 soluções disponíveis:
            
            1. **Usar banco em nuvem** (recomendado): Migrar para Supabase/Neon
            2. **Tunnel público**: Usar ngrok para expor o banco
            3. **API intermediária**: Criar API REST
            
            📖 Veja: `DATABASE_CLOUD_SETUP.md` para instruções detalhadas.
            """)
            raise Exception("Não conectado ao banco de dados")
        
        try:
            # Exportar resultado como CSV via psql
            cmd = f"""docker exec {self.container_id} psql -U {POSTGRES_USER} -d {POSTGRES_DB} -c "COPY ({sql}) TO STDOUT WITH CSV HEADER;" """
            
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            output = stdout.read().decode()
            err = stderr.read().decode()
            
            if "ERROR" in err.upper():
                raise Exception(f"Erro SQL: {err}")
            
            # Converter CSV string para DataFrame
            from io import StringIO
            df = pd.read_csv(StringIO(output))
            return df
            
        except Exception as e:
            print(f"❌ Erro na query: {e}")
            return pd.DataFrame()
    
    def obter_tickets_abertos(self) -> pd.DataFrame:
        """Obtém todos os tickets abertos"""
        sql = "SELECT * FROM tickets WHERE status != 'Fechado' ORDER BY data_criacao DESC"
        return self._executar_query(sql)
    
    def obter_tickets_por_periodo(self, mes: int, ano: int) -> pd.DataFrame:
        """Obtém tickets de um período específico"""
        data_inicio = f"{ano}-{mes:02d}-01"
        
        # Calcular próximo mês
        if mes == 12:
            data_fim = f"{ano + 1}-01-01"
        else:
            data_fim = f"{ano}-{mes + 1:02d}-01"
        
        sql = f"""
        SELECT * FROM tickets 
        WHERE data_criacao >= '{data_inicio}' AND data_criacao < '{data_fim}'
        ORDER BY data_criacao DESC
        """
        return self._executar_query(sql)
    
    def obter_top_modulos(self, mes: int = None, ano: int = None) -> List[Tuple[str, int]]:
        """Obtém top 10 módulos por ticket abertos"""
        
        if mes and ano:
            data_inicio = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_fim = f"{ano + 1}-01-01"
            else:
                data_fim = f"{ano}-{mes + 1:02d}-01"
            
            filtro = f"WHERE data_criacao >= '{data_inicio}' AND data_criacao < '{data_fim}' AND status != 'Fechado'"
        else:
            filtro = "WHERE status != 'Fechado'"
        
        sql = f"""
        SELECT componente, COUNT(*) as total 
        FROM tickets {filtro}
        GROUP BY componente 
        ORDER BY total DESC 
        LIMIT 10
        """
        
        df = self._executar_query(sql)
        return [(row['componente'], row['total']) for _, row in df.iterrows()]
    
    def obter_top_servidores(self, mes: int = None, ano: int = None) -> List[Tuple[str, int]]:
        """Obtém top 10 servidores por tickets abertos"""
        
        if mes and ano:
            data_inicio = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_fim = f"{ano + 1}-01-01"
            else:
                data_fim = f"{ano}-{mes + 1:02d}-01"
            
            filtro = f"WHERE data_criacao >= '{data_inicio}' AND data_criacao < '{data_fim}' AND status != 'Fechado'"
        else:
            filtro = "WHERE status != 'Fechado'"
        
        sql = f"""
        SELECT servidor_cluster, COUNT(*) as total 
        FROM tickets {filtro}
        GROUP BY servidor_cluster 
        ORDER BY total DESC 
        LIMIT 10
        """
        
        df = self._executar_query(sql)
        return [(row['servidor_cluster'], row['total']) for _, row in df.iterrows()]
    
    def obter_top_responsaveis(self, mes: int = None, ano: int = None) -> List[Tuple[str, int]]:
        """Obtém top 10 responsáveis por tickets"""
        
        if mes and ano:
            data_inicio = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_fim = f"{ano + 1}-01-01"
            else:
                data_fim = f"{ano}-{mes + 1:02d}-01"
            
            filtro = f"WHERE data_criacao >= '{data_inicio}' AND data_criacao < '{data_fim}'"
        else:
            filtro = ""
        
        sql = f"""
        SELECT responsavel, COUNT(*) as total 
        FROM tickets {filtro}
        GROUP BY responsavel 
        ORDER BY total DESC 
        LIMIT 10
        """
        
        df = self._executar_query(sql)
        return [(row['responsavel'], row['total']) for _, row in df.iterrows()]
    
    def obter_tipologia(self, mes: int = None, ano: int = None) -> List[Tuple[str, int]]:
        """Obtém tipologia (tipo de item) dos tickets - apenas Support, Incident e Tarefa"""
        
        if mes and ano:
            data_inicio = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_fim = f"{ano + 1}-01-01"
            else:
                data_fim = f"{ano}-{mes + 1:02d}-01"
            
            filtro = f"WHERE data_criacao >= '{data_inicio}' AND data_criacao < '{data_fim}' AND tipo_item IN ('Support', 'Incident', 'Tarefa')"
        else:
            filtro = "WHERE tipo_item IN ('Support', 'Incident', 'Tarefa')"
        
        sql = f"""
        SELECT tipo_item, COUNT(*) as total 
        FROM tickets {filtro}
        GROUP BY tipo_item 
        ORDER BY total DESC
        """
        
        df = self._executar_query(sql)
        return [(row['tipo_item'], row['total']) for _, row in df.iterrows()]
    
    def obter_origem(self, mes: int = None, ano: int = None) -> List[Tuple[str, int]]:
        """Obtém origem (relator) dos tickets"""
        
        if mes and ano:
            data_inicio = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_fim = f"{ano + 1}-01-01"
            else:
                data_fim = f"{ano}-{mes + 1:02d}-01"
            
            filtro = f"WHERE data_criacao >= '{data_inicio}' AND data_criacao < '{data_fim}'"
        else:
            filtro = ""
        
        sql = f"""
        SELECT relator, COUNT(*) as total 
        FROM tickets {filtro}
        GROUP BY relator 
        ORDER BY total DESC 
        LIMIT 10
        """
        
        df = self._executar_query(sql)
        return [(row['relator'], row['total']) for _, row in df.iterrows()]
    
    def obter_resumo(self, mes: int = None, ano: int = None) -> Dict:
        """Obtém resumo geral de tickets"""
        
        if mes and ano:
            data_inicio = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_fim = f"{ano + 1}-01-01"
            else:
                data_fim = f"{ano}-{mes + 1:02d}-01"
            
            filtro = f"WHERE data_criacao >= '{data_inicio}' AND data_criacao < '{data_fim}'"
        else:
            filtro = ""
        
        sql = f"""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status != 'Fechado' THEN 1 ELSE 0 END) as abertos,
            SUM(CASE WHEN status = 'Fechado' THEN 1 ELSE 0 END) as fechados
        FROM tickets {filtro}
        """
        
        df = self._executar_query(sql)
        
        if df.empty:
            return {'total': 0, 'abertos': 0, 'fechados': 0}
        
        row = df.iloc[0]
        return {
            'total': int(row['total']) if pd.notna(row['total']) else 0,
            'abertos': int(row['abertos']) if pd.notna(row['abertos']) else 0,
            'fechados': int(row['fechados']) if pd.notna(row['fechados']) else 0
        }
    
    def desconectar(self):
        """Desconecta SSH"""
        if self.ssh:
            self.ssh.close()


# Singleton global
_servico = None

def obter_servico() -> ServicoTicketDB:
    """Obtém instância do serviço (singleton)"""
    global _servico
    if _servico is None:
        _servico = ServicoTicketDB()
    return _servico
