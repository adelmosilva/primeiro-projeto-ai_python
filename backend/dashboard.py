"""
Dashboard Streamlit para AGT 4.0
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile
import shutil
from datetime import datetime
import sys
import matplotlib.pyplot as plt

# Adicionar pasta ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.jira_parser import parser_jira_csv
from app.services.ticket_service import TicketService
from app.services.analysis_service import AnalysisService
from app.services.pdf_report_service import PDFReportService
from app.config import REPORTS_OUTPUT_DIR, UPLOADS_DIR

# Configurar página
st.set_page_config(
    page_title="AGT 4.0 - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título
st.title("📊 AGT 4.0 - Sistema de Análise de Tickets")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    opcao = st.radio(
        "Selecione uma opção:",
        ["📈 Análise de Período", "📊 Comparativo de Períodos"]
    )

# Análise de Período Único
if opcao == "📈 Análise de Período":
    st.header("Análise de um Período")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Faça upload do arquivo CSV do Jira",
            type="csv",
            key="single_csv"
        )
    
    with col2:
        periodo = st.text_input("Nome do período:", value="Período Atual")
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processando arquivo..."):
                # Criar diretório se não existir
                UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
                
                # Salvar arquivo no diretório UPLOADS
                csv_filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
                csv_path = UPLOADS_DIR / csv_filename
                
                with open(csv_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.info(f"✅ Arquivo salvo em: `uploads/{csv_filename}`")
                
                # Processar
                tickets = parser_jira_csv(csv_path)
                
                service = TicketService()
                service.carregar_tickets(tickets)
                
                resumo = AnalysisService.calcular_resumo_executivo(tickets)
                analises_tipologia = AnalysisService.analisar_por_tipologia(tickets)
                analises_componente = AnalysisService.analisar_por_componente(tickets)
                analises_origem = AnalysisService.analisar_por_origem(tickets)
                analises_prioridade = AnalysisService.analisar_por_prioridade(tickets)
                analises_servidor = AnalysisService.analisar_por_servidor(tickets)
            
            # Resumo Executivo
            st.subheader("📋 Resumo Executivo")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total de Tickets", resumo['total_geral'])
            with col2:
                st.metric("Abertos", resumo['total_abertos'], delta=resumo['total_abertos'])
            with col3:
                st.metric("Fechados", resumo['total_fechados'], delta=resumo['total_fechados'])
            with col4:
                st.metric("Backlog", resumo['backlog_final'], delta=resumo['backlog_final'])
            
            st.markdown("---")
            
            # Análises
            st.subheader("📊 Análises Detalhadas")
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "Tipologia",
                "Componente",
                "Origem",
                "Prioridade"
            ])
            
            with tab1:
                df_tipologia = pd.DataFrame([
                    {
                        "Tipologia": k,
                        "Total": v["total"],
                        "Abertos": v["abertos"],
                        "Fechados": v["fechados"]
                    }
                    for k, v in analises_tipologia.items()
                ])
                st.dataframe(df_tipologia, use_container_width=True)
            
            with tab2:
                df_componente = pd.DataFrame([
                    {
                        "Componente": k,
                        "Total": v["total"],
                        "Abertos": v["abertos"],
                        "Fechados": v["fechados"]
                    }
                    for k, v in analises_componente.items()
                ])
                st.dataframe(df_componente, use_container_width=True)
            
            with tab3:
                df_origem = pd.DataFrame([
                    {
                        "Origem": k,
                        "Total": v["total"],
                        "Abertos": v["abertos"],
                        "Fechados": v["fechados"]
                    }
                    for k, v in analises_origem.items()
                ])
                st.dataframe(df_origem, use_container_width=True)
            
            with tab4:
                df_prioridade = pd.DataFrame([
                    {
                        "Prioridade": k,
                        "Total": v["total"],
                        "Abertos": v["abertos"],
                        "Fechados": v["fechados"]
                    }
                    for k, v in analises_prioridade.items()
                ])
                st.dataframe(df_prioridade, use_container_width=True)
            
            # Aba adicional para Servidor/Cluster
            with st.expander("🖥️ Análise por Servidor/Cluster"):
                df_servidor = pd.DataFrame([
                    {
                        "Servidor/Cluster": k,
                        "Total": v["total"],
                        "Abertos": v["abertos"],
                        "Fechados": v["fechados"]
                    }
                    for k, v in analises_servidor.items()
                ])
                st.dataframe(df_servidor, use_container_width=True)
                
                # Gráfico de barras horizontais
                fig, ax = plt.subplots(figsize=(10, max(6, len(analises_servidor) * 0.3)))
                df_sorted = df_servidor.sort_values("Total")
                ax.barh(df_sorted["Servidor/Cluster"], df_sorted["Total"], color="#1f4788")
                ax.set_xlabel("Quantidade de Tickets")
                ax.set_title("Tickets por Servidor/Cluster")
                ax.grid(axis='x', alpha=0.3)
                st.pyplot(fig)
            
            st.markdown("---")
            
            # Gerar PDF
            st.subheader("📄 Gerar Relatório")
            
            if st.button("Gerar PDF com Gráficos", use_container_width=True, type="primary"):
                with st.spinner("Gerando PDF..."):
                    REPORTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                    
                    pdf_filename = f"relatorio_{periodo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    pdf_path = REPORTS_OUTPUT_DIR / pdf_filename
                    
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
                    
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Baixar PDF",
                            data=pdf_file,
                            file_name=pdf_filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    st.success(f"✅ PDF gerado: {pdf_filename}")
        
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {e}")

# Comparativo de Períodos
elif opcao == "📊 Comparativo de Períodos":
    st.header("Comparativo Entre Dois Períodos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Período Anterior")
        arquivo_anterior = st.file_uploader(
            "Upload do CSV anterior",
            type="csv",
            key="anterior_csv"
        )
        periodo_anterior = st.text_input("Nome do período anterior:", value="Período Anterior")
    
    with col2:
        st.subheader("📅 Período Atual")
        arquivo_atual = st.file_uploader(
            "Upload do CSV atual",
            type="csv",
            key="atual_csv"
        )
        periodo_atual = st.text_input("Nome do período atual:", value="Período Atual")
    
    if arquivo_anterior is not None and arquivo_atual is not None:
        try:
            with st.spinner("Processando arquivos..."):
                # Criar diretório se não existir
                UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
                
                # Salvar arquivo anterior
                csv_ant_filename = f"upload_anterior_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{arquivo_anterior.name}"
                csv_ant_path = UPLOADS_DIR / csv_ant_filename
                with open(csv_ant_path, "wb") as f:
                    f.write(arquivo_anterior.getbuffer())
                
                # Processar anterior
                tickets_ant = parser_jira_csv(csv_ant_path)
                service_ant = TicketService()
                service_ant.carregar_tickets(tickets_ant)
                resumo_ant = AnalysisService.calcular_resumo_executivo(tickets_ant)
                
                # Salvar arquivo atual
                csv_atu_filename = f"upload_atual_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{arquivo_atual.name}"
                csv_atu_path = UPLOADS_DIR / csv_atu_filename
                with open(csv_atu_path, "wb") as f:
                    f.write(arquivo_atual.getbuffer())
                
                # Processar atual
                tickets_atu = parser_jira_csv(csv_atu_path)
                service_atu = TicketService()
                service_atu.carregar_tickets(tickets_atu)
                resumo_atu = AnalysisService.calcular_resumo_executivo(tickets_atu)
                analises_tipologia = AnalysisService.analisar_por_tipologia(tickets_atu)
                analises_componente = AnalysisService.analisar_por_componente(tickets_atu)
                analises_origem = AnalysisService.analisar_por_origem(tickets_atu)
                analises_prioridade = AnalysisService.analisar_por_prioridade(tickets_atu)
                analises_servidor = AnalysisService.analisar_por_servidor(tickets_atu)
                
                # Análises para Top 10 e Acumulado (por total de tickets)
                top_10_servidores_atual = AnalysisService.top_10_servidores_por_total(tickets_atu)
                top_10_servidores_acumulado = AnalysisService.top_10_servidores_por_total(tickets_ant + tickets_atu)
                resumo_acumulado = AnalysisService.calcular_resumo_acumulado(tickets_ant, tickets_atu)
                
                # Tabelas detalhadas para relatório
                tabela_tipologia = AnalysisService.tabela_tipologia(tickets_ant, tickets_atu)
                tabela_top10_modulos = AnalysisService.tabela_top10_modulos(tickets_ant, tickets_atu)
                tabela_origem = AnalysisService.tabela_origem(tickets_ant, tickets_atu)
                tmp_atu_path.unlink()
            
            # Comparativo
            st.subheader("📊 Comparativo")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                delta = resumo_atu['total_geral'] - resumo_ant['total_geral']
                st.metric("Total de Tickets", resumo_atu['total_geral'], delta=delta)
            
            with col2:
                delta = resumo_atu['total_abertos'] - resumo_ant['total_abertos']
                st.metric("Abertos", resumo_atu['total_abertos'], delta=delta)
            
            with col3:
                delta = resumo_atu['total_fechados'] - resumo_ant['total_fechados']
                st.metric("Fechados", resumo_atu['total_fechados'], delta=delta)
            
            with col4:
                delta = resumo_atu['backlog_final'] - resumo_ant['backlog_final']
                st.metric("Backlog", resumo_atu['backlog_final'], delta=delta)
            
            st.markdown("---")
            
            # Tabela Comparativa
            st.subheader("📋 Análise Comparativa")
            
            df_comparativo = pd.DataFrame({
                "Métrica": ["Total", "Abertos", "Fechados", "Backlog"],
                periodo_anterior: [
                    resumo_ant['total_geral'],
                    resumo_ant['total_abertos'],
                    resumo_ant['total_fechados'],
                    resumo_ant['backlog_final']
                ],
                periodo_atual: [
                    resumo_atu['total_geral'],
                    resumo_atu['total_abertos'],
                    resumo_atu['total_fechados'],
                    resumo_atu['backlog_final']
                ]
            })
            
            df_comparativo["Variação"] = (
                df_comparativo[periodo_atual] - df_comparativo[periodo_anterior]
            )
            
            st.dataframe(df_comparativo, use_container_width=True)
            
            st.markdown("---")
            
            # Resumo Acumulado
            if resumo_acumulado:
                st.subheader("📈 Resumo Acumulado (Ambos os Períodos)")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Acumulado", resumo_acumulado.get('total_geral', 0))
                
                with col2:
                    st.metric("Abertos Acumulado", resumo_acumulado.get('total_abertos', 0))
                
                with col3:
                    st.metric("Fechados Acumulado", resumo_acumulado.get('total_fechados', 0))
                
                with col4:
                    backlog_acumulado = (resumo_acumulado.get('total_geral', 0) - 
                                       resumo_acumulado.get('total_fechados', 0))
                    st.metric("Backlog Acumulado", backlog_acumulado)
                
                st.markdown("---")
            
            # Top 10 Servidores
            if top_10_servidores_atual or top_10_servidores_acumulado:
                st.subheader("🏢 Top 10 Servidores/Clusters com Mais Tickets Abertos")
                
                # Período Atual
                if top_10_servidores_atual:
                    st.markdown("#### 📊 Período Atual")
                    df_top10_atual = pd.DataFrame(
                        top_10_servidores_atual,
                        columns=["Servidor/Cluster", "Tickets Abertos"]
                    )
                    
                    # Calcular soma dos demais servidores
                    top10_sum = df_top10_atual["Tickets Abertos"].sum()
                    total_abertos_atual = resumo_atu['total_abertos']
                    demais_sum = max(0, total_abertos_atual - top10_sum)
                    
                    # Adicionar linha "Demais servidores"
                    df_demais = pd.DataFrame({
                        "Servidor/Cluster": ["Demais Servidores"],
                        "Tickets Abertos": [demais_sum]
                    })
                    df_top10_atual = pd.concat([df_top10_atual, df_demais], ignore_index=True)
                    
                    # Calcular total geral da tabela
                    total_modulos_atual = df_top10_atual["Tickets Abertos"].sum()
                    
                    df_top10_atual.index = df_top10_atual.index + 1
                    df_top10_atual.index.name = "Posição"
                    
                    # Exibir título com total
                    st.markdown(f"**Total de Tickets por Módulo: {total_modulos_atual}**")
                    
                    # Exibir tabela com destaque
                    st.dataframe(
                        df_top10_atual,
                        use_container_width=True,
                        height=350
                    )
                else:
                    st.info("ℹ️ Nenhum servidor com tickets abertos no período atual")
                
                st.divider()
                
                # Acumulado
                if top_10_servidores_acumulado:
                    st.markdown("#### 📈 Acumulado (Ambos os Períodos)")
                    df_top10_acumulado = pd.DataFrame(
                        top_10_servidores_acumulado,
                        columns=["Servidor/Cluster", "Tickets Abertos"]
                    )
                    
                    # Calcular soma dos demais servidores
                    top10_sum_acum = df_top10_acumulado["Tickets Abertos"].sum()
                    total_abertos_acum = resumo_acumulado['total_abertos']
                    demais_sum_acum = max(0, total_abertos_acum - top10_sum_acum)
                    
                    # Adicionar linha "Demais servidores"
                    df_demais_acum = pd.DataFrame({
                        "Servidor/Cluster": ["Demais Servidores"],
                        "Tickets Abertos": [demais_sum_acum]
                    })
                    df_top10_acumulado = pd.concat([df_top10_acumulado, df_demais_acum], ignore_index=True)
                    
                    # Calcular total geral da tabela
                    total_modulos_acum = df_top10_acumulado["Tickets Abertos"].sum()
                    
                    df_top10_acumulado.index = df_top10_acumulado.index + 1
                    df_top10_acumulado.index.name = "Posição"
                    
                    # Exibir título com total
                    st.markdown(f"**Total de Tickets por Módulo: {total_modulos_acum}**")
                    
                    # Exibir tabela com destaque
                    st.dataframe(
                        df_top10_acumulado,
                        use_container_width=True,
                        height=350
                    )
                else:
                    st.info("ℹ️ Nenhum servidor com tickets abertos no acumulado")
                
                st.markdown("---")
            
            # Tabelas Detalhadas
            if tabela_tipologia or tabela_top10_modulos or tabela_origem:
                st.subheader("📊 Análises Detalhadas Comparativas")
                
                # Tipologia
                if tabela_tipologia:
                    st.markdown("#### Distribuição por Tipologia")
                    df_tipologia = pd.DataFrame(tabela_tipologia)
                    # Renomear colunas para exibição
                    df_tipologia_display = df_tipologia.copy()
                    df_tipologia_display.columns = ['Tipologia', 'Abertos Ant.', 'Abertos Atu.', 
                                                     'Fechados Ant.', 'Fechados Atu.', 'Total Ant.', 'Total Atu.']
                    st.dataframe(df_tipologia_display, use_container_width=True, hide_index=True)
                
                st.divider()
                
                # Top 10 Módulos
                if tabela_top10_modulos:
                    st.markdown("#### Top 10 Módulos/Servidores (Comparativo)")
                    df_modulos = pd.DataFrame(tabela_top10_modulos)
                    df_modulos_display = df_modulos.copy()
                    df_modulos_display.columns = ['Módulo', 'Abertos Ant.', 'Abertos Atu.', 
                                                   'Fechados Ant.', 'Fechados Atu.']
                    st.dataframe(df_modulos_display, use_container_width=True, hide_index=True)
                
                st.divider()
                
                # Origem
                if tabela_origem:
                    st.markdown("#### Distribuição por Origem")
                    df_origem = pd.DataFrame(tabela_origem)
                    df_origem_display = df_origem.copy()
                    # Formatar percentuais
                    df_origem_display['percentual_anterior'] = df_origem_display['percentual_anterior'].apply(lambda x: f"{x:.1f}%")
                    df_origem_display['percentual_atual'] = df_origem_display['percentual_atual'].apply(lambda x: f"{x:.1f}%")
                    df_origem_display.columns = ['Origem', 'Abertos Ant.', 'Abertos Atu.', 'Fechados Ant.', 
                                                 'Fechados Atu.', 'Total Ant.', 'Total Atu.', '% Ant.', '% Atu.']
                    st.dataframe(df_origem_display, use_container_width=True, hide_index=True)
                
                st.markdown("---")
            
            st.subheader("📄 Gerar Relatório Comparativo")
            
            if st.button("Gerar PDF Comparativo com Gráficos", use_container_width=True, type="primary"):
                with st.spinner("Gerando PDF comparativo..."):
                    REPORTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                    
                    comparativo = {
                        'periodo_anterior': periodo_anterior,
                        'periodo_atual': periodo_atual,
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
                        'variacao_backlog': resumo_atu['backlog_final'] - resumo_ant['backlog_final']
                    }
                    
                    pdf_filename = f"relatorio_comparativo_{periodo_anterior}_vs_{periodo_atual}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    pdf_path = REPORTS_OUTPUT_DIR / pdf_filename
                    
                    pdf_service = PDFReportService(pdf_path)
                    pdf_service.gerar_relatorio(
                        periodo=f"{periodo_anterior} vs {periodo_atual}",
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
                        top_10_servidores_acumulado=top_10_servidores_acumulado,
                        tabela_tipologia=tabela_tipologia,
                        tabela_top10_modulos=tabela_top10_modulos,
                        tabela_origem=tabela_origem
                    )
                    
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Baixar PDF Comparativo",
                            data=pdf_file,
                            file_name=pdf_filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                    st.success(f"✅ PDF comparativo gerado: {pdf_filename}")
        
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivos: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
    <p>AGT 4.0 - Sistema de Análise de Middleware e Infraestrutura</p>
    <p><small>Desenvolvido com ❤️ usando Streamlit</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
