"""
Serviço de geração de relatórios em PDF
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import tempfile
import os

logger = logging.getLogger(__name__)


class PDFReportService:
    """Serviço responsável pela geração de relatórios em PDF"""
    
    def __init__(self, output_path: Path):
        """
        Inicializa o serviço de PDF
        
        Args:
            output_path: Caminho onde o PDF será salvo
        """
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _gerar_grafico_barras(dados: Dict[str, int], titulo: str, temp_path: str) -> str:
        """
        Gera gráfico de barras
        
        Args:
            dados: Dicionário com dados
            titulo: Título do gráfico
            temp_path: Caminho temporário para salvar
            
        Returns:
            Caminho do arquivo de imagem
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        labels = list(dados.keys())
        values = list(dados.values())
        colors_list = ['#1f4788', '#2e5c8a', '#3d7a9e', '#4c98b2', '#5bb3c8']
        
        ax.bar(labels, values, color=colors_list[:len(labels)])
        ax.set_title(titulo, fontsize=12, fontweight='bold', color='#1f4788')
        ax.set_ylabel('Quantidade', fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        # Adicionar valores nas barras
        for i, v in enumerate(values):
            ax.text(i, v + max(values) * 0.01, str(v), ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(temp_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        return temp_path
    
    @staticmethod
    def _gerar_grafico_barras_horizontal(dados: Dict[str, int], titulo: str, temp_path: str) -> str:
        """
        Gera gráfico de barras horizontais (ideal para muitos itens)
        
        Args:
            dados: Dicionário com dados
            titulo: Título do gráfico
            temp_path: Caminho temporário para salvar
            
        Returns:
            Caminho do arquivo de imagem
        """
        fig, ax = plt.subplots(figsize=(10, max(6, len(dados) * 0.4)))
        
        labels = list(dados.keys())
        values = list(dados.values())
        colors_list = ['#1f4788', '#2e5c8a', '#3d7a9e', '#4c98b2', '#5bb3c8', '#6accd9']
        
        # Gráfico horizontal
        ax.barh(labels, values, color=colors_list[:len(labels)])
        ax.set_title(titulo, fontsize=12, fontweight='bold', color='#1f4788')
        ax.set_xlabel('Quantidade', fontsize=10)
        ax.grid(axis='x', alpha=0.3)
        
        # Adicionar valores nas barras
        for i, v in enumerate(values):
            ax.text(v + max(values) * 0.01, i, str(v), va='center', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(temp_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        return temp_path
    
    @staticmethod
    def _gerar_grafico_pizza(dados: Dict[str, int], titulo: str, temp_path: str) -> str:
        """
        Gera gráfico de pizza
        
        Args:
            dados: Dicionário com dados
            titulo: Título do gráfico
            temp_path: Caminho temporário para salvar
            
        Returns:
            Caminho do arquivo de imagem
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        labels = list(dados.keys())
        values = list(dados.values())
        colors_list = ['#1f4788', '#2e5c8a', '#3d7a9e', '#4c98b2', '#5bb3c8']
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors_list[:len(labels)],
            startangle=90
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(titulo, fontsize=12, fontweight='bold', color='#1f4788')
        
        plt.tight_layout()
        plt.savefig(temp_path, dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        return temp_path
    
    @staticmethod
    def _criar_estilos():
        """Cria estilos personalizados para o relatório"""
        styles = getSampleStyleSheet()
        
        titulo = ParagraphStyle(
            'TituloCustom',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitulo = ParagraphStyle(
            'SubtituloCustom',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2e5c8a'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        secao = ParagraphStyle(
            'SecaoCustom',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        normal = ParagraphStyle(
            'NormalCustom',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=4
        )
        
        return styles, titulo, subtitulo, secao, normal
    
    def gerar_relatorio(
        self,
        periodo: str,
        resumo: Dict[str, Any],
        analises_tipologia: Dict[str, Dict[str, int]],
        analises_componente: Dict[str, Dict[str, int]],
        analises_origem: Dict[str, Dict[str, int]],
        analises_prioridade: Dict[str, Dict[str, int]] = None,
        analises_servidor: Dict[str, Dict[str, int]] = None,
        comparativo: Dict[str, Any] = None,
        resumo_anterior: Dict[str, Any] = None,
        resumo_acumulado: Dict[str, Any] = None,
        top_10_servidores_atual: List[tuple] = None,
        top_10_servidores_acumulado: List[tuple] = None
    ) -> Path:
        """
        Gera relatório em PDF
        
        Args:
            periodo: Período do relatório
            resumo: Resumo executivo
            analises_tipologia: Análise por tipologia
            analises_componente: Análise por componente
            analises_origem: Análise por origem
            analises_prioridade: Análise por prioridade (opcional)
            comparativo: Dados de comparativo (opcional)
            
        Returns:
            Path do arquivo PDF gerado
        """
        
        doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=landscape(A4),
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )
        
        story = []
        styles, titulo, subtitulo, secao, normal = self._criar_estilos()
        
        # Header
        story.append(Paragraph("RELATÓRIO DE MIDDLEWARE E INFRAESTRUTURA", titulo))
        story.append(Paragraph("AGT 4.0", subtitulo))
        story.append(Spacer(1, 0.3*cm))
        
        data_info = f"Período: {periodo} | Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        story.append(Paragraph(data_info, normal))
        story.append(Spacer(1, 0.5*cm))
        
        # Resumo Executivo
        story.append(Paragraph("1. RESUMO EXECUTIVO", secao))
        resumo_data = [
            ['Métrica', 'Quantidade'],
            ['Total de Tickets', str(resumo['total_geral'])],
            ['Tickets Abertos', str(resumo['total_abertos'])],
            ['Tickets Fechados', str(resumo['total_fechados'])],
            ['Backlog Final', str(resumo['backlog_final'])]
        ]
        resumo_table = Table(resumo_data, colWidths=[8*cm, 4*cm])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        story.append(resumo_table)
        story.append(Spacer(1, 0.5*cm))
        
        # Análise por Tipologia
        story.append(Paragraph("2. ANÁLISE POR TIPOLOGIA", secao))
        tipologia_data = [['Tipologia', 'Total', 'Abertos', 'Fechados']]
        for tipo, dados in sorted(analises_tipologia.items()):
            tipologia_data.append([
                tipo,
                str(dados['total']),
                str(dados['abertos']),
                str(dados['fechados'])
            ])
        tipologia_table = Table(tipologia_data, colWidths=[6*cm, 3*cm, 3*cm, 3*cm])
        tipologia_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(tipologia_table)
        story.append(Spacer(1, 0.3*cm))
        
        # Gráfico de tipologia
        grafico_tipo_path = os.path.join(tempfile.gettempdir(), f"grafico_tipologia_{datetime.now().timestamp()}.png")
        self._gerar_grafico_pizza(
            {k: v['total'] for k, v in sorted(analises_tipologia.items())},
            "Distribuição por Tipologia",
            grafico_tipo_path
        )
        story.append(Image(grafico_tipo_path, width=14*cm, height=9*cm))
        story.append(Spacer(1, 0.5*cm))
        
        # Análise por Componente
        story.append(Paragraph("3. ANÁLISE POR COMPONENTE", secao))
        comp_data = [['Componente', 'Total', 'Abertos', 'Fechados']]
        for comp, dados in sorted(analises_componente.items()):
            comp_data.append([
                comp,
                str(dados['total']),
                str(dados['abertos']),
                str(dados['fechados'])
            ])
        comp_table = Table(comp_data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 0.3*cm))
        
        # Gráfico de componentes
        grafico_comp_path = os.path.join(tempfile.gettempdir(), f"grafico_componente_{datetime.now().timestamp()}.png")
        self._gerar_grafico_barras(
            {k: v['total'] for k, v in sorted(analises_componente.items())},
            "Tickets por Componente",
            grafico_comp_path
        )
        story.append(Image(grafico_comp_path, width=14*cm, height=7*cm))
        story.append(Spacer(1, 0.5*cm))
        
        # Análise por Origem
        story.append(Paragraph("4. ANÁLISE POR ORIGEM", secao))
        orig_data = [['Origem', 'Total', 'Abertos', 'Fechados']]
        for orig, dados in sorted(analises_origem.items()):
            orig_data.append([
                orig,
                str(dados['total']),
                str(dados['abertos']),
                str(dados['fechados'])
            ])
        orig_table = Table(orig_data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
        orig_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(orig_table)
        story.append(Spacer(1, 0.3*cm))
        
        # Análise por Servidor/Cluster
        if analises_servidor:
            story.append(Paragraph("5. ANÁLISE POR SERVIDOR/CLUSTER", secao))
            serv_data = [['Servidor/Cluster', 'Total', 'Abertos', 'Fechados']]
            for serv, dados in sorted(analises_servidor.items()):
                serv_data.append([
                    serv,
                    str(dados['total']),
                    str(dados['abertos']),
                    str(dados['fechados'])
                ])
            serv_table = Table(serv_data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
            serv_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(serv_table)
            story.append(Spacer(1, 0.3*cm))
            
            # Gráfico de servidores
            grafico_serv_path = os.path.join(tempfile.gettempdir(), f"grafico_servidor_{datetime.now().timestamp()}.png")
            self._gerar_grafico_barras_horizontal(
                {k: v['total'] for k, v in sorted(analises_servidor.items())},
                "Tickets por Servidor/Cluster",
                grafico_serv_path
            )
            story.append(Image(grafico_serv_path, width=14*cm, height=10*cm))
            story.append(Spacer(1, 0.5*cm))
        
        # Análise por Prioridade se fornecida
        if analises_prioridade:
            story.append(Paragraph("6. ANÁLISE POR PRIORIDADE", secao))
            prio_data = [['Prioridade', 'Total', 'Abertos', 'Fechados']]
            for prio, dados in sorted(analises_prioridade.items()):
                prio_data.append([
                    prio,
                    str(dados['total']),
                    str(dados['abertos']),
                    str(dados['fechados'])
                ])
            prio_table = Table(prio_data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
            prio_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(prio_table)
        
        # Comparativo se fornecido
        if comparativo:
            story.append(PageBreak())
            story.append(Paragraph("7. COMPARATIVO COM PERÍODO ANTERIOR", secao))
            story.append(Spacer(1, 0.3*cm))
            
            comp_data = [
                ['Métrica', f"{comparativo['periodo_anterior']}", f"{comparativo['periodo_atual']}", 'Variação'],
                ['Total de Tickets', 
                 str(comparativo['total_anterior']),
                 str(comparativo['total_atual']),
                 f"{comparativo['variacao_total']:+.0f}"],
                ['Abertos',
                 str(comparativo['abertos_anterior']),
                 str(comparativo['abertos_atual']),
                 f"{comparativo['variacao_abertos']:+.0f}"],
                ['Fechados',
                 str(comparativo['fechados_anterior']),
                 str(comparativo['fechados_atual']),
                 f"{comparativo['variacao_fechados']:+.0f}"],
                ['Backlog',
                 str(comparativo['backlog_anterior']),
                 str(comparativo['backlog_atual']),
                 f"{comparativo['variacao_backlog']:+.0f}"]
            ]
            comp_comp_table = Table(comp_data, colWidths=[6*cm, 4*cm, 4*cm, 4*cm])
            comp_comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(comp_comp_table)
            
            # Resumo Acumulado se fornecido
            if resumo_acumulado:
                story.append(Spacer(1, 0.5*cm))
                story.append(Paragraph("8. RESUMO ACUMULADO", secao))
                story.append(Spacer(1, 0.3*cm))
                
                acum_data = [
                    ['Métrica', 'Acumulado'],
                    ['Total de Tickets', str(resumo_acumulado.get('total_geral', 0))],
                    ['Abertos', str(resumo_acumulado.get('total_abertos', 0))],
                    ['Fechados', str(resumo_acumulado.get('total_fechados', 0))]
                ]
                
                acum_table = Table(acum_data, colWidths=[8*cm, 6*cm])
                acum_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                story.append(acum_table)
            
            # Top 10 Servidores com Mais Tickets Abertos - Período Atual
            if top_10_servidores_atual:
                story.append(Spacer(1, 0.5*cm))
                story.append(Paragraph("9. TOP 10 SERVIDORES/CLUSTERS - PERÍODO ATUAL", secao))
                story.append(Spacer(1, 0.3*cm))
                
                top10_data = [['Servidor/Cluster', 'Tickets Abertos']]
                for servidor, count in top_10_servidores_atual:
                    top10_data.append([str(servidor)[:30], str(count)])
                
                top10_table = Table(top10_data, colWidths=[12*cm, 4*cm])
                top10_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                story.append(top10_table)
            
            # Top 10 Servidores com Mais Tickets Abertos - Acumulado
            if top_10_servidores_acumulado:
                story.append(Spacer(1, 0.5*cm))
                story.append(Paragraph("10. TOP 10 SERVIDORES/CLUSTERS - ACUMULADO", secao))
                story.append(Spacer(1, 0.3*cm))
                
                top10_acum_data = [['Servidor/Cluster', 'Tickets Abertos']]
                for servidor, count in top_10_servidores_acumulado:
                    top10_acum_data.append([str(servidor)[:30], str(count)])
                
                top10_acum_table = Table(top10_acum_data, colWidths=[12*cm, 4*cm])
                top10_acum_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                ]))
                story.append(top10_acum_table)
        
        # Build PDF
        doc.build(story)
        logger.info(f"PDF gerado com sucesso: {self.output_path}")
        
        return self.output_path
