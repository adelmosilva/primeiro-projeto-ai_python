"""
API REST para geração de relatórios - FastAPI
"""

import logging
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil

from app.utils.jira_parser import parser_jira_csv
from app.services.ticket_service import TicketService
from app.services.analysis_service import AnalysisService
from app.services.pdf_report_service import PDFReportService
from app.config import REPORTS_OUTPUT_DIR

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title="AGT 4.0 - API de Relatórios",
    description="API para processamento de tickets e geração de relatórios",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Rota raiz"""
    return {
        "projeto": "AGT 4.0",
        "versao": "1.0.0",
        "descricao": "Sistema de Análise de Tickets e Geração de Relatórios",
        "endpoints": {
            "POST /upload-csv": "Upload de CSV e geração de relatório",
            "POST /upload-comparativo": "Upload de dois CSVs e geração de relatório comparativo",
            "GET /health": "Verificar status da API"
        }
    }


@app.get("/health")
async def health_check():
    """Verificar saúde da API"""
    return {"status": "OK", "servico": "AGT 4.0 API"}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload de CSV e geração de relatório
    
    Args:
        file: Arquivo CSV do Jira
        
    Returns:
        Path do PDF gerado
    """
    try:
        logger.info(f"Recebido arquivo: {file.filename}")
        
        # Salvar temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Processar
        logger.info("Processando arquivo...")
        tickets = parser_jira_csv(tmp_path)
        
        service = TicketService()
        service.carregar_tickets(tickets)
        
        resumo = AnalysisService.calcular_resumo_executivo(tickets)
        analises_tipologia = AnalysisService.analisar_por_tipologia(tickets)
        analises_componente = AnalysisService.analisar_por_componente(tickets)
        analises_origem = AnalysisService.analisar_por_origem(tickets)
        analises_prioridade = AnalysisService.analisar_por_prioridade(tickets)
        analises_servidor = AnalysisService.analisar_por_servidor(tickets)
        
        # Gerar PDF
        periodo = file.filename.split("_")[1] if "_" in file.filename else "Período"
        pdf_path = REPORTS_OUTPUT_DIR / f"relatorio_{file.filename.replace('.csv', '.pdf')}"
        
        logger.info("Gerando PDF...")
        pdf_service = PDFReportService(pdf_path)
        pdf_service.gerar_relatorio(
            periodo=periodo,
            resumo=resumo,
            analises_tipologia=analises_tipologia,
            analises_componente=analises_componente,
            analises_origem=analises_origem,
            analises_prioridade=analises_prioridade,
            analises_servidor=analises_servidor
        )
        
        # Limpar temporário
        tmp_path.unlink()
        
        logger.info(f"PDF gerado: {pdf_path}")
        
        return {
            "status": "sucesso",
            "arquivo": file.filename,
            "total_tickets": len(tickets),
            "resumo": resumo,
            "pdf_path": str(pdf_path),
            "pdf_url": f"/download/{pdf_path.name}"
        }
    
    except Exception as e:
        logger.error(f"Erro: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/upload-comparativo")
