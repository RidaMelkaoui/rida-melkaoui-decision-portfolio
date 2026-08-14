import os
from pathlib import Path
from html import escape
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether,
)

from config import (
    DELIVERABLES_DIR, CANDIDATE_NAME, CANDIDATE_TITLE, CANDIDATE_EMAIL,
    CANDIDATE_PHONE, CANDIDATE_LOCATION, PORTFOLIO_URL, LINKEDIN_URL
)

# Register Standard Fonts
FONT_DIR = Path("C:/Windows/Fonts")
if (FONT_DIR / "arial.ttf").exists():
    pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_DIR / "ariali.ttf")))
    MAIN_FONT = "Arial"
    BOLD_FONT = "Arial-Bold"
    ITALIC_FONT = "Arial-Italic"
else:
    MAIN_FONT = "Helvetica"
    BOLD_FONT = "Helvetica-Bold"
    ITALIC_FONT = "Helvetica-Oblique"

# Color Palette (Deep Navy / Electric Blue / Ice Pale)
INK = colors.HexColor("#111826")
NAVY = colors.HexColor("#071D49")
BLUE = colors.HexColor("#0070AD")
CYAN = colors.HexColor("#12ABDB")
PALE = colors.HexColor("#EAF7FC")
SOFT = colors.HexColor("#F4F7FA")
MUTED = colors.HexColor("#596675")
WHITE = colors.white
BORDER_BLUE = colors.HexColor("#BDE4F4")

def link(url: str, label: str, color: str = "#0070AD") -> str:
    return f'<link href="{escape(url)}" color="{color}">{escape(label)}</link>'

styles = {
    "name": ParagraphStyle("name", fontName=BOLD_FONT, fontSize=19.5, leading=21.5, textColor=WHITE),
    "identity": ParagraphStyle("identity", fontName=MAIN_FONT, fontSize=7.5, leading=10, textColor=colors.HexColor("#C8EAF8"), letterSpacing=0.25),
    "contact": ParagraphStyle("contact", fontName=MAIN_FONT, fontSize=7.2, leading=10.2, textColor=WHITE, alignment=TA_RIGHT),
    "eyebrow": ParagraphStyle("eyebrow", fontName=BOLD_FONT, fontSize=7.5, leading=9, textColor=BLUE, letterSpacing=0.7),
    "title": ParagraphStyle("title", fontName=BOLD_FONT, fontSize=21, leading=23, textColor=NAVY, spaceAfter=3),
    "subtitle": ParagraphStyle("subtitle", fontName=MAIN_FONT, fontSize=9, leading=12, textColor=MUTED),
    "date": ParagraphStyle("date", fontName=MAIN_FONT, fontSize=7.3, leading=9, textColor=MUTED, alignment=TA_RIGHT),
    "salutation": ParagraphStyle("salutation", fontName=BOLD_FONT, fontSize=9.3, leading=12, textColor=INK),
    "body": ParagraphStyle("body", fontName=MAIN_FONT, fontSize=8.6, leading=11.8, textColor=INK, spaceAfter=4.8),
    "lead": ParagraphStyle("lead", fontName=BOLD_FONT, fontSize=11.2, leading=14.0, textColor=NAVY),
    "panel_label": ParagraphStyle("panel_label", fontName=BOLD_FONT, fontSize=6.7, leading=8, textColor=BLUE, letterSpacing=0.6),
    "panel_head": ParagraphStyle("panel_head", fontName=BOLD_FONT, fontSize=8.9, leading=10.5, textColor=NAVY),
    "panel_body": ParagraphStyle("panel_body", fontName=MAIN_FONT, fontSize=7.1, leading=9.4, textColor=INK),
    "proof_metric": ParagraphStyle("proof_metric", fontName=BOLD_FONT, fontSize=13.5, leading=14.5, textColor=BLUE),
    "proof_label": ParagraphStyle("proof_label", fontName=MAIN_FONT, fontSize=6.5, leading=8, textColor=MUTED),
    "footer": ParagraphStyle("footer", fontName=BOLD_FONT, fontSize=6.7, leading=8.5, textColor=BLUE, letterSpacing=0.5),
}

