"""LeafScan AI v4 — Professional PDF Report Generator using ReportLab"""
import os, json
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,TableStyle, HRFlowable, KeepTogether)
from reportlab.platypus import Flowable

W, H = A4

# ── Brand Colors ──────────────────────────────────────────────
GREEN_DARK  = colors.HexColor('#1a4d31')
GREEN_MID   = colors.HexColor('#2d7a4f')
GREEN_LIGHT = colors.HexColor('#4aa369')
GREEN_PALE  = colors.HexColor('#d8f3dc')
GOLD        = colors.HexColor('#c9984a')
GOLD_PALE   = colors.HexColor('#fdf3dc')
RUST        = colors.HexColor('#c0504a')
RUST_PALE   = colors.HexColor('#fde8e8')
AMBER       = colors.HexColor('#d4843a')
CRITICAL    = colors.HexColor('#9b2c2c')
DARK        = colors.HexColor('#1a1a16')
MUTED       = colors.HexColor('#6b6b60')
BORDER      = colors.HexColor('#e4e0d4')
CREAM       = colors.HexColor('#f9f7f2')
WHITE       = colors.white
BLACK       = colors.black


def sev_color(severity):
    s = (severity or '').lower()
    if s == 'none':     return GREEN_LIGHT, GREEN_PALE
    if s == 'moderate': return GOLD, GOLD_PALE
    if s == 'high':     return AMBER, colors.HexColor('#fef0e6')
    if s == 'critical': return CRITICAL, RUST_PALE
    return MUTED, CREAM


class ColoredBar(Flowable):
    """Horizontal colored bar as section divider."""
    def __init__(self, color, width=None, height=3):
        Flowable.__init__(self)
        self.bar_color = color
        self.bar_width = width
        self.bar_height = height

    def draw(self):
        w = self.bar_width or self._width
        self.canv.setFillColor(self.bar_color)
        self.canv.rect(0, 0, w, self.bar_height, stroke=0, fill=1)

    def wrap(self, available_width, available_height):
        self.bar_width = available_width
        self._width = available_width
        return available_width, self.bar_height


def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles['title'] = ParagraphStyle('title',
        fontName='Helvetica-Bold', fontSize=26, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=4, leading=30)

    styles['subtitle'] = ParagraphStyle('subtitle',
        fontName='Helvetica', fontSize=11, textColor=colors.HexColor('#c8e6c9'),
        alignment=TA_CENTER, spaceAfter=2)

    styles['section'] = ParagraphStyle('section',
        fontName='Helvetica-Bold', fontSize=12, textColor=GREEN_DARK,
        spaceBefore=14, spaceAfter=6, leading=15)

    styles['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=DARK,
        spaceAfter=4, leading=14, alignment=TA_JUSTIFY)

    styles['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=9, textColor=DARK,
        leftIndent=14, spaceAfter=3, leading=13,
        bulletIndent=4, bulletFontName='Helvetica-Bold',
        bulletColor=GREEN_LIGHT)

    styles['tip'] = ParagraphStyle('tip',
        fontName='Helvetica-Oblique', fontSize=9.5, textColor=DARK,
        spaceAfter=4, leading=14, leftIndent=4)

    styles['label'] = ParagraphStyle('label',
        fontName='Helvetica-Bold', fontSize=8, textColor=MUTED,
        spaceAfter=1, leading=10, alignment=TA_CENTER)

    styles['value'] = ParagraphStyle('value',
        fontName='Helvetica-Bold', fontSize=14, textColor=DARK,
        spaceAfter=0, leading=16, alignment=TA_CENTER)

    styles['step_num'] = ParagraphStyle('step_num',
        fontName='Helvetica-Bold', fontSize=9, textColor=WHITE,
        alignment=TA_CENTER, leading=11)

    styles['step_text'] = ParagraphStyle('step_text',
        fontName='Helvetica', fontSize=9, textColor=DARK,
        leading=13, spaceAfter=0)

    styles['footer'] = ParagraphStyle('footer',
        fontName='Helvetica', fontSize=8, textColor=MUTED,
        alignment=TA_CENTER)

    styles['disease_name'] = ParagraphStyle('disease_name',
        fontName='Helvetica-Bold', fontSize=18, textColor=DARK,
        spaceAfter=4, leading=22)

    return styles


