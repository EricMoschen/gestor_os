from __future__ import annotations

from io import BytesIO
from pathlib import Path

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 12 * mm
TOP_MARGIN = PAGE_HEIGHT - (12 * mm)
CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN_X)
LINE_HEIGHT = 6 * mm
FIELD_HEIGHT = 7 * mm
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def _draw_label_value(pdf: canvas.Canvas, label: str, value: str, x: float, y: float) -> None:
    pdf.setFont(FONT_BOLD, 9)
    pdf.drawString(x, y, label)
    label_width = stringWidth(label, FONT_BOLD, 9)
    pdf.setFont(FONT, 9)
    pdf.drawString(x + label_width + 2, y, value or "-")


def _draw_section_title(pdf: canvas.Canvas, title: str, y: float) -> None:
    pdf.setFont(FONT_BOLD, 11)
    pdf.drawString(MARGIN_X, y, title)
    pdf.setStrokeColor(colors.HexColor("#B0B7C3"))
    pdf.line(MARGIN_X, y - 2, MARGIN_X + CONTENT_WIDTH, y - 2)


def _draw_multiline_field(
    pdf: canvas.Canvas,
    *,
    name: str,
    label: str,
    x: float,
    y: float,
    width: float,
    height: float,
    value: str = "",
) -> None:
    pdf.setFont(FONT_BOLD, 10)
    pdf.drawString(x, y + height + 4, label)
    pdf.acroForm.textfield(
        name=name,
        tooltip=label,
        x=x,
        y=y,
        width=width,
        height=height,
        borderStyle="inset",
        borderWidth=1,
        forceBorder=True,
        textColor=colors.black,
        borderColor=colors.HexColor("#4B5563"),
        fillColor=colors.white,
        fontName=FONT,
        fontSize=9,
        value=value,
        fieldFlags="multiline",
    )


def _draw_text_field(
    pdf: canvas.Canvas,
    *,
    name: str,
    label: str,
    x: float,
    y: float,
    width: float,
    value: str = "",
) -> None:
    pdf.setFont(FONT_BOLD, 9)
    pdf.drawString(x, y + FIELD_HEIGHT + 3, label)
    pdf.acroForm.textfield(
        name=name,
        tooltip=label,
        x=x,
        y=y,
        width=width,
        height=FIELD_HEIGHT,
        borderStyle="underlined",
        borderWidth=1,
        forceBorder=True,
        textColor=colors.black,
        borderColor=colors.HexColor("#4B5563"),
        fillColor=colors.white,
        fontName=FONT,
        fontSize=9,
        value=value,
    )


