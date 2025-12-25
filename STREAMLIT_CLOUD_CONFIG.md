# ⚙️ Configuração do Streamlit Cloud

## Problema Atual

No Streamlit Cloud, 3 erros precisam ser resolvidos:

1. **ModuleNotFoundError: No module named 'plotly'** 
   - ✅ RESOLVIDO: Adicionado `plotly>=5.17.0` ao `requirements.txt`

2. **Database indisponível** 
   - Problema: SSH Tunnel para VPS não funciona no Streamlit Cloud
   - Solução: Usar Supabase (já configurado como fallback)

3. **Credenciais do Supabase não encontradas**
   - Problema: Aplicação precisa das credenciais para conectar
   - Solução: Configurar secrets no Streamlit Cloud

---

## ✅ Passo 1: Configurar Secrets no Streamlit Cloud

### Onde adicionar:
1. Acesse sua app no Streamlit Cloud
2. Clique em **"Manage app"** (botão no canto inferior direito)
3. Vá para **"Secrets"** na barra esquerda

### Copie e cole no formulário de Secrets:

```toml
SUPABASE_HOST = "db.nmsarhysujzhpjbpnqtl.supabase.co"
SUPABASE_PORT = 5432
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Dx220304@28010"
SUPABASE_DB = "postgres"
```

### Salve e confirme:
- Clique em **"Save"**
- A aplicação será redeplayed automaticamente (aguarde 3-5 minutos)

---

## 🔍 Como Funciona a Detecção de Ambiente

O arquivo `backend/unified_db_service.py` detecta automaticamente:

```python
IS_CLOUD = 'STREAMLIT' in os.environ or 'streamlit.io' in os.getenv('HOSTNAME', '')
```

- **Se em Cloud** (Streamlit Cloud): Usa Supabase
- **Se em Local**: Usa SSH Tunnel para VPS

---

## 🧪 Testar Conexão

Após configurar os secrets, você pode:

1. Acessar a página **"Teste Conexão"** para verificar se conecta ao Supabase
2. Acessar **"Dashboard DB"** para ver os tickets
3. Acessar **"Dados Banco"** para visualizar dados detalhados

---

## 📊 Versões Plotly

Após configurar os secrets, as seguintes páginas ficarão disponíveis:

- **Dashboard (Plotly)** (`01b_dashboard_plotly.py`): Gráficos interativos com Plotly
- **Dados (Plotly)** (`04b_dados_plotly.py`): Visualizações de dados com Plotly

---

## 🆘 Se Ainda Não Funcionar

### Verificar logs:
1. No Streamlit Cloud, clique em **"Manage app"** → **"Logs"**
2. Procure por:
   - ❌ `ModuleNotFoundError: No module named 'plotly'`
   - ❌ `'SUPABASE_HOST' not found in secrets`
   - ❌ `Cannot assign requested address` (erro de IPv6)

### Soluções Rápidas:
1. **Plotly não instalado**: Confirme que salvou o commit com `requirements.txt` atualizado
2. **Secrets não reconhecidos**: Redeploye a app (clique em redeploy button)
3. **Erro de IPv6**: Já está resolvido com `ipv4_socket_wrapper.py`

---

## 📝 Resumo das Mudanças

```
✅ requirements.txt: Adicionado plotly>=5.17.0, kaleido>=0.2.1
✅ .env: Adicionadas credenciais Supabase (local, backup)
✅ .streamlit/secrets.toml.example: Template para Streamlit Cloud
✅ unified_db_service.py: Detecta Cloud vs Local automaticamente
✅ ipv4_socket_wrapper.py: Força IPv4 globalmente (já ativo)
```

---

## 🚀 Próximas Etapas

1. Configure os secrets no Streamlit Cloud (veja acima)
2. Aguarde o redeploy (3-5 minutos)
3. Teste as páginas
4. Reporte qualquer erro residual
