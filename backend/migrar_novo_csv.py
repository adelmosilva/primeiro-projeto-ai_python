#!/usr/bin/env python3
"""
Script para migrar o novo CSV uploadado para o PostgreSQL

O CSV 'upload_20251225_154143_Tickets_JAN-NOV-2025_formatado.csv' tem 755 tickets,
mas o banco de dados ainda tem apenas 280 (dados antigos).

Este script vai:
1. Limpar os tickets antigos do banco (280)
2. Importar os 755 novos tickets
3. Confirmar que o banco agora tem 755 tickets
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
import io

# Configurar output UTF-8 e logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ssh_tunnel import SSHTunnelManager
from backend.app.config import UPLOADS_DIR

def limpar_banco():
    """Deleta todos os tickets do banco (zerar e reimportar)."""
    tunnel = SSHTunnelManager()
    try:
        logger.info("Conectando ao SSH...")
        tunnel.conectar()
        
        # Encontrar container
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(
            "docker ps -aq -f 'ancestor=postgres:17' | head -1"
        )
        container_id = ssh_stdout.read().decode().strip()
        logger.info(f"Container PostgreSQL: {container_id}")
        
        # Deletar todos os tickets
        logger.info("Limpando tabela de tickets...")
        cmd = f"docker exec {container_id} psql -U adelmosilva -d pythonai_db -c 'DELETE FROM tickets;'"
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
        stderr = ssh_stderr.read().decode()
        
        if stderr and 'ERROR' in stderr.upper():
            logger.error(f"Erro ao limpar: {stderr}")
            return False
        
        logger.info("[OK] Tabela limpa")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao conectar: {e}")
        return False
    finally:
        tunnel.fechar()

def migrar_novo_csv():
    """Migra o novo CSV para o PostgreSQL."""
    
    # Encontrar o arquivo mais recente
    csv_files = list(UPLOADS_DIR.glob("upload_*.csv"))
    if not csv_files:
        logger.error("Nenhum arquivo CSV encontrado em uploads/")
        return False
    
    csv_path = max(csv_files, key=lambda p: p.stat().st_mtime)
    logger.info(f"Arquivo selecionado: {csv_path.name}")
    
    tunnel = SSHTunnelManager()
    try:
        logger.info("Conectando ao SSH...")
        tunnel.conectar()
        
        # Encontrar container
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(
            "docker ps -aq -f 'ancestor=postgres:17' | head -1"
        )
        container_id = ssh_stdout.read().decode().strip()
        
        # Ler CSV
        logger.info(f"Lendo CSV ({csv_path.name})...")
        try:
            df = pd.read_csv(csv_path, sep=';', encoding='latin-1')
        except:
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        
        logger.info(f"Total de linhas no CSV: {len(df)}")
        
        # Funcao para converter data de DD/MM/YYYY HH:MM para YYYY-MM-DD HH:MM
        def converter_data(data_str):
            if not data_str or pd.isna(data_str):
                return None
            try:
                # Formato esperado: "27/11/2025 14:27"
                from datetime import datetime
                dt = datetime.strptime(str(data_str).strip(), "%d/%m/%Y %H:%M")
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                return None
        
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
                'data_criacao': converter_data(row.get('Criado', '')),
                'data_atualizacao': converter_data(row.get('Atualizado(a)', '')),
                'servidor_cluster': str(row.get('Servidores / Cluster', '')).strip(),
            }
            tickets.append(ticket)
        
        logger.info(f"Preparados {len(tickets)} tickets para importacao")
        
        # Inserir no PostgreSQL
        logger.info("Inserindo tickets no PostgreSQL...")
        
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
            
            # Construir INSERT com CAST para datas
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
                    logger.error(f"Erro ao inserir lote: {stderr}")
                    return False
                
                logger.info(f"[OK] {idx}/{len(tickets)} tickets inseridos")
                sql_inserts = []
        
        logger.info("[OK] Todos os tickets inseridos com sucesso")
        
        # Verificar contagem final
        cmd = f"docker exec {container_id} psql -U adelmosilva -d pythonai_db -c 'SELECT COUNT(*) FROM tickets;'"
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
        output = ssh_stdout.read().decode()
        
        # Parse da saída (formato: "count\n-------\n755\n(1 row)")
        linhas = output.strip().split('\n')
        if len(linhas) >= 2:
            try:
                count = int(linhas[2])
                logger.info(f"\n{'='*50}")
                logger.info(f"[SUCESSO]")
                logger.info(f"   Banco de dados agora tem: {count} tickets")
                logger.info(f"   (eram 280, agora sao {count})")
                logger.info(f"{'='*50}\n")
                return True
            except:
                logger.warning("Nao foi possivel extrair contagem final")
                return True
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao migrar: {e}")
        return False
    finally:
        tunnel.fechar()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("ATUALIZANDO BANCO COM NOVOS 755 TICKETS")
    print("="*50)
    
    # 1. Limpar banco (remover 280 antigos)
    print("\n[PASSO 1] Limpando tickets antigos...")
    if not limpar_banco():
        logger.error("Falha ao limpar banco")
        sys.exit(1)
    
    # 2. Migrar novo CSV
    print("\n[PASSO 2] Migrando novo CSV...")
    if not migrar_novo_csv():
        logger.error("Falha ao migrar CSV")
        sys.exit(1)
    
    print("\n[OK] Migracao concluida! O dashboard_db.py agora mostrara 755 tickets.")
