# 📊 Dashboard com Plotly - AGT 4.0

## Visão Geral

Adicionamos versões interativas das páginas principais usando **Plotly** em vez de Matplotlib/Streamlit charts.

## Novas Páginas

### 1. **01b_dashboard_plotly.py** 
📊 Dashboard Principal com Plotly

**Localização**: `pages/01b_dashboard_plotly.py`

**Recursos**:
- Gráficos interativos (zoom, pan, hover)
- 3 modos de visualização:
  - 📊 Dashboard Geral (pie charts, bar charts)
  - 📅 Período Específico (temporal analysis)
  - 📈 Comparativo de Meses (side-by-side comparison)
- Métricas em cards coloridos
- Visualizações:
  - Status Distribution (pie)
  - Priority Distribution (bar)
  - Top 10 Components (horizontal bar)
  - Top 10 Servers (horizontal bar)

### 2. **04b_dados_plotly.py**
👀 Dados do Banco com Plotly

**Localização**: `pages/04b_dados_plotly.py`

**Recursos**:
- 4 abas com diferentes visualizações:
  - Tab 1: Resumo Geral + Status Distribution
  - Tab 2: Top 20 Componentes (horizontal bar chart)
  - Tab 3: Top 20 Servidores (horizontal bar chart)
  - Tab 4: Tipologia (Status e Prioridade side-by-side)
- Hover interativo em todos os gráficos
- Tabelas descritivas
- Escalas de cores dinâmicas

## Vantagens do Plotly

✅ **Interatividade Total**
- Zoom, pan, download como PNG
- Hover com detalhes
- Legendas clicáveis

✅ **Responsividade**
- Gráficos se ajustam ao container
- `use_container_width=True` em todos os charts

✅ **Visual Apelativo**
- Cores temáticas
- Animações suaves
- Layout profissional

✅ **Performance**
- Cache de dados
- Renderização eficiente

## Arquivos de Suporte

### `backend/dashboard_db_plotly.py`
- Lógica do dashboard principal
- Todas as funções de gráficos
- Modos de visualização

## Como Usar

### No Streamlit Cloud
1. Navegue até "📊 Dashboard Plotly" (nova página)
2. Selecione o modo na sidebar
3. Interaja com os gráficos:
   - Clique para destacar categorias
   - Hover para ver valores
   - Use toolbar do Plotly (zoom, pan, download)

### Localmente
```bash
streamlit run streamlit_app.py
# Acesse http://localhost:8501/01b_dashboard_plotly
```

## Integração com Banco de Dados

Ambas as páginas usam `unified_db_service.py`, que automaticamente:
- Detecta ambiente (Cloud vs Local)
- Roteia para Supabase (Cloud) ou VPS (Local)
- Retorna dados via mesma interface

## Customização

### Mudar Cores
```python
color_discrete_sequence=px.colors.qualitative.Set2  # ou Set1, Set3, etc
color_continuous_scale="Viridis"  # ou Blues, Reds, Greens
```

### Ajustar Altura dos Gráficos
```python
fig.update_layout(height=500)  # padrão 400
```

### Adicionar Mais Gráficos
```python
import plotly.express as px

fig = px.scatter(df, x='col1', y='col2', color='col3')
st.plotly_chart(fig, use_container_width=True)
```

## Próximas Melhorias

- [ ] Dashboard 02 (Upload) com Plotly
- [ ] Gráficos de série temporal
- [ ] Dashboard 3D para análises complexas
- [ ] Export interativo para PDF com Plotly
- [ ] Dashboards com Dash (alternativa ao Streamlit)

## Versões Disponíveis

| Página | Original | Plotly |
|--------|----------|--------|
| Dashboard | `01_dashboard_db.py` | `01b_dashboard_plotly.py` |
| Dados Banco | `04_dados_banco.py` | `04b_dados_plotly.py` |
| Teste Conexão | `03_teste_conexao.py` | - |
| Status | `05_status.py` | - |
| Upload | `02_dashboard_upload.py` | - |

---

**Criado**: 2025-12-25  
**Versão**: 1.0  
**Status**: ✅ Pronto para produção
