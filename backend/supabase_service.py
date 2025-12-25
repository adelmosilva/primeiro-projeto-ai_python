"""
Serviço para conectar ao Supabase (PostgreSQL na nuvem)
"""

import os
import pandas as pd
import psycopg2
from psycopg2 import sql
import streamlit as st
from typing import Optional

# Credenciais Supabase
SUPABASE_HOST = "db.nmsarhysujzhpjbpnqtl.supabase.co"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Dx220304@28010"
SUPABASE_DB = "postgres"
SUPABASE_PORT = 5432

class SupabaseTicketService:
    """Serviço para acessar tickets do Supabase"""
    
    def __init__(self):
        self.connection = None
        self._conectar()
    
    def _conectar(self):
        """Conecta ao Supabase PostgreSQL"""
        try:
            # Tentar obter credenciais do Streamlit Cloud Secrets primeiro
            try:
                host = st.secrets.get("SUPABASE_HOST", SUPABASE_HOST)
                user = st.secrets.get("SUPABASE_USER", SUPABASE_USER)
                password = st.secrets.get("SUPABASE_PASSWORD", SUPABASE_PASSWORD)
                database = st.secrets.get("SUPABASE_DB", SUPABASE_DB)
                port = int(st.secrets.get("SUPABASE_PORT", SUPABASE_PORT))
            except:
                # Fallback para variáveis de ambiente ou constantes
                host = os.getenv("SUPABASE_HOST", SUPABASE_HOST)
                port = int(os.getenv("SUPABASE_PORT", SUPABASE_PORT))
                user = os.getenv("SUPABASE_USER", SUPABASE_USER)
                password = os.getenv("SUPABASE_PASSWORD", SUPABASE_PASSWORD)
                database = os.getenv("SUPABASE_DB", SUPABASE_DB)
            
            if not all([host, user, password]):
                raise Exception("Credenciais do Supabase não configuradas")
            
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            print("✅ Conectado ao Supabase!")
            
        except Exception as e:
            print(f"❌ Erro ao conectar ao Supabase: {e}")
            self.connection = None
    
    def _executar_query(self, sql_query: str) -> pd.DataFrame:
        """Executa query SQL e retorna DataFrame"""
        if not self.connection:
            raise Exception("Não conectado ao Supabase")
        
        try:
            df = pd.read_sql_query(sql_query, self.connection)
            return df
        except Exception as e:
            print(f"❌ Erro na query: {e}")
            return pd.DataFrame()
    
    def obter_resumo(self) -> dict:
        """Obtém resumo dos tickets"""
        sql_query = """
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN status != 'Fechado' THEN 1 END) as abertos,
            COUNT(CASE WHEN status = 'Fechado' THEN 1 END) as fechados
        FROM tickets
        """
        df = self._executar_query(sql_query)
        
        if df.empty:
            return {"total": 0, "abertos": 0, "fechados": 0}
        
        return df.iloc[0].to_dict()
    
    def obter_tickets_abertos(self) -> pd.DataFrame:
        """Obtém todos os tickets abertos"""
        sql_query = "SELECT * FROM tickets WHERE status != 'Fechado' ORDER BY data_criacao DESC"
        return self._executar_query(sql_query)
    
    def obter_tickets_por_periodo(self, mes: int, ano: int) -> pd.DataFrame:
        """Obtém tickets de um período específico"""
        sql_query = f"""
        SELECT * FROM tickets 
        WHERE EXTRACT(MONTH FROM data_criacao) = {mes} 
        AND EXTRACT(YEAR FROM data_criacao) = {ano}
        ORDER BY data_criacao DESC
        """
        return self._executar_query(sql_query)
    
    def fechar_conexao(self):
        """Fecha a conexão"""
        if self.connection:
            self.connection.close()
            print("Conexão fechada")

# Singleton para reutilizar conexão
_servico_instance = None

def obter_servico_supabase():
    """Retorna instância única do serviço"""
    global _servico_instance
    if _servico_instance is None:
        _servico_instance = SupabaseTicketService()
    return _servico_instance