def generate_pdf_report(result, scan_id=None, language='en'):
    """Generate a beautiful A4 PDF report for a scan result."""
    buf    = BytesIO()
    info   = result.get('disease_info', {})
    sev    = (info.get('severity') or 'Unknown')
    sc, sp = sev_color(sev)
    styles = build_styles()

    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=10*mm, bottomMargin=15*mm)

    story = []
    usable_w = W - 36*mm

    # ── HEADER BANNER ──────────────────────────────────────────
    header_data = [[
        Paragraph('🌿 LeafScan AI', styles['title']),
        Paragraph('Plant Disease Detection Report', styles['subtitle']),
        Paragraph(f'Generated: {datetime.now().strftime("%d %b %Y, %I:%M %p")}', styles['subtitle']),
    ]]
    header_table = Table([[Paragraph('🌿 LeafScan AI — Plant Disease Detection Report', styles['title'])]],
                          colWidths=[usable_w])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN_DARK),
        ('TOPPADDING',    (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,-1), 18),
        ('LEFTPADDING',   (0,0), (-1,-1), 16),
        ('RIGHTPADDING',  (0,0), (-1,-1), 16),
        ('ROUNDEDCORNERS', (0,0), (-1,-1), [8,8,8,8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4))

    # Date / Scan ID row
    meta_items = [
        f'📅 Date: {datetime.now().strftime("%d %B %Y")}',
        f'⏰ Time: {datetime.now().strftime("%H:%M:%S")}',
        f'🔬 Scan ID: #{scan_id or "N/A"}',
        f'🌐 Language: {language.upper()}',
    ]
    meta_table = Table([[Paragraph(m, ParagraphStyle('meta',
        fontName='Helvetica', fontSize=8.5, textColor=MUTED,
        alignment=TA_CENTER)) for m in meta_items]],
        colWidths=[usable_w/4]*4)
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # ── DIAGNOSIS BANNER ───────────────────────────────────────
    emoji_cell = Paragraph(info.get('emoji','🌿'),
        ParagraphStyle('emoji', fontName='Helvetica-Bold', fontSize=32,
                        alignment=TA_CENTER, textColor=DARK))

    diag_cells = [
        [Paragraph('DIAGNOSIS', ParagraphStyle('dlabel', fontName='Helvetica-Bold',
            fontSize=7, textColor=sc, letterSpacing=1.5, leading=9))],
        [Paragraph(result.get('display_name','Unknown'), styles['disease_name'])],
        [Paragraph(f"Type: <b>{info.get('type','—')}</b>  |  Plant: <b>{result.get('class_name','').split('___')[0].replace('_',' ') if '___' in result.get('class_name','') else 'Various'}</b>",
            ParagraphStyle('dtype', fontName='Helvetica', fontSize=9, textColor=MUTED, leading=12))],
    ]

    diag_main = Table(diag_cells, colWidths=[usable_w - 80])
    diag_main.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))

    conf_pct = round(result.get('confidence', 0) * 100)
    conf_cells = [
        [Paragraph('CONFIDENCE', ParagraphStyle('clabel', fontName='Helvetica-Bold',
            fontSize=7, textColor=MUTED, letterSpacing=1, leading=9, alignment=TA_CENTER))],
        [Paragraph(f'{conf_pct}%', ParagraphStyle('cval', fontName='Helvetica-Bold',
            fontSize=22, textColor=GREEN_LIGHT, alignment=TA_CENTER, leading=26))],
        [Paragraph('Model Score', ParagraphStyle('csub', fontName='Helvetica',
            fontSize=7.5, textColor=MUTED, alignment=TA_CENTER, leading=10))],
    ]
    conf_table = Table(conf_cells, colWidths=[68])
    conf_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CREAM),
        ('BOX', (0,0), (-1,-1), 1, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ROUNDEDCORNERS', (0,0), (-1,-1), [6,6,6,6]),
    ]))

    diag_row = Table([[emoji_cell, diag_main, conf_table]],
                     colWidths=[56, usable_w-56-76, 76])
    diag_row.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), sp),
        ('BOX', (0,0), (-1,-1), 1.5, sc),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROUNDEDCORNERS', (0,0), (-1,-1), [8,8,8,8]),
    ]))
    story.append(diag_row)
    story.append(Spacer(1, 8))

    # ── QUICK FACTS ROW ────────────────────────────────────────
    facts = [
        ('SEVERITY', sev, sev_color(sev)[0]),
        ('STATUS',   '✅ Healthy' if result.get('is_healthy') else '⚠️ Diseased', GREEN_LIGHT if result.get('is_healthy') else RUST),
        ('DISEASE TYPE', info.get('type','—'), GREEN_MID),
        ('TOP PREDICTION', result.get('top3',[{}])[0].get('confidence_pct','—'), GOLD),
    ]

    fact_cells = []
    for label, value, color in facts:
        cell = Table([[
            Paragraph(label, ParagraphStyle('fl', fontName='Helvetica-Bold', fontSize=7,
                textColor=MUTED, alignment=TA_CENTER, letterSpacing=0.8, leading=9)),
            Paragraph(value, ParagraphStyle('fv', fontName='Helvetica-Bold', fontSize=11,
                textColor=color, alignment=TA_CENTER, leading=14)),
        ]], colWidths=[usable_w/4 - 4])
        cell.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CREAM),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        fact_cells.append(cell)

    facts_row = Table([fact_cells], colWidths=[(usable_w/4)]*4, spaceBefore=2)
    facts_row.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(facts_row)
    story.append(Spacer(1, 12))

    # ── DESCRIPTION ────────────────────────────────────────────
    story.append(ColoredBar(GREEN_LIGHT))
    story.append(Paragraph('📋 Description', styles['section']))
    story.append(Paragraph(info.get('description','No description available.'), styles['body']))
    story.append(Spacer(1, 8))

    # ── SYMPTOMS ───────────────────────────────────────────────
    symptoms = info.get('symptoms') or []
    if symptoms:
        if isinstance(symptoms, str):
            try: symptoms = json.loads(symptoms)
            except: symptoms = [symptoms]
        story.append(ColoredBar(GOLD))
        story.append(Paragraph('🔍 Symptoms to Watch For', styles['section']))
        for i, s in enumerate(symptoms):
            sym_row = Table([[
                Paragraph(str(i+1), ParagraphStyle('sn', fontName='Helvetica-Bold',
                    fontSize=8, textColor=WHITE, alignment=TA_CENTER, leading=10)),
                Paragraph(str(s), styles['step_text'])
            ]], colWidths=[18, usable_w - 24])
            sym_row.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), GOLD),
                ('BACKGROUND', (1,0), (1,0), GOLD_PALE),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e8d8a0')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (1,0), (1,0), 8),
                ('ROUNDEDCORNERS', (0,0), (-1,-1), [4,4,4,4]),
            ]))
            story.append(sym_row)
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 8))

    # ── TREATMENT ──────────────────────────────────────────────
    treatment = info.get('treatment') or []
    if isinstance(treatment, str):
        try: treatment = json.loads(treatment)
        except: treatment = [treatment]
    if treatment:
        story.append(ColoredBar(GREEN_LIGHT))
        story.append(Paragraph('💊 Treatment Steps', styles['section']))
        for i, t in enumerate(treatment):
            step_row = Table([[
                Paragraph(f'0{i+1}' if i < 9 else str(i+1), styles['step_num']),
                Paragraph(str(t), styles['step_text'])
            ]], colWidths=[22, usable_w - 28])
            step_row.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (0,0), GREEN_MID),
                ('BACKGROUND', (1,0), (1,0), GREEN_PALE),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#a8d5b5')),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 7),
                ('BOTTOMPADDING', (0,0), (-1,-1), 7),
                ('LEFTPADDING', (1,0), (1,0), 10),
                ('ROUNDEDCORNERS', (0,0), (-1,-1), [4,4,4,4]),
            ]))
            story.append(step_row)
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 8))

    # ── PREVENTION ─────────────────────────────────────────────
    prevention = info.get('prevention', '')
    if prevention:
        story.append(ColoredBar(GREEN_DARK))
        story.append(Paragraph('🛡️ Prevention', styles['section']))
        prev_table = Table([[Paragraph(str(prevention), styles['body'])]],
                            colWidths=[usable_w])
        prev_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), GREEN_PALE),
            ('BOX', (0,0), (-1,-1), 1, GREEN_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(prev_table)
        story.append(Spacer(1, 8))

    # ── FARMER TIP ──────────────────────────────────────────────
    farmer_tip = info.get('farmer_tip', '')
    if farmer_tip:
        story.append(ColoredBar(GOLD))
        story.append(Paragraph("🌾 Farmer's Expert Tip", styles['section']))
        tip_table = Table([[Paragraph('💡', ParagraphStyle('ti', fontSize=18, alignment=TA_CENTER)),
                            Paragraph(str(farmer_tip), styles['tip'])]],
                           colWidths=[30, usable_w - 36])
        tip_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), GOLD_PALE),
            ('BOX', (0,0), (-1,-1), 1.5, GOLD),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(tip_table)
        story.append(Spacer(1, 8))

    # ── TOP 3 PREDICTIONS ──────────────────────────────────────
    top3 = result.get('top3', [])
    if isinstance(top3, str):
        try: top3 = json.loads(top3)
        except: top3 = []
    if top3:
        story.append(ColoredBar(MUTED))
        story.append(Paragraph('📊 Model Predictions (Top 3)', styles['section']))
        top3_data = [['Rank', 'Disease Name', 'Confidence', 'Bar']]
        for i, p in enumerate(top3[:3]):
            pct = round(p.get('confidence',0) * 100)
            bar_color = GREEN_LIGHT if i == 0 else (GOLD if i == 1 else MUTED)
            bar_w = int(pct * 0.8)
            top3_data.append([
                str(i+1),
                p.get('name','—'),
                p.get('confidence_pct','—'),
                f"{'█' * (bar_w // 8)}  {pct}%"
            ])
        t3_table = Table(top3_data, colWidths=[20, usable_w-130, 60, 50])
        t3_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
            ('TEXTCOLOR', (0,0), (-1,0), WHITE),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 8),
            ('FONTSIZE', (0,1), (-1,-1), 8.5),
            ('BACKGROUND', (0,1), (-1,1), GREEN_PALE),
            ('ROWBACKGROUNDS', (0,2), (-1,-1), [WHITE, CREAM]),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,-1), 'CENTER'),
            ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ])
        t3_table.setStyle(t3_style)
        story.append(t3_table)
        story.append(Spacer(1, 10))

    # ── DISCLAIMER / FOOTER ────────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER))
    story.append(Spacer(1, 6))
    disclaimer = "⚠️ Disclaimer: This report is generated by LeafScan AI for educational and agricultural guidance purposes only. For critical crop decisions, always consult a qualified agronomist or local agricultural extension officer. Model accuracy ~96% on PlantVillage dataset."
    story.append(Paragraph(disclaimer, styles['footer']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('🌿 LeafScan AI v4.0 | MobileNetV2 + PlantVillage | Powered by TensorFlow',
                            styles['footer']))

    doc.build(story)
    buf.seek(0)
    return buf