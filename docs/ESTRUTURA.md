# Documentação da Estrutura do Projeto

## Visão Geral

O projeto AGT 4.0 é organizado em camadas bem definidas para facilitar manutenção, testes e extensão.

## Diretórios Principais

### `/backend/app/`
Código principal da aplicação, dividido em módulos especializados.

#### `/app/services/`
Contém a lógica de negócio principal:
- `ticket_service.py` - Processamento e contagem de tickets
- `analysis_service.py` - Cálculos e análises estatísticas
- `report_service.py` - Geração de relatórios

#### `/app/models/`
Estruturas de dados:
- `ticket.py` - Classe Ticket
- `report.py` - Classe RelatorioAGT40

#### `/app/utils/`
Funções utilitárias:
- `csv_parser.py` - Leitura/escrita de CSV
- `data_validator.py` - Validação de dados
- `formatters.py` - Formatação de saídas

#### `/app/reports/`
Geração de relatórios:
- `/templates/` - Templates HTML/DOCX
- `/output/` - Relatórios gerados

### `/backend/tests/`
Testes unitários e de integração:
- `/test_services/` - Testes dos serviços
- `/test_utils/` - Testes dos utilitários
- `/fixtures/` - Dados para testes

### `/backend/data/`
Gestão de dados:
- `/input/` - Arquivos CSV de entrada
- `/processed/` - Dados processados
- `/historical/` - Dados históricos para comparativos

### `/docs/`
Documentação:
- `/especificacoes/` - Especificações do projeto
- `/exemplos/` - Exemplos de entrada/saída

## Fluxo de Dados

```
CSV de Entrada
    ↓
csv_parser.ler_csv()
    ↓
data_validator.validar_tickets()
    ↓
TicketService.carregar_tickets()
    ↓
AnalysisService.analisar_*()
    ↓
ReportService.gerar_relatorio_*()
    ↓
Relatório (TXT, Excel, HTML, PDF)
```

## Convenções

### Nomenclatura
- Arquivos: `snake_case.py`
- Classes: `PascalCase`
- Funções/Métodos: `snake_case`
- Constantes: `UPPER_SNAKE_CASE`

### Documentação
- Docstrings em português
- Comentários explicativos quando necessário
- Type hints em todas as funções públicas

### Imports
- Imports do stdlib primeiro
- Imports de terceiros depois
- Imports locais por último
- Ordenados alfabeticamente em cada grupo

## Próximos Passos

1. Criar templates de relatório
2. Implementar exportação para Excel/PDF
3. Criar endpoints de API (FastAPI)
4. Adicionar dashboard web
5. Implementar comparativos históricos
