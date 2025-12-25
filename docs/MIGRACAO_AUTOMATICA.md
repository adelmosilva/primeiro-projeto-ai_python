# Migração Automática de CSV para PostgreSQL

## Visão Geral

A partir de agora, **toda vez que você faz upload de um CSV no dashboard**, o arquivo é automaticamente sincronizado com o banco de dados PostgreSQL. Não precisa mais executar scripts separados!

## Como Funciona

### Fluxo Automático

```
1. Usuário faz upload de CSV no dashboard
   ↓
2. Arquivo é salvo em /uploads/
   ↓
3. Migração automática é iniciada
   ↓
4. Banco de dados é limpo (remove dados antigos)
   ↓
5. Novos dados são inseridos
   ↓
6. Contagem é verificada e exibida na UI
   ↓
7. Dashboard mostra status da sincronização
```

### Tipos de Upload Suportados

#### 1. **Análise de Período** (Dashboard com Upload)
- Upload único de um CSV
- Sincroniza automaticamente ao banco
- Mostra contagem de tickets

#### 2. **Comparativo de Períodos** (Dois CSVs)
- Upload do período anterior (opcional para análise)
- Upload do período atual (sincroniza automaticamente)
- Compara dados entre os dois períodos

## Componentes

### `backend/auto_migrar.py`
```python
migrar_csv_para_banco(csv_path: Path) -> Tuple[bool, Dict]
```

**Responsabilidades:**
- Lê CSV com encoding automático (latin-1/utf-8)
- Converte datas para formato PostgreSQL
- Conecta via SSH tunnel
- Limpa dados antigos
- Insere novos dados em lotes de 100
- Verifica contagem final

**Tratamento de Erros:**
- Encoding automaticamente detectado
- Datas com formato variável convertidas
- Caracteres especiais escapados
- Conexão SSH reutilizada

### `backend/dashboard.py`
**Modificações:**
- Importa `migrar_csv_para_banco`
- Chama função após salvar arquivo
- Exibe feedback de sincronização na UI
- Trata erros e mostra mensagens

## Mensagens da UI

### Sucesso ✅
```
✅ Banco de dados sincronizado!

- Tickets no CSV: 755
- Tickets no banco: 755
```

### Erro ❌
```
❌ Erro ao sincronizar banco de dados:
[mensagem de erro específica]
```

## Fluxo de Dados

```
CSV Uploadado
    ↓
auto_migrar.py
├─ Lê arquivo
├─ Valida encoding
├─ Converte datas
├─ Conecta SSH
├─ Limpa banco
├─ Insere em lotes
└─ Verifica contagem
    ↓
PostgreSQL
├─ Tabela tickets limpa
└─ 755 novos registros
    ↓
dashboard_db.py
└─ Mostra dados atualizados
```

## Exemplos de Conversão de Dados

### Datas
```
Entrada: "27/11/2025 14:27"
Saída:  "2025-11-27 14:27:00"
```

### Caracteres Especiais
```
Entrada: "José O'Brien's"
Escapado: "José O''Brien''s"
Inserido: INSERT ... VALUES ('José O''Brien''s', ...)
```

### Valores NULL
```
Entrada: campo vazio
Saída:  NULL (sem insert de valor)
```

## Performance

- **Leitura CSV**: ~1-2 segundos
- **Conexão SSH**: ~2-3 segundos
- **Limpeza banco**: ~0.5 segundos
- **Inserção (755 tickets)**: ~5-10 segundos
- **Total**: ~10-15 segundos

Para 755 tickets: ~30-40 mil caracteres SQL gerados

## Sincronização Entre Dashboards

### dashboard.py (Upload CSV)
- Mostra 755 tickets (dados locais)
- Dispara migração automática

### dashboard_db.py (Banco de Dados)
- Mostra 755 tickets (dados de banco)
- Atualiza após migração

**Ambos mostram o mesmo número agora!** ✅

## Tratamento de Erros

Se ocorrer erro na migração:

1. **Encoding Error**: Tenta latin-1 e utf-8 automaticamente
2. **Conexão SSH**: Mostra mensagem de erro de conexão
3. **SQL Error**: Mostra erro específico do PostgreSQL
4. **CSV Inválido**: Retorna erro de parsing

## Fluxo Completo

```python
# 1. Usuário faz upload
with st.file_uploader("CSV", type="csv") as uploaded_file:
    
    # 2. Salva no diretório
    csv_path = UPLOADS_DIR / filename
    csv_path.write_bytes(uploaded_file.getbuffer())
    
    # 3. Migra automaticamente
    sucesso, resultado = migrar_csv_para_banco(csv_path)
    
    # 4. Exibe resultado
    if sucesso:
        st.success(f"Sincronizado: {resultado['total_banco']} tickets")
    else:
        st.error(f"Erro: {resultado['erro']}")
    
    # 5. Continua processamento local
    tickets = parser_jira_csv(csv_path)
    # ... análises ...
```

## Checklist de Funcionalidade

- ✅ Migração automática ao upload
- ✅ Limpeza de dados antigos
- ✅ Conversão de datas
- ✅ Tratamento de encoding
- ✅ Escape de caracteres especiais
- ✅ Inserção em lotes
- ✅ Verificação de contagem
- ✅ Feedback de UI
- ✅ Tratamento de erros
- ✅ Sincronização entre dashboards

## Próximas Melhorias Possíveis

1. **Modo Append**: Adicionar dados sem limpar (em vez de substituir)
2. **Deduplicação**: Validar tickets únicos antes de inserir
3. **Histórico**: Manter versões anteriores dos dados
4. **Backup**: Fazer backup antes de limpar
5. **Agendamento**: Migração automática em horários específicos

---

**Status: ✅ IMPLEMENTADO**

A migração automática está funcionando e pronta para uso.
Sempre que você faz upload de um CSV, o banco é sincronizado automaticamente!