def gerar_pdf_imprimir_os(ordem_servico) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f"Ordem de Serviço {ordem_servico.numero_os}")
    pdf.setAuthor("Gestor OS")
    pdf.setSubject("Ordem de Serviço com campos editáveis")

    logo_path = Path(settings.BASE_DIR) / "abertura_os" / "static" / "img" / "tevere_logo.jpg"
    if logo_path.exists():
        pdf.drawImage(str(logo_path), PAGE_WIDTH - (42 * mm), PAGE_HEIGHT - (26 * mm), width=28 * mm, height=14 * mm, preserveAspectRatio=True, mask="auto")

    current_y = TOP_MARGIN
    pdf.setFont(FONT_BOLD, 16)
    pdf.drawString(MARGIN_X, current_y, f"ORDEM DE SERVIÇO - {ordem_servico.numero_os}")
    current_y -= 10 * mm

    data_abertura = ordem_servico.data_abertura
    cliente = getattr(ordem_servico, "cliente", None)
    centro_custo = getattr(ordem_servico, "centro_custo", None)
    motivo = getattr(ordem_servico, "motivo_intervencao", None)
    username = getattr(ordem_servico, "username", None) or "-"

    left_x = MARGIN_X
    right_x = MARGIN_X + (CONTENT_WIDTH / 2)

    _draw_label_value(pdf, "Nº da Solicitação:", str(ordem_servico.ssm), left_x, current_y)
    _draw_label_value(pdf, "Solicitante:", str(username), right_x, current_y)
    current_y -= LINE_HEIGHT
    _draw_label_value(pdf, "Centro Custo:", str(getattr(centro_custo, "cod_tag", "-")), left_x, current_y)
    _draw_label_value(pdf, "Equipamento:", str(getattr(centro_custo, "descricao", "-")), right_x, current_y)
    current_y -= LINE_HEIGHT
    _draw_label_value(pdf, "Cliente:", str(cliente or "-"), left_x, current_y)
    _draw_label_value(pdf, "Situação:", str(ordem_servico.get_situacao_display()), right_x, current_y)
    current_y -= LINE_HEIGHT
    _draw_label_value(pdf, "Data Solicitação:", data_abertura.strftime("%d/%m/%Y"), left_x, current_y)
    _draw_label_value(pdf, "Hora:", data_abertura.strftime("%H:%M"), right_x, current_y)
    current_y -= LINE_HEIGHT
    _draw_label_value(pdf, "Motivo da Intervenção:", str(motivo or "-"), left_x, current_y)
    current_y -= 10 * mm

    descricao_height = 24 * mm
    _draw_multiline_field(
        pdf,
        name="descricao_solicitacao",
        label="Descrição da Solicitação",
        x=MARGIN_X,
        y=current_y - descricao_height,
        width=CONTENT_WIDTH,
        height=descricao_height,
        value=str(ordem_servico.descricao_os or ""),
    )
    current_y -= descricao_height + 12 * mm

    _draw_multiline_field(
        pdf,
        name="descricao_tecnica_avaria",
        label="Descrição Técnica da Avaria",
        x=MARGIN_X,
        y=current_y - descricao_height,
        width=CONTENT_WIDTH,
        height=descricao_height,
    )
    current_y -= descricao_height + 12 * mm

    _draw_multiline_field(
        pdf,
        name="descricao_intervencao",
        label="Descrição da Intervenção",
        x=MARGIN_X,
        y=current_y - descricao_height,
        width=CONTENT_WIDTH,
        height=descricao_height,
    )
    current_y -= descricao_height + 12 * mm

    _draw_section_title(pdf, "Peças Aplicadas", current_y)
    current_y -= 10 * mm
    half_width = (CONTENT_WIDTH - (6 * mm)) / 2
    _draw_text_field(pdf, name="peca_qtd_1", label="Quantidade", x=MARGIN_X, y=current_y, width=25 * mm)
    _draw_text_field(pdf, name="peca_desc_1", label="Descrição", x=MARGIN_X + 28 * mm, y=current_y, width=half_width - (28 * mm))
    _draw_text_field(pdf, name="peca_qtd_2", label="Quantidade", x=MARGIN_X + half_width + (6 * mm), y=current_y, width=25 * mm)
    _draw_text_field(pdf, name="peca_desc_2", label="Descrição", x=MARGIN_X + half_width + (34 * mm), y=current_y, width=half_width - (28 * mm))
    current_y -= 14 * mm
    _draw_text_field(pdf, name="peca_qtd_3", label="Quantidade", x=MARGIN_X, y=current_y, width=25 * mm)
    _draw_text_field(pdf, name="peca_desc_3", label="Descrição", x=MARGIN_X + 28 * mm, y=current_y, width=half_width - (28 * mm))
    _draw_text_field(pdf, name="peca_qtd_4", label="Quantidade", x=MARGIN_X + half_width + (6 * mm), y=current_y, width=25 * mm)
    _draw_text_field(pdf, name="peca_desc_4", label="Descrição", x=MARGIN_X + half_width + (34 * mm), y=current_y, width=half_width - (28 * mm))
    current_y -= 18 * mm

    field_width = (CONTENT_WIDTH - (8 * mm)) / 3
    _draw_text_field(pdf, name="cod_sintoma", label="Cód. Sintoma", x=MARGIN_X, y=current_y, width=field_width)
    _draw_text_field(pdf, name="cod_causa", label="Cód. Causa", x=MARGIN_X + field_width + (4 * mm), y=current_y, width=field_width)
    _draw_text_field(pdf, name="cod_intervencao", label="Cód. Intervenção", x=MARGIN_X + (2 * field_width) + (8 * mm), y=current_y, width=field_width)
    current_y -= 16 * mm

    quarter_width = (CONTENT_WIDTH - (9 * mm)) / 4
    _draw_text_field(pdf, name="data_inicio", label="Data Início", x=MARGIN_X, y=current_y, width=quarter_width)
    _draw_text_field(pdf, name="hora_inicio", label="Hora Início", x=MARGIN_X + quarter_width + (3 * mm), y=current_y, width=quarter_width)
    _draw_text_field(pdf, name="data_fim", label="Data Fim", x=MARGIN_X + (2 * quarter_width) + (6 * mm), y=current_y, width=quarter_width)
    _draw_text_field(pdf, name="hora_fim", label="Hora Fim", x=MARGIN_X + (3 * quarter_width) + (9 * mm), y=current_y, width=quarter_width)
    current_y -= 16 * mm

    half = (CONTENT_WIDTH - (6 * mm)) / 2
    _draw_text_field(pdf, name="responsavel_execucao", label="Responsável", x=MARGIN_X, y=current_y, width=half)
    _draw_text_field(pdf, name="visto_solicitante", label="Visto Solicitante", x=MARGIN_X + half + (6 * mm), y=current_y, width=half)
    current_y -= 18 * mm

    _draw_multiline_field(
        pdf,
        name="observacoes_execucao",
        label="Observações",
        x=MARGIN_X,
        y=current_y - (20 * mm),
        width=CONTENT_WIDTH,
        height=20 * mm,
        value=str(ordem_servico.observacoes or ""),
    )

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
