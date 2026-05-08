from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import io
from datetime import datetime


def gerar_autorizacao_pdf(participante):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.5 * cm,
        leftMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm
    )

    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        'Titulo',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a2e'),
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitulo_style = ParagraphStyle(
        'Subtitulo',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#4a4a8a'),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    corpo_style = ParagraphStyle(
        'Corpo',
        parent=styles['Normal'],
        fontSize=11,
        leading=18,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )

    campo_style = ParagraphStyle(
        'Campo',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=8
    )

    data_atual = datetime.now().strftime('%d de %B de %Y').replace(
        'January', 'janeiro').replace('February', 'fevereiro').replace(
        'March', 'março').replace('April', 'abril').replace(
        'May', 'maio').replace('June', 'junho').replace(
        'July', 'julho').replace('August', 'agosto').replace(
        'September', 'setembro').replace('October', 'outubro').replace(
        'November', 'novembro').replace('December', 'dezembro')

    story = []

    story.append(Paragraph("ACAMPAX", titulo_style))
    story.append(Paragraph("Sistema de Inscrições", subtitulo_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#4a4a8a')))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("<b>AUTORIZAÇÃO PARA PARTICIPAÇÃO DE MENOR DE IDADE</b>", ParagraphStyle(
        'TituloDoc',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor('#1a1a2e')
    )))

    story.append(Paragraph(
        f"Eu, <b>{participante.responsavel_nome}</b>, portador(a) do RG <b>{participante.responsavel_rg}</b>, "
        f"telefone <b>{participante.responsavel_telefone or 'não informado'}</b>, na qualidade de "
        f"responsável legal pelo(a) menor:",
        corpo_style
    ))

    dados_menor = [
        ['Nome do Menor:', participante.nome],
        ['Idade:', f'{participante.idade} anos'],
        ['Cidade:', participante.cidade or 'Não informada'],
        ['Telefone:', participante.telefone or 'Não informado'],
    ]

    tabela = Table(dados_menor, colWidths=[5 * cm, 11 * cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f8')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a1a2e')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ccccdd')),
        ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#f8f8fc')]),
    ]))

    story.append(tabela)
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(
        "AUTORIZO a participação do(a) menor acima identificado(a) no evento <b>ACAMPAX</b>, "
        "declarando estar ciente de todas as atividades programadas, normas e regulamentos do evento, "
        "e me responsabilizo legalmente por qualquer ocorrência durante o período de realização.",
        corpo_style
    ))

    story.append(Paragraph(
        "Declaro ainda que li e aceito os Termos de Uso e a Política de Privacidade "
        "(LGPD) do evento, e que as informações fornecidas são verdadeiras.",
        corpo_style
    ))

    story.append(Spacer(1, 1 * cm))

    story.append(Paragraph(f"_______________________________, {data_atual}", ParagraphStyle(
        'Data', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER, spaceAfter=30
    )))

    assinatura_data = [
        ['_' * 40, '_' * 40],
        ['Assinatura do(a) Responsável', 'Assinatura da Organização'],
        [participante.responsavel_nome, 'ACAMPAX'],
    ]

    tabela_ass = Table(assinatura_data, colWidths=[8 * cm, 8 * cm])
    tabela_ass.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#4a4a8a')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
    ]))

    story.append(tabela_ass)
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ccccdd')))

    story.append(Paragraph(
        f"<i>Documento gerado automaticamente pelo sistema Acampax em {datetime.now().strftime('%d/%m/%Y às %H:%M')} "
        f"— ID de inscrição: #{participante.id}</i>",
        ParagraphStyle('Rodape', parent=styles['Normal'], fontSize=8,
                       textColor=colors.grey, alignment=TA_CENTER, spaceBefore=8)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
