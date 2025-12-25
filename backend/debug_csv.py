"""
Script para debug do CSV e contagem de tickets
"""

import sys
from pathlib import Path
import pandas as pd
import io

# Configurar output UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.jira_parser import parser_jira_csv
from app.config import UPLOADS_DIR

csv_file = UPLOADS_DIR / "upload_20251225_154143_Tickets_JAN-NOV-2025_formatado.csv"

print(f"[FILE] Arquivo: {csv_file}")
print(f"[FILE] Existe: {csv_file.exists()}")
print()

# Contar linhas do CSV
with open(csv_file, 'r', encoding='latin1') as f:
    linhas = f.readlines()
    print(f"[CSV] Total de linhas no arquivo: {len(linhas)}")
    print(f"[CSV] Linhas de dados (sem cabeçalho): {len(linhas) - 1}")
print()

# Verificar com pandas
df = pd.read_csv(csv_file, sep=';', encoding='latin1')
print(f"[PANDAS] Linhas via pandas: {len(df)}")
print(f"[PANDAS] Colunas: {list(df.columns)}")
print()

# Verificar se há linhas vazias ou duplicadas
print(f"[CHECK] Linhas vazias: {df.isnull().all(axis=1).sum()}")
print(f"[CHECK] Linhas duplicadas (completas): {df.duplicated().sum()}")
print()

# Parser original
print("[PARSER] Testando parser_jira_csv...")
tickets = parser_jira_csv(csv_file)
print(f"[PARSER] OK - Tickets carregados: {len(tickets)}")
print()

# Análise de status
status_counts = {}
for t in tickets:
    status = t.status
    status_counts[status] = status_counts.get(status, 0) + 1

print("[STATUS] Contagem por status:")
for status, count in sorted(status_counts.items()):
    print(f"  - {status}: {count}")
print()

# Análise de tipologia
tipologia_counts = {}
for t in tickets:
    tipologia = t.tipologia
    tipologia_counts[tipologia] = tipologia_counts.get(tipologia, 0) + 1

print("[TIPOLOGIA] Contagem por tipologia:")
for tipologia, count in sorted(tipologia_counts.items()):
    print(f"  - {tipologia}: {count}")
print()

# Análise de componente
componente_counts = {}
for t in tickets:
    componente = t.componente
    componente_counts[componente] = componente_counts.get(componente, 0) + 1

print("[COMPONENTE] Contagem por componente (top 10):")
for componente, count in sorted(componente_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  - {componente}: {count}")
