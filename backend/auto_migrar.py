"""
Função auxiliar para migração automática de CSV para PostgreSQL
Integrada ao dashboard para sincronizar automaticamente após upload
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from typing import Tuple, Dict

logger = logging.getLogger(__name__)


def converter_data_postgres(data_str):
    """Converte data de DD/MM/YYYY HH:MM para YYYY-MM-DD HH:MM:SS"""
    if not data_str or pd.isna(data_str):
        return None
    try:
        dt = datetime.strptime(str(data_str).strip(), "%d/%m/%Y %H:%M")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return None


def migrar_csv_para_banco(csv_path: Path) -> Tuple[bool, Dict]:
    """
    Migra um CSV para PostgreSQL automaticamente
    
    Args:
        csv_path: Caminho do arquivo CSV
        
    Returns:
        (sucesso: bool, resultado: dict com status e contagem)
    """
    try:
        from backend.ssh_tunnel import SSHTunnelManager
        
        # Ler CSV
        try:
            df = pd.read_csv(csv_path, sep=';', encoding='latin-1')
        except:
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        
        total_linhas = len(df)
        
        # Normalizar dados
        tickets = []
        for idx, row in df.iterrows():
            ticket = {
                'tipo_item': str(row.get('Tipo de item', '')).strip(),
                'responsavel': str(row.get('Responsavel', '')).strip(),
                'relator': str(row.get('Relator', '')).strip(),
                'componente': str(row.get('Componentes', '')).strip(),
                'prioridade': str(row.get('Prioridade', '')).strip(),
                'status': str(row.get('Status', '')).strip(),
                'data_criacao': converter_data_postgres(row.get('Criado', '')),
                'data_atualizacao': converter_data_postgres(row.get('Atualizado(a)', '')),
                'servidor_cluster': str(row.get('Servidores / Cluster', '')).strip(),
            }
            tickets.append(ticket)
        
        # Conectar SSH
        tunnel = SSHTunnelManager()
        tunnel.conectar()
        
        try:
            # Encontrar container
            ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(
                "docker ps -aq -f 'ancestor=postgres:17' | head -1"
            )
            container_id = ssh_stdout.read().decode().strip()
            
            if not container_id:
                return False, {'erro': 'Container PostgreSQL não encontrado'}
            
            # Limpar tickets antigos
            cmd = f"docker exec {container_id} psql -U adelmosilva -d pythonai_db -c 'DELETE FROM tickets;'"
            tunnel.ssh_client.exec_command(cmd)
            
            # Inserir novos tickets em lotes
            sql_inserts = []
            for idx, ticket in enumerate(tickets, 1):
                # Escapar aspas
                campos = {
                    'tipo_item': ticket['tipo_item'].replace("'", "''"),
                    'responsavel': ticket['responsavel'].replace("'", "''"),
                    'relator': ticket['relator'].replace("'", "''"),
                    'componente': ticket['componente'].replace("'", "''"),
                    'prioridade': ticket['prioridade'].replace("'", "''"),
                    'status': ticket['status'].replace("'", "''"),
                    'data_criacao': ticket['data_criacao'] if ticket['data_criacao'] else 'NULL',
                    'data_atualizacao': ticket['data_atualizacao'] if ticket['data_atualizacao'] else 'NULL',
                    'servidor_cluster': ticket['servidor_cluster'].replace("'", "''"),
                }
                
                # Construir INSERT
                data_criacao = f"'{campos['data_criacao']}'::timestamp" if campos['data_criacao'] != 'NULL' else 'NULL'
                data_atualizacao = f"'{campos['data_atualizacao']}'::timestamp" if campos['data_atualizacao'] != 'NULL' else 'NULL'
                
                sql = f"""
                INSERT INTO tickets (tipo_item, responsavel, relator, componente, prioridade, status, data_criacao, data_atualizacao, servidor_cluster, criado_em, atualizado_em)
                VALUES ('{campos['tipo_item']}', '{campos['responsavel']}', '{campos['relator']}', '{campos['componente']}', '{campos['prioridade']}', '{campos['status']}', {data_criacao}, {data_atualizacao}, '{campos['servidor_cluster']}', NOW(), NOW());
                """
                
                sql_inserts.append(sql)
                
                # Inserir em lotes de 100
                if idx % 100 == 0 or idx == len(tickets):
                    batch_sql = " ".join(sql_inserts)
                    cmd = f"docker exec {container_id} psql -U adelmosilva -d pythonai_db -c \"{batch_sql}\""
                    
                    ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
                    stderr = ssh_stderr.read().decode()
                    
                    if stderr and 'ERROR' in stderr.upper():
                        return False, {'erro': f'Erro ao inserir lote: {stderr}', 'linhas_processadas': idx}
                    
                    sql_inserts = []
            
            # Verificar contagem final
            cmd = f"docker exec {container_id} psql -U adelmosilva -d pythonai_db -c 'SELECT COUNT(*) FROM tickets;'"
            ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
            output = ssh_stdout.read().decode()
            
            # Parse contagem
            linhas = output.strip().split('\n')
            count = 0
            if len(linhas) >= 2:
                try:
                    count = int(linhas[2])
                except:
                    pass
            
            return True, {
                'total_csv': total_linhas,
                'total_banco': count,
                'status': 'Sincronizado com sucesso'
            }
        
        finally:
            tunnel.fechar()
    
    except Exception as e:
        logger.error(f"Erro ao migrar CSV: {e}")
        return False, {'erro': str(e)}