def generate_cover_letter_pdf(
    company_name: str,
    role_title: str,
    location: str = "Casablanca, Morocco",
    recipient_name: str = "Hiring Team",
    work_mode: str = "Hybrid / Remote",
    job_ref: str = ""
) -> str:
    """Generates a professional 1-page Cover Letter PDF customized for the target role."""
    
    clean_company = "".join(c if c.isalnum() else "_" for c in company_name).strip("_")
    company_dir = DELIVERABLES_DIR / clean_company
    company_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = company_dir / f"Rida_Melkaoui_Cover_Letter_{clean_company}.pdf"

    doc = BaseDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=10 * mm,
        bottomMargin=8 * mm,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal", topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    doc.addPageTemplates([PageTemplate(id="OnePage", frames=frame)])

    date_str = datetime.now().strftime("%d %B %Y")
    ref_code = job_ref if job_ref else f"JOB-{clean_company.upper()}-2026"

    # Header block
    head_left = [
        Paragraph(CANDIDATE_NAME, styles["name"]),
        Paragraph(CANDIDATE_TITLE, styles["identity"]),
    ]
    head_right = [
        Paragraph(f"{CANDIDATE_LOCATION}<br/>{CANDIDATE_PHONE}<br/>{CANDIDATE_EMAIL}", styles["contact"]),
        Paragraph(f"{link(PORTFOLIO_URL, 'PORTFOLIO')} | {link(LINKEDIN_URL, 'LINKEDIN')}", styles["contact"]),
    ]
    header_table = Table([[head_left, head_right]], colWidths=[doc.width * 0.65, doc.width * 0.35])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    # Title & Metadata block
    meta_left = [
        Paragraph(f"APPLICATION / REF. {escape(ref_code)}", styles["eyebrow"]),
        Paragraph(escape(role_title), styles["title"]),
        Paragraph(f"{escape(company_name)} &bull; {escape(work_mode)}", styles["subtitle"]),
    ]
    meta_right = [
        Paragraph(f"<strong>{date_str}</strong><br/>{escape(company_name)}<br/>{escape(location)}", styles["date"]),
    ]
    meta_table = Table([[meta_left, meta_right]], colWidths=[doc.width * 0.72, doc.width * 0.28])
    meta_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    # Content paragraphs
    salutation_p = Paragraph(f"Dear {escape(recipient_name)},", styles["salutation"])
    lead_p = Paragraph(
        "The dashboard is not the deliverable. The operating decision is. That is how I work as a Decision Engineer.",
        styles["lead"]
    )
    p1 = Paragraph(
        f"As a Supplier Quality Engineer at <b>Magna International</b>, I operate between global suppliers, quality evidence, and operational risk. I convert fragmented inputs into clear ownership and automated decision views. The SQE BI command center I developed traces activity across 6 control modules and 4 lifecycle gates, highlighting critical components and triggering automated alerts before open issues turn into launch risks.",
        styles["body"]
    )
    p2 = Paragraph(
        f"That experience translates directly to the challenges at <b>{escape(company_name)}</b>: mapping business workflows, structuring KPIs, designing automated exception queues, and providing leadership with defensible operating signals rather than passive reports.",
        styles["body"]
    )

    # 3-Pillar Proof Grid
    p_w = (doc.width - 8 * mm) / 3.0
    c1 = [
        Paragraph("01 / SEE THE OPERATION", styles["panel_label"]),
        Spacer(1, 1.5 * mm),
        Paragraph("Decision-Ready Visibility", styles["panel_head"]),
        Spacer(1, 1 * mm),
        Paragraph("I define OEE, scrap, lead times, and throughput around the decisions they must trigger. At Stellantis R&D, that discipline reduced BOM anomaly cycle times from 2 days to under 3 minutes.", styles["panel_body"]),
    ]
    c2 = [
        Paragraph("02 / CONTROL EXCEPTIONS", styles["panel_label"]),
        Spacer(1, 1.5 * mm),
        Paragraph("Owner, Risk & Next Action", styles["panel_head"]),
        Spacer(1, 1 * mm),
        Paragraph("At Magna, I built an SQE BI and workflow system aligning owners, PPAP/DVP evidence, critical parts, and automated alerts across international supplier programs.", styles["panel_body"]),
    ]
    c3 = [
        Paragraph("03 / VALIDATE & OPERATE", styles["panel_label"]),
        Spacer(1, 1.5 * mm),
        Paragraph("Evidence-Led Solutions", styles["panel_head"]),
        Spacer(1, 1 * mm),
        Paragraph("My portfolio showcases verified models: M5 demand forecasting simulation, last-mile route control towers, and AI-agent reliability diagnostics.", styles["panel_body"]),
    ]

    grid_table = Table([[c1, c2, c3]], colWidths=[p_w, p_w, p_w])
    grid_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    # 4-Metric Bar
    m_w = doc.width / 4.0
    m1 = [Paragraph("&lt; 3 min", styles["proof_metric"]), Paragraph("validated BOM cycle<br/>previously 2 days", styles["proof_label"])]
    m2 = [Paragraph("6 modules", styles["proof_metric"]), Paragraph("SQE control system<br/>nomination to SOP", styles["proof_label"])]
    m3 = [Paragraph("3 systems", styles["proof_metric"]), Paragraph("public portfolio cases<br/>with evidence bounds", styles["proof_label"])]
    m4 = [Paragraph("C1 English", styles["proof_metric"]), Paragraph("TOEIC 855<br/>global collaboration", styles["proof_label"])]

    metric_table = Table([[m1, m2, m3, m4]], colWidths=[m_w, m_w, m_w, m_w])
    metric_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER_BLUE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_BLUE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    closing = Paragraph(
        f"I would welcome a conversation about the operational workflows and decision systems {escape(company_name)} wants to structure next. You can inspect my live decision systems and evidence trails in my portfolio.",
        styles["body"]
    )
    sign = Paragraph("Sincerely,<br/><b>Rida Melkaoui</b>", styles["body"])
    footer_p = Paragraph(f"{link(PORTFOLIO_URL, 'VIEW DECISION PORTFOLIO')} | {escape(company_name).upper()} APPLICATION", styles["footer"])

    story = [
        header_table,
        meta_table,
        Spacer(1, 3 * mm),
        salutation_p,
        Spacer(1, 2 * mm),
        lead_p,
        Spacer(1, 2.5 * mm),
        p1,
        p2,
        Spacer(1, 2 * mm),
        grid_table,
        Spacer(1, 2.5 * mm),
        metric_table,
        Spacer(1, 3 * mm),
        closing,
        Spacer(1, 2 * mm),
        sign,
        Spacer(1, 3 * mm),
        footer_p
    ]

    doc.build(story)
    return str(pdf_path)

if __name__ == "__main__":
    test_pdf = generate_cover_letter_pdf(
        company_name="Capgemini Engineering",
        role_title="Business Analyst Junior / Decision Engineer",
        location="Casablanca, Morocco",
        recipient_name="Capgemini Recruitment Team"
    )
    print("Cover letter generated at:", test_pdf)
