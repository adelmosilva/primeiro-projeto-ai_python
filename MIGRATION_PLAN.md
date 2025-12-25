# 🚀 Plano de Migração para Supabase (3 Opções)

## Status Atual

✅ **755 tickets prontos para migrar**  
✅ **Credenciais Supabase confirmadas**  
✅ **Scripts de migração criados**  
⚠️ **DNS local não funciona (não é bloqueante)**  

---

## 🎯 3 Opções de Migração

### **OPÇÃO 1: Teste Local Primeiro (Se DNS funcionar)**

```bash
# 1. Testar conexão e senha
python test_password.py

# Se passar:
# 2. Migrar dados
python run_migration.py

# 3. Verificar dados no Supabase
# Ir para: https://app.supabase.com
# Tabela: tickets → Verificar 755 registros
```

**Pré-requisitos:**
- ✅ Credenciais: `Dx220304@28010`
- ✅ Acesso ao VPS via SSH (`vps_key.pem`)
- ⚠️ DNS local funcionar (pode não funcionar em Windows)

**Tempo:** ~5 minutos

---

### **OPÇÃO 2: Migrar via Streamlit Cloud ⭐ RECOMENDADO**

**Motivo:** Streamlit Cloud tem DNS funcional, SSH acesso ao VPS está disponível

#### Passo 1: Preparar Repositório
```bash
git add .
git commit -m "Deploy prep: Supabase integration"
git push origin main
```

#### Passo 2: Configurar Streamlit Cloud Secrets
1. Ir para: https://share.streamlit.io
2. Selecionar seu app
3. **Settings** → **Secrets**
4. Adicionar:
```toml
SUPABASE_HOST = "db.nmsarhysujzhpjbpnqtl.supabase.co"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Dx220304@28010"
SUPABASE_DB = "postgres"
SUPABASE_PORT = 5432
```

#### Passo 3: Executar Migração
1. Acessar seu app no Streamlit Cloud
2. Ir para página: **Migrate Supabase** (nova página 06)
3. Clicar em: **🧪 Testar Supabase**
4. Clicar em: **📋 Criar Tabelas**
5. Clicar em: **🚀 Migrar Dados**
6. Aguardar conclusão (~2 minutos)

#### Passo 4: Verificar Dados
```
https://app.supabase.com → projeto → tickets
Verificar: 755 registros
```

#### Passo 5: Redeployer App
```bash
# Seu código usa unified_db_service.py que detecta automaticamente:
# - Local → VPS via SSH
# - Cloud → Supabase via credenciais

git add .
git commit -m "Enable Supabase for production"
git push origin main
# Streamlit Cloud redeploya automaticamente
```

**Vantagens:**
- ✅ DNS funcional (Streamlit Cloud tem rede boa)
- ✅ Sem necessidade de testes locais
- ✅ Rápido e confiável
- ✅ Tudo em um lugar (app + migração)

**Tempo:** ~10 minutos total

---

### **OPÇÃO 3: Migração Manual SQL**

**Se as duas opções falharem:**

```bash
# 1. Extrair dados do VPS manualmente:
ssh -i vps_key.pem root@91.108.124.150

# No VPS:
docker ps  # Encontrar container postgres
docker exec <container_id> psql -U adelmosilva -d pythonai_db \
  -c "\COPY (SELECT * FROM tickets) TO '/tmp/tickets.csv' WITH CSV HEADER"

# Baixar CSV:
exit  # Sair do SSH
```

```bash
# 2. Inserir dados no Supabase via pgAdmin ou psql:
psql -h db.nmsarhysujzhpjbpnqtl.supabase.co \
     -U postgres \
     -d postgres

# No psql:
\COPY tickets FROM '/path/to/tickets.csv' WITH CSV HEADER
```

**Tempo:** ~15 minutos

---

## 📋 Checklist de Pré-Requisitos

- [x] Credenciais Supabase confirmadas
  - Host: `db.nmsarhysujzhpjbpnqtl.supabase.co`
  - Senha: `Dx220304@28010`
- [x] Acesso ao VPS (`vps_key.pem` existente)
- [x] Scripts criados:
  - `test_password.py` → Testar conexão
  - `run_migration.py` → Executar migração
  - `pages/06_migrate_supabase.py` → Interface web
- [x] Code pronto:
  - `unified_db_service.py` → Auto-detecta local/cloud
  - `supabase_service.py` → Conexão cloud
  - Theme system e CSV validation → Já integrados

---

## 🎬 Recomendação Final

**👉 Use OPÇÃO 2 (Streamlit Cloud)** porque:
1. ✅ DNS funciona lá
2. ✅ Sem precisar testar localmente
3. ✅ Interface web amigável (página 06)
4. ✅ Rápido (~2 min de execução)
5. ✅ Depois o app já está em produção com Supabase

---

## 📊 O Que Vai Acontecer

```
┌─────────────────────────────────────────────┐
│ ANTES: VPS PostgreSQL (local + SSH)         │
│ - Você acessa via SSH tunnel               │
│ - Streamlit Cloud não consegue             │
└─────────────────────────────────────────────┘
                    ↓ MIGRAÇÃO
┌─────────────────────────────────────────────┐
│ DEPOIS: Supabase PostgreSQL Cloud           │
│ - Você acessa via credenciais diretas      │
│ - Streamlit Cloud consegue direto          │
│ - 755 tickets em produção                  │
└─────────────────────────────────────────────┘
```

---

## 🚨 Troubleshooting

### Erro: "Não consegue resolver db.nmsarhysujzhpjbpnqtl.supabase.co"
- **Local:** Use Opção 2 (Streamlit Cloud tem DNS)
- **Cloud:** Não vai acontecer (eles têm DNS bom)

### Erro: "Conexão recusada na porta 5432"
- Verifique se Supabase está online (status.supabase.com)
- Verifique se a senha está certa

### Erro: "SSH key not found"
- Certifique-se de que `vps_key.pem` está em `backend/`
- Verifique permissões: `chmod 600 vps_key.pem`

---

## ✅ Sucesso!

Após a migração, sua app terá:
- ✅ 755 tickets em Supabase
- ✅ Conectando automaticamente (local → VPS, cloud → Supabase)
- ✅ Theme system funcionando
- ✅ CSV upload com auto-migration
- ✅ Comparativo de meses
- ✅ Tudo pronto para produção
