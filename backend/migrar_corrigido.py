#!/usr/bin/env python3
"""Script para migrar CSVs com delimitador correto (;)."""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ssh_tunnel import SSHTunnelManager
from backend.app.config import UPLOADS_DIR

def clean_ticket_data(row):
    """Limpa e normaliza os dados de um ticket."""
    # Mapear colunas do CSV para o banco
    mapping = {
        'Tipo de item': 'tipo_item',
        'Responsável': 'responsavel',
        'Relator': 'relator',
        'Componentes': 'componente',
        'Status': 'status',
        'Criado': 'data_criacao',
        'Atualizado(a)': 'data_atualizacao',
        'Servidores / Cluster': 'servidor_cluster',
    }
    
    cleaned = {}
    for csv_col, db_col in mapping.items():
        if csv_col in row.index:
            val = row[csv_col]
            if pd.isna(val):
                cleaned[db_col] = None
            else:
                cleaned[db_col] = str(val).strip()
        else:
            cleaned[db_col] = None
    
    # Adicionar campos padrão
    cleaned['criado_em'] = datetime.now().isoformat()
    cleaned['atualizado_em'] = datetime.now().isoformat()
    
    return cleaned

def migrar_csvs():
    """Migra CSVs para PostgreSQL via SSH."""
    print("\n" + "="*60)
    print("MIGRANDO CSVs COM DELIMITADOR CORRETO")
    print("="*60)
    
    tunnel = SSHTunnelManager()
    try:
        print("\n1️⃣ Conectando ao SSH...")
        tunnel.conectar()
        print("   ✅ Conectado")
        
        # Encontrar container
        print("\n2️⃣ Encontrando container PostgreSQL...")
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(
            "docker ps -aq -f 'ancestor=postgres:17' | head -1"
        )
        container_id = ssh_stdout.read().decode().strip()
        print(f"   Container ID: {container_id}")
        
        # Encontrar CSVs
        csv_paths = list(UPLOADS_DIR.glob("*formatado.csv"))
        print(f"\n3️⃣ Encontrados {len(csv_paths)} CSVs em {UPLOADS_DIR}")
        
        total_inseridos = 0
        total_erros = 0
        
        for csv_path in csv_paths:
            print(f"\n📄 Processando {csv_path.name}...")
            
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            df = None
            enc_usado = None
            
            for enc in encodings:
                try:
                    df = pd.read_csv(csv_path, encoding=enc, delimiter=';')
                    enc_usado = enc
                    print(f"   ✅ Encoding: {enc}")
                    break
                except:
                    continue
            
            if df is None:
                print(f"   ❌ Não conseguiu ler o arquivo")
                total_erros += 1
                continue
            
            print(f"   📊 Total de linhas: {len(df)}")
            
            # Inserir cada linha
            for idx, (_, row) in enumerate(df.iterrows()):
                try:
                    cleaned = clean_ticket_data(row)
                    
                    # Montar INSERT
                    cols = []
                    vals = []
                    for col, val in cleaned.items():
                        cols.append(col)
                        if val is None:
                            vals.append("NULL")
                        else:
                            val_str = str(val).replace("'", "''")
                            vals.append(f"'{val_str}'")
                    
                    cols_str = ", ".join(cols)
                    vals_str = ", ".join(vals)
                    sql = f"INSERT INTO tickets ({cols_str}) VALUES ({vals_str})"
                    
                    # Executar INSERT
                    cmd = f"""docker exec {container_id} psql -U adelmosilva -d pythonai_db -c "{sql}" """
                    ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
                    stdout = ssh_stdout.read().decode()
                    
                    total_inseridos += 1
                    
                    if (idx + 1) % 20 == 0:
                        print(f"   ✅ {idx + 1}/{len(df)} inseridos...")
                
                except Exception as e:
                    print(f"   ⚠️ Erro na linha {idx + 1}: {e}")
                    total_erros += 1
            
            print(f"   ✅ {len(df)} registros processados")
        
        # Criar snapshots mensais
        print(f"\n4️⃣ Criando snapshots mensais...")
        
        meses = [
            (10, 2025, "Outubro 2025"),
            (11, 2025, "Novembro 2025"),
        ]
        
        for mes, ano, nome in meses:
            sql = f"""
            INSERT INTO snapshots (mes, ano, data_snapshot, total_tickets_abertos, total_tickets_fechados, total_geral)
            SELECT {mes}, {ano}, NOW(),
                   COUNT(CASE WHEN status IN ('Aberto', 'Em Progresso', 'Aguardando') THEN 1 END) as abertos,
                   COUNT(CASE WHEN status = 'Fechado' THEN 1 END) as fechados,
                   COUNT(*) as total
            FROM tickets
            """
            
            cmd = f"""docker exec {container_id} psql -U adelmosilva -d pythonai_db -c "{sql}" """
            ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
            print(f"   ✅ Snapshot {nome} criado")
        
        # Verificar dados finais
        print(f"\n5️⃣ Verificando dados inseridos...")
        query = "SELECT COUNT(*) as total, COUNT(DISTINCT componente) as componentes FROM tickets"
        cmd = f"""docker exec {container_id} psql -U adelmosilva -d pythonai_db -c "\\copy ({query}) TO STDOUT WITH CSV HEADER" """
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
        output = ssh_stdout.read().decode()
        print(f"\n{output}")
        
        print(f"\n" + "="*60)
        print(f"📊 RESUMO FINAL:")
        print(f"   Total inseridos: {total_inseridos}")
        print(f"   Erros: {total_erros}")
        print(f"="*60)
        
    finally:
        tunnel.ssh_client.close()

if __name__ == "__main__":
    try:
        # Primeiro, limpar dados antigos
        print("\n⚠️ Limpando dados antigos...")
        tunnel = SSHTunnelManager()
        tunnel.conectar()
        
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(
            "docker ps -aq -f 'ancestor=postgres:17' | head -1"
        )
        container_id = ssh_stdout.read().decode().strip()
        
        sqls = ["DELETE FROM snapshots;", "DELETE FROM tickets;"]
        for sql in sqls:
            cmd = f"""docker exec {container_id} psql -U adelmosilva -d pythonai_db -c "{sql}" """
            tunnel.ssh_client.exec_command(cmd)
        
        tunnel.ssh_client.close()
        print("✅ Dados limpos")
        
        # Agora migrar
        migrar_csvs()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
