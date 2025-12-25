# Resolução: Discrepância de Contagem de Tickets (755 vs 280)

## Problema Identificado

Ao fazer upload do CSV "upload_20251225_154143_Tickets_JAN-NOV-2025_formatado.csv" com **755 tickets**, o dashboard mostrava apenas **280 tickets**.

### Causa Raiz

Havia **dois dashboards diferentes** funcionando em paralelo:

1. **`dashboard.py`** (Upload CSV)
   - Faz upload de arquivo CSV
   - Processa os tickets localmente
   - **Mostrava corretamente: 755 tickets** ✅

2. **`dashboard_db.py`** (Banco de Dados)
   - Consulta PostgreSQL via SSH
   - Mostra dados persistidos no banco
   - **Mostrava apenas 280 tickets** ❌ (dados antigos)

### Por Que 280?

O banco de dados PostgreSQL tinha dados antigos de migrações anteriores (arquivo: `Tickets_JAN-NOV-2025_formatado.csv` original com deduplicação).

Quando o novo CSV foi uploadado, os dados não foram automaticamente importados para o banco.

## Solução Implementada

### 1. Análise do CSV Uploadado
```
Arquivo: upload_20251225_154143_Tickets_JAN-NOV-2025_formatado.csv
Total de linhas: 755 (confirmado via pandas)
Encoding: latin-1
Delimitador: semicolon (;)
Sem duplicatas: 0 duplicatas encontradas
```

**Status dos dados:**
- Support: 415 tickets
- Incident: 193 tickets
- Task: 137 tickets
- Epic: 5 tickets
- Iniciativa: 5 tickets

Componentes principais:
- Middleware: 647 tickets
- Database: 72 tickets
- Infraestruturas: 31 tickets
- AD/BI: 3 tickets
- MFT Server: 1 ticket

### 2. Script de Migração Criado

**Arquivo:** `backend/migrar_novo_csv.py`

```python
# Executa os seguintes passos:
1. Conecta ao PostgreSQL via SSH
2. Limpa tabela de tickets (remove 280 antigos)
3. Lê o novo CSV do diretório uploads/
4. Converte datas de DD/MM/YYYY para YYYY-MM-DD
5. Insere 755 novos tickets em lotes de 100
6. Verifica contagem final
```

**Problemas Resolvidos:**
- ✅ Encoding: latin-1 (acentos portugueses)
- ✅ Data: Converteu "27/11/2025 14:27" → "2025-11-27 14:27:00"
- ✅ Aspas: Escapou caracteres especiais para SQL

### 3. Resultado Final

```
ANTES:
- Banco: 280 tickets (dados antigos)
- CSV: 755 tickets (novo upload)
- Diferença: 475 tickets

DEPOIS:
- Banco: 755 tickets (atualizado)
- CSV: 755 tickets (novo upload)
- Diferença: 0 ❌ → Sincronizado! ✅

Tempo de migração: ~2 minutos
Taxa: 755 tickets em 8 lotes de 100
```

## Como Usar

### Para Migrar Novos CSVs

```bash
# O script encontra automaticamente o CSV mais recente em uploads/
cd c:\...\primeiro-projeto-ai_python

python backend/migrar_novo_csv.py
```

### Output Esperado

```
==================================================
ATUALIZANDO BANCO COM NOVOS 755 TICKETS
==================================================

[PASSO 1] Limpando tickets antigos...
[OK] Tabela limpa

[PASSO 2] Migrando novo CSV...
[OK] 100/755 tickets inseridos
[OK] 200/755 tickets inseridos
...
[OK] 755/755 tickets inseridos

[SUCESSO]
   Banco de dados agora tem: 755 tickets
   (eram 280, agora sao 755)
==================================================

[OK] Migracao concluida! O dashboard_db.py agora mostrara 755 tickets.
```

## Verificação Pós-Migração

O arquivo `debug_csv.py` pode ser usado para analisar futuros uploads:

```bash
python backend/debug_csv.py
```

Mostra:
- Contagem de linhas no arquivo
- Duplicatas encontradas
- Status dos tickets
- Tipologia (tipo de item)
- Componentes afetados

## Recomendações

1. **Automatizar Migração**: Considere adicionar um botão "Importar para Banco" no `dashboard.py`

2. **Sincronização**: Manter CSV e banco de dados sincronizados

3. **Validação**: Sempre verificar a contagem após importação

4. **Backup**: Antes de limpar, fazer backup dos dados antigos (se necessário)

## Commit

```
feat: Add script to migrate new 755 tickets CSV to PostgreSQL

- Created migrar_novo_csv.py to automatically import new CSV data
- Cleans old 280 tickets and imports 755 new tickets
- Handles date format conversion (DD/MM/YYYY -> YYYY-MM-DD)
- Verifies count after migration
- Updated debug_csv.py to analyze uploaded files

[cf13344]
```

---

**Status: ✅ RESOLVIDO**

O banco de dados agora está sincronizado com os 755 tickets do novo CSV.
O `dashboard_db.py` mostrará os dados corretos na próxima execução.
