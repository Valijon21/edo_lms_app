"""ReportLab bilan 1-sahifalik Cheat Sheet PDF generatsiya servisi."""
import io


def generate_cheat_sheet_pdf(sheet_data):
    """Cheat sheet ma'lumotlaridan PDF yaratadi.

    Args:
        sheet_data: cheatsheets.py dagi dict (title, subtitle, steps, tips, legal_ref)

    Returns:
        io.BytesIO: PDF fayl buferi
    """
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )

    # Brand ranglari
    INDIGO = colors.HexColor("#4f46e5")
    INDIGO_DARK = colors.HexColor("#312e81")
    INDIGO_LIGHT = colors.HexColor("#e0e7ff")
    WHITE = colors.white
    GRAY_700 = colors.HexColor("#374151")
    GRAY_500 = colors.HexColor("#6b7280")
    AMBER = colors.HexColor("#f59e0b")
    AMBER_LIGHT = colors.HexColor("#fef3c7")

    # Paragraph styles
    STYLE_TITLE = ParagraphStyle(
        "CheatTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        textColor=WHITE,
        leading=22,
        spaceAfter=2 * mm,
    )

    STYLE_SUBTITLE = ParagraphStyle(
        "CheatSubtitle",
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.HexColor("#c7d2fe"),
        leading=13,
    )

    STYLE_STEP_NUM = ParagraphStyle(
        "StepNum",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=INDIGO,
        alignment=1,
    )

    STYLE_STEP_TITLE = ParagraphStyle(
        "StepTitle",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=INDIGO_DARK,
        leading=13,
    )

    STYLE_STEP_DESC = ParagraphStyle(
        "StepDesc",
        fontName="Helvetica",
        fontSize=9,
        textColor=GRAY_700,
        leading=12,
    )

    STYLE_TIP = ParagraphStyle(
        "Tip",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=GRAY_700,
        leading=11,
        leftIndent=3 * mm,
    )

    STYLE_LEGAL = ParagraphStyle(
        "Legal",
        fontName="Helvetica",
        fontSize=7.5,
        textColor=GRAY_500,
        alignment=1,
    )
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=0,
        bottomMargin=10 * mm,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
    )

    elements = []
    page_w = A4[0] - 24 * mm  # usable width

    # ── Header (indigo fon) ──
    header_data = [[
        Paragraph(sheet_data["title"], STYLE_TITLE),
    ]]
    header_table = Table(header_data, colWidths=[page_w])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INDIGO),
        ("TOPPADDING", (0, 0), (-1, -1), 10 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 6 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6 * mm),
        ("ROUNDEDCORNERS", [0, 0, 3 * mm, 3 * mm]),
    ]))
    elements.append(header_table)

    # Subtitle
    sub_data = [[Paragraph(sheet_data["subtitle"], STYLE_SUBTITLE)]]
    sub_table = Table(sub_data, colWidths=[page_w])
    sub_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), INDIGO_DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 6 * mm),
    ]))
    elements.append(sub_table)
    elements.append(Spacer(1, 5 * mm))

    # ── Bosqichlar (Steps) — 2 ustunli grid ──
    steps = sheet_data["steps"]
    step_rows = []
    for i in range(0, len(steps), 2):
        row = []
        for step in steps[i:i + 2]:
            cell_content = [
                [
                    Paragraph(step["number"], STYLE_STEP_NUM),
                    Paragraph(step["title"], STYLE_STEP_TITLE),
                ],
                [
                    "",
                    Paragraph(step["description"], STYLE_STEP_DESC),
                ],
            ]
            cell_table = Table(cell_content, colWidths=[10 * mm, page_w / 2 - 16 * mm])
            cell_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1 * mm),
                ("LEFTPADDING", (0, 0), (-1, -1), 1 * mm),
            ]))
            row.append(cell_table)
        if len(row) == 1:
            row.append("")
        step_rows.append(row)

    col_w = page_w / 2
    steps_grid = Table(step_rows, colWidths=[col_w, col_w])
    steps_grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f9fafb")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 2 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
    ]))
    elements.append(steps_grid)
    elements.append(Spacer(1, 5 * mm))

    # ── Maslahatlar bloki ──
    tip_label = ParagraphStyle(
        "TipLabel",
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=colors.HexColor("#92400e"),
    )
    tip_header = [[Paragraph("💡 Foydali maslahatlar", tip_label)]]
    tips_content = []
    for tip in sheet_data["tips"]:
        tips_content.append([Paragraph(f"• {tip}", STYLE_TIP)])

    all_tip_rows = tip_header + tips_content
    tip_table = Table(all_tip_rows, colWidths=[page_w])
    tip_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER_LIGHT),
        ("TOPPADDING", (0, 0), (0, 0), 3 * mm),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 3 * mm),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, AMBER),
    ]))
    elements.append(tip_table)
    elements.append(Spacer(1, 5 * mm))

    # ── Huquqiy asos (footer) ──
    legal_text = f"Huquqiy asos: {sheet_data['legal_ref']}  |  UNICON SOFT — Ijro.uz o'quv platformasi"
    elements.append(Paragraph(legal_text, STYLE_LEGAL))

    doc.build(elements)
    buf.seek(0)
    return buf
