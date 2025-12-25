📁 **ESTRUTURA DE DIRETÓRIOS DEFINIDA**

## 📍 Estrutura de Armazenamento

### 📤 Upload de CSVs
- **Diretório**: `./uploads/`
- **Conteúdo**: Arquivos CSV enviados pelos usuários
- **Formato**: `upload_{timestamp}_{nome_arquivo}.csv`
- **Usado por**: dashboard.py, migrar_corrigido.py

### 📊 Relatórios PDF
- **Diretório**: `./relatorios/`
- **Conteúdo**: Relatórios PDF gerados
- **Formato**: `relatorio_{período}_{timestamp}.pdf`
- **Usado por**: dashboard.py (PDFReportService)

---

## 📁 Árvore Completa

```
projeto/
│
├── 📤 uploads/                      # CSVs enviados
│   ├── upload_20250101_120000_jira.csv
│   ├── upload_20250102_150030_jira.csv
│   └── ...
│
├── 📊 relatorios/                   # Relatórios PDF
│   ├── relatorio_Período_Atual_20250101_120000.pdf
│   ├── relatorio_Período_Anterior_20250102_150030.pdf
│   └── ...
│
├── 📁 backend/
│   ├── 📁 data/                     # Dados internos
│   │   ├── input/                   # Dados de entrada
│   │   ├── processed/               # Dados processados
│   │   └── historical/              # Histórico
│   │
│   ├── app/
│   ├── database.py
│   ├── models.py
│   ├── dashboard.py
│   ├── dashboard_db.py
│   └── ...
│
└── ... outros arquivos
```

---

## 🔧 Configuração

### Arquivo: `backend/app/config.py`

```python
# Diretórios de uploads e relatórios (na raiz do projeto)
UPLOADS_DIR = PROJECT_ROOT / "uploads"
RELATORIOS_DIR = PROJECT_ROOT / "relatorios"

# Diretório de outputs de relatórios PDF
REPORTS_OUTPUT_DIR = RELATORIOS_DIR
```

---

## 🚀 Como Usar

### 1️⃣ Inicializar Diretórios
```bash
python criar_diretorios.py
```

### 2️⃣ Fazer Upload de CSV
- Abrir: `streamlit run index.py` → Dashboard com Upload
- Fazer upload de um arquivo CSV
- Arquivo é automaticamente salvo em: `./uploads/upload_{timestamp}_{nome}.csv`

### 3️⃣ Gerar Relatório PDF
- Após processar um CSV
- Clicar em "Gerar PDF com Gráficos"
- PDF é automaticamente salvo em: `./relatorios/relatorio_{período}_{timestamp}.pdf`

### 4️⃣ Migrar CSVs para Banco de Dados
```bash
python backend/migrar_corrigido.py
```
- Procura por CSVs em: `./uploads/`
- Migra para PostgreSQL

---

## 📝 Mudanças Realizadas

✅ **backend/app/config.py**
- Adicionado: `UPLOADS_DIR` e `RELATORIOS_DIR` apontando para raiz
- Atualizado: `REPORTS_OUTPUT_DIR` para usar `RELATORIOS_DIR`

✅ **backend/dashboard.py**
- Importado: `UPLOADS_DIR`
- Alterado: Salvamento de CSV do upload para usar `UPLOADS_DIR`
- Removido: Uso de `tempfile` (antes salvava em temp)
- Adicionado: Mensagem de confirmação do arquivo salvo

✅ **backend/migrar_corrigido.py**
- Importado: `UPLOADS_DIR`
- Alterado: Procura por CSVs em `UPLOADS_DIR` ao invés de hardcoded path

✅ **Criado: criar_diretorios.py**
- Script para inicializar estrutura de diretórios
- Garante que todas as pastas existem

---

## 📌 Resumo

| Objetivo | Diretório | Exemplo |
|----------|-----------|---------|
| Arquivos CSV enviados | `./uploads/` | `upload_20250101_120000_jira.csv` |
| Relatórios PDF gerados | `./relatorios/` | `relatorio_Período_Atual_20250101.pdf` |
| Dados internos | `./backend/data/` | Scripts processam dados aqui |

**Tudo organizado e centralizado!** ✨