async def upload_comparativo(
    arquivo_anterior: UploadFile = File(...),
    arquivo_atual: UploadFile = File(...)
):
    """
    Upload de dois CSVs e geração de relatório comparativo
    
    Args:
        arquivo_anterior: CSV do período anterior
        arquivo_atual: CSV do período atual
        
    Returns:
        Path do PDF comparativo
    """
    try:
        logger.info(f"Recebidos arquivos: {arquivo_anterior.filename}, {arquivo_atual.filename}")
        
        # Salvar temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_ant:
            shutil.copyfileobj(arquivo_anterior.file, tmp_ant)
            tmp_ant_path = Path(tmp_ant.name)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_atu:
            shutil.copyfileobj(arquivo_atual.file, tmp_atu)
            tmp_atu_path = Path(tmp_atu.name)
        
        # Processar período anterior
        logger.info("Processando período anterior...")
        tickets_ant = parser_jira_csv(tmp_ant_path)
        service_ant = TicketService()
        service_ant.carregar_tickets(tickets_ant)
        resumo_ant = AnalysisService.calcular_resumo_executivo(tickets_ant)
        
        # Processar período atual
        logger.info("Processando período atual...")
        tickets_atu = parser_jira_csv(tmp_atu_path)
        service_atu = TicketService()
        service_atu.carregar_tickets(tickets_atu)
        resumo_atu = AnalysisService.calcular_resumo_executivo(tickets_atu)
        analises_tipologia = AnalysisService.analisar_por_tipologia(tickets_atu)
        analises_componente = AnalysisService.analisar_por_componente(tickets_atu)
        analises_origem = AnalysisService.analisar_por_origem(tickets_atu)
        analises_prioridade = AnalysisService.analisar_por_prioridade(tickets_atu)
        analises_servidor = AnalysisService.analisar_por_servidor(tickets_atu)
        
        # Top 10 servidores com tickets abertos
        top_10_servidores_atual = AnalysisService.top_10_servidores_abertos(tickets_atu)
        top_10_servidores_acumulado = AnalysisService.top_10_servidores_abertos(tickets_ant + tickets_atu)
        
        # Resumo acumulado
        resumo_acumulado = AnalysisService.calcular_resumo_acumulado(tickets_ant, tickets_atu)
        
        # Gerar comparativo
        comparativo = {
            'periodo_anterior': arquivo_anterior.filename.split("_")[1] if "_" in arquivo_anterior.filename else "Anterior",
            'periodo_atual': arquivo_atual.filename.split("_")[1] if "_" in arquivo_atual.filename else "Atual",
            'total_anterior': resumo_ant['total_geral'],
            'total_atual': resumo_atu['total_geral'],
            'variacao_total': resumo_atu['total_geral'] - resumo_ant['total_geral'],
            'abertos_anterior': resumo_ant['total_abertos'],
            'abertos_atual': resumo_atu['total_abertos'],
            'variacao_abertos': resumo_atu['total_abertos'] - resumo_ant['total_abertos'],
            'fechados_anterior': resumo_ant['total_fechados'],
            'fechados_atual': resumo_atu['total_fechados'],
            'variacao_fechados': resumo_atu['total_fechados'] - resumo_ant['total_fechados'],
            'backlog_anterior': resumo_ant['backlog_final'],
            'backlog_atual': resumo_atu['backlog_final'],
            'variacao_backlog': resumo_atu['backlog_final'] - resumo_ant['backlog_final'],
            'top_10_servidores_atual': top_10_servidores_atual,
            'top_10_servidores_acumulado': top_10_servidores_acumulado,
            'resumo_acumulado': resumo_acumulado
        }
        
        # Gerar PDF
        pdf_path = REPORTS_OUTPUT_DIR / f"relatorio_comparativo_{comparativo['periodo_anterior']}_vs_{comparativo['periodo_atual']}.pdf"
        
        logger.info("Gerando PDF comparativo...")
        pdf_service = PDFReportService(pdf_path)
        pdf_service.gerar_relatorio(
            periodo=f"{comparativo['periodo_anterior']} vs {comparativo['periodo_atual']}",
            resumo=resumo_atu,
            analises_tipologia=analises_tipologia,
            analises_componente=analises_componente,
            analises_origem=analises_origem,
            analises_prioridade=analises_prioridade,
            analises_servidor=analises_servidor,
            comparativo=comparativo,
            resumo_anterior=resumo_ant,
            resumo_acumulado=resumo_acumulado,
            top_10_servidores_atual=top_10_servidores_atual,
            top_10_servidores_acumulado=top_10_servidores_acumulado
        )
        
        # Limpar temporários
        tmp_ant_path.unlink()
        tmp_atu_path.unlink()
        
        logger.info(f"PDF comparativo gerado: {pdf_path}")
        
        return {
            "status": "sucesso",
            "arquivo_anterior": arquivo_anterior.filename,
            "arquivo_atual": arquivo_atual.filename,
            "tickets_anterior": len(tickets_ant),
            "tickets_atual": len(tickets_atu),
            "comparativo": comparativo,
            "pdf_path": str(pdf_path),
            "pdf_url": f"/download/{pdf_path.name}"
        }
    
    except Exception as e:
        logger.error(f"Erro: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download de arquivo PDF
    
    Args:
        filename: Nome do arquivo
        
    Returns:
        Arquivo PDF
    """
    try:
        file_path = REPORTS_OUTPUT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/pdf"
        )
    
    except Exception as e:
        logger.error(f"Erro ao baixar: {e}")
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
