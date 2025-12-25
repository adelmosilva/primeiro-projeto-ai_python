#!/usr/bin/env python3
"""Script para diagnosticar problema de NaN nas colunas de string."""

import os
import sys
import pandas as pd
from pathlib import Path

# Adicionar o diretório parent ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ssh_tunnel import SSHTunnelManager
from backend.servico_tickets import ServicoTicketDB

def debug_csv_export():
    """Testa o export CSV direto do PostgreSQL."""
    print("\n" + "="*60)
    print("DEBUG: Testando export CSV direto do banco")
    print("="*60)
    
    tunnel = SSHTunnelManager()
    try:
        # Conectar ao servidor SSH
        print("\n1. Conectando ao SSH...")
        tunnel.conectar()
        print("   ✅ SSH conectado")
        
        # Executar query simples
        print("\n2. Executando query de teste...")
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(
            "docker ps -aq -f 'ancestor=postgres:17' | head -1"
        )
        container_id = ssh_stdout.read().decode().strip()
        print(f"   Container ID: {container_id}")
        
        # Query 1: Ver dados brutos
        print("\n3. Dados brutos (SELECT * LIMIT 5):")
        query = "SELECT id, tipo_item, componente, servidor_cluster, relator FROM tickets LIMIT 5"
        cmd = f"""docker exec {container_id} psql -U adelmosilva -d pythonai_db -c "\\copy ({query}) TO STDOUT WITH CSV HEADER" """
        
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd)
        output = ssh_stdout.read().decode()
        print(output)
        if ssh_stderr:
            error = ssh_stderr.read().decode()
            if error:
                print(f"   Erro: {error}")
        
        # Query 2: Ver GROUP BY
        print("\n4. GROUP BY componente:")
        query2 = "SELECT componente, COUNT(*) as total FROM tickets GROUP BY componente LIMIT 10"
        cmd2 = f"""docker exec {container_id} psql -U adelmosilva -d pythonai_db -c "\\copy ({query2}) TO STDOUT WITH CSV HEADER" """
        
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd2)
        output2 = ssh_stdout.read().decode()
        print(output2)
        if ssh_stderr:
            error = ssh_stderr.read().decode()
            if error:
                print(f"   Erro: {error}")
        
        # Query 3: Contar NULLs
        print("\n5. Verificando NULLs/vazios:")
        query3 = """SELECT 
            COUNT(*) as total,
            COUNT(DISTINCT componente) as componentes_distinct,
            COUNT(CASE WHEN componente IS NULL THEN 1 END) as componentes_null,
            COUNT(CASE WHEN componente = '' THEN 1 END) as componentes_vazio,
            COUNT(DISTINCT servidor_cluster) as servidores_distinct,
            COUNT(CASE WHEN servidor_cluster IS NULL THEN 1 END) as servidores_null
        FROM tickets"""
        cmd3 = f"""docker exec {container_id} psql -U adelmosilva -d pythonai_db -c "\\copy ({query3}) TO STDOUT WITH CSV HEADER" """
        
        ssh_stdin, ssh_stdout, ssh_stderr = tunnel.ssh_client.exec_command(cmd3)
        output3 = ssh_stdout.read().decode()
        print(output3)
        if ssh_stderr:
            error = ssh_stderr.read().decode()
            if error:
                print(f"   Erro: {error}")
        
        # Agora testar com pandas
        print("\n" + "="*60)
        print("DEBUG: Testando parsing com pandas")
        print("="*60)
        
        # Converter output3 em DataFrame
        from io import StringIO
        df_debug = pd.read_csv(StringIO(output3))
        print("\nDataFrame de debug:")
        print(df_debug)
        print(f"\nDtypes:\n{df_debug.dtypes}")
        
    finally:
        tunnel.desconectar()

def debug_servico():
    """Testa o serviço usando a mesma abordagem."""
    print("\n" + "="*60)
    print("DEBUG: Testando serviço de tickets")
    print("="*60)
    
    servico = ServicoTicketDB()
    try:
        print("\n1. Obtendo resumo...")
        resumo = servico.obter_resumo()
        print(f"   Total: {resumo.get('total', 'N/A')}")
        print(f"   Abertos: {resumo.get('abertos', 'N/A')}")
        
        print("\n2. Obtendo top módulos (raw DataFrame)...")
        df_modulos = servico.obter_tickets_abertos()
        if df_modulos is not None and len(df_modulos) > 0:
            print(f"   Shape: {df_modulos.shape}")
            print(f"   Colunas: {df_modulos.columns.tolist()}")
            print(f"   Primeiras 5 linhas:\n{df_modulos.head()}")
            print(f"   Dtypes:\n{df_modulos.dtypes}")
        
        # Tentar agrupar direto
        print("\n3. Agrupando por componente no DataFrame...")
        if df_modulos is not None and 'componente' in df_modulos.columns:
            grouped = df_modulos.groupby('componente').size().sort_values(ascending=False)
            print(grouped.head(10))
        
    finally:
        servico.desconectar()

if __name__ == "__main__":
    print("\n🔍 DIAGNOSTICANDO PROBLEMA DE NaN NO BANCO DE DADOS\n")
    
    try:
        debug_csv_export()
    except Exception as e:
        print(f"\n❌ Erro no debug do CSV: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        debug_servico()
    except Exception as e:
        print(f"\n❌ Erro no debug do serviço: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("Diagnóstico completo")
    print("="*60)
