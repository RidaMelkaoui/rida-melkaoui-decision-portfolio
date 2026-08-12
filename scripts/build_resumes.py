from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, Image, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables" / "final-profile"
PUBLIC = ROOT / "public" / "documents"
OUT.mkdir(parents=True, exist_ok=True)
PUBLIC.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", "C:/Windows/Fonts/ariali.ttf"))

BLUE = colors.HexColor("#123DDB")
ORANGE = colors.HexColor("#FF5A1F")
INK = colors.HexColor("#141519")
MUTED = colors.HexColor("#51525A")
LIGHT = colors.HexColor("#E4E4E7")
PAPER = colors.HexColor("#F7F6F2")


def link(url: str, label: str) -> str:
    return f'<link href="{url}" color="#123DDB">{label}</link>'


def styles(branded: bool):
    base = dict(fontName="Arial", textColor=INK, leading=11.45, fontSize=8.9, spaceAfter=0)
    bullet = dict(base)
    bullet["leading"] = 11.2
    return {
        "body": ParagraphStyle("body", **base),
        "bullet": ParagraphStyle("bullet", **bullet, leftIndent=8, firstLineIndent=-7, bulletIndent=0),
        "role": ParagraphStyle("role", fontName="Arial-Bold", fontSize=9.7, leading=11.2, textColor=INK),
        "meta": ParagraphStyle("meta", fontName="Arial-Italic", fontSize=7.95, leading=9.5, textColor=MUTED),
        "section": ParagraphStyle("section", fontName="Arial-Bold", fontSize=9.9, leading=11.2, textColor=BLUE if branded else INK, spaceBefore=6.6, spaceAfter=3.4, uppercase=True),
        "small": ParagraphStyle("small", fontName="Arial", fontSize=7.2, leading=8.7, textColor=MUTED),
        "right": ParagraphStyle("right", fontName="Arial", fontSize=7.95, leading=9.4, textColor=MUTED, alignment=TA_RIGHT),
    }


def section_heading(text: str, s, branded: bool):
    line = Table([[Paragraph(text.upper(), s["section"]), ""]], colWidths=[90*mm, None])
    line.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
        ("LINEBELOW", (0,0), (-1,-1), .65, BLUE if branded else INK),
        ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 1.1),
    ]))
    return line


def entry(company, location, role, dates, bullets, s):
    head = Table([
        [Paragraph(escape(company), s["role"]), Paragraph(escape(location), s["right"])],
        [Paragraph(escape(role), s["meta"]), Paragraph(escape(dates), s["right"])],
    ], colWidths=[122*mm, 56*mm])
    head.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    parts = [head]
    for bullet in bullets:
        parts.append(Paragraph(f"- {bullet}", s["bullet"]))
    return KeepTogether(parts)


def project(title, label, text, s):
    return KeepTogether([
        Paragraph(f'<b>{title}</b> <font color="#51525A">| {label}</font>', s["role"]),
        Paragraph(text, s["body"]),
    ])


def draw_page(canvas, doc, branded):
    canvas.saveState()
    if branded:
        canvas.setFillColor(BLUE); canvas.rect(0, A4[1]-6*mm, A4[0], 6*mm, stroke=0, fill=1)
        canvas.setFillColor(ORANGE); canvas.rect(A4[0]-8*mm, 0, 8*mm, A4[1], stroke=0, fill=1)
        canvas.setStrokeColor(colors.HexColor("#CBCBC8")); canvas.setLineWidth(.35); canvas.line(11*mm, 8*mm, A4[0]-12*mm, 8*mm)
        canvas.setFont("Arial", 5.8); canvas.setFillColor(MUTED); canvas.drawString(11*mm, 4.8*mm, "RIDA MELKAOUI / INDUSTRIAL ENGINEER / DATA + AI / BI")
    canvas.restoreState()


def build(filename: str, branded: bool):
    path = OUT / filename
    margin_right = 13*mm if branded else 10*mm
    doc = BaseDocTemplate(str(path), pagesize=A4, leftMargin=10*mm, rightMargin=margin_right, topMargin=8*mm if branded else 7*mm, bottomMargin=10*mm if branded else 7*mm, title="Rida Melkaoui - Industrial Engineer, Data and AI", author="Rida Melkaoui")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=lambda c,d: draw_page(c,d,branded))])
    s = styles(branded)
    story = []

    name = ParagraphStyle("name", fontName="Arial-Bold", fontSize=21 if branded else 18.5, leading=21, textColor=INK)
    title = ParagraphStyle("title", fontName="Arial-Bold", fontSize=9.2, leading=10.5, textColor=BLUE)
    contact = ParagraphStyle("contact", fontName="Arial", fontSize=6.8, leading=8.2, textColor=INK)
    header_left = [Paragraph("RIDA MELKAOUI", name), Paragraph("INDUSTRIAL ENGINEER | DATA, AI & BUSINESS INTELLIGENCE", title), Spacer(1,1.5*mm), Paragraph(
        f'{link("mailto:ridamelkaouiofficial@gmail.com","ridamelkaouiofficial@gmail.com")}  |  +212 620 999 885  |  Kenitra, Morocco<br/>{link("https://www.linkedin.com/in/rida-melkaoui-7bab50256/","LinkedIn")}  |  {link("https://github.com/RidaMelkaoui","GitHub")}', contact)]
    if branded:
        portrait = Image(str(ROOT / "assets" / "rida_portrait.png"), width=22*mm, height=29*mm, kind="proportional")
        header = Table([[header_left, portrait]], colWidths=[154*mm, 24*mm])
        header.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("ALIGN",(1,0),(1,0),"RIGHT"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
        story.append(header)
    else:
        story.extend(header_left)
    story.append(Spacer(1, 2.1*mm))

    story.append(section_heading("Profile", s, branded))
    story.append(Paragraph("Industrial and Production Engineer combining supplier-quality ownership with data analytics, BI and applied AI. Builds traceable decision systems with Python, SQL, Power BI and statistical/optimization methods - from launch and issue visibility to demand planning, routing and AI-agent reliability.", s["body"]))

    story.append(section_heading("Professional Experience", s, branded))
    story.append(entry("MAGNA INTERNATIONAL", "Kenitra, Morocco", "Supplier Quality Engineer - Electronics & Metal Commodities", "Mar 2026 - Present", [
        "Manage supplier quality across Europe, Asia and Morocco; use performance indicators, launch readiness, 8D/CAPA status and open-issue risk to prioritize action.",
        "Developed an SQE BI system covering nomination through Safe Launch and SOP, consolidating activities, critical-part status, milestones and open issues into one traceable management view.",
        "Built a smart notification pipeline for overdue actions and launch risks, keeping owners and deadlines visible across the project portfolio."
    ], s))
    story.append(Spacer(1, 1.2*mm))
    story.append(entry("STELLANTIS R&D", "Casablanca, Morocco", "Engineering Intern - Data Analytics, Process Optimization & AI", "Feb 2025 - Aug 2025", [
        "Mapped a configuration-anomaly workflow and built a Python application with a structured Databricks data model for detection, prioritization and traceability; reduced treatment time from <b>2 days to 2 minutes</b>."
    ], s))
    story.append(Spacer(1, 1.2*mm))
    story.append(entry("SANY - FORGE DE BAZAS", "Casablanca, Morocco", "Engineering Intern - Process Digitalization & Maintenance", "Jul 2024 - Sep 2024", [
        "Built a Unity/NLP assistant to structure access to maintenance and spare-parts knowledge, reducing fragmented search and improving shop-floor information flow."
    ], s))
    story.append(Spacer(1, 1.2*mm))
    story.append(entry("3D SMART FACTORY", "Mohammedia, Morocco", "Data Analyst Intern", "Aug 2023 - Sep 2023", [
        "Built Power BI and Excel reporting around OEE, FPY, scrap and downtime to expose production bottlenecks for Lean review."
    ], s))

    story.append(section_heading("Selected Decision Systems", s, branded))
    story.append(project("Demand / Order", "Forecasting and replenishment", "Built a cutoff-safe Python decision engine across 900 M5 item-store series; improved WAPE 4.5% vs the strongest calibration-selected seasonal baseline and simulated 1,528 fewer lost units at 96.7% fulfilled demand. " + link("https://github.com/RidaMelkaoui","Evidence"), s))
    story.append(Spacer(1, 1.1*mm))
    story.append(project("Route / Control", "Optimization and operations", "Learned zone sequencing from 6,112 historical routes and built a constrained route policy; on a separate 13-route public cohort, cut simulated drive time 2.8% vs nearest neighbour, maintained 100% timed-package adherence and eliminated 332 zone re-entries. " + link("https://github.com/RidaMelkaoui","Evidence"), s))
    story.append(Spacer(1, 1.1*mm))
    story.append(project("Agent / Proof", "AI evaluation and observability", "Built a reliability lab over 3,336 official historical tool-agent trajectories; implemented Pass1-Pass4, cost, latency and failure diagnostics, exposing a 14.9-point one-shot-to-repeatability loss in the pinned GPT-4.1 telecom cohort. " + link("https://github.com/RidaMelkaoui","Evidence"), s))

    story.append(section_heading("Education", s, branded))
    edu = Table([[Paragraph("<b>Mohammed VI International Civil Aviation Academy (AIAC)</b><br/>Engineering Degree - Industrial & Production Engineering", s["body"]), Paragraph("Nouaceur, Morocco<br/>2022 - 2025", s["right"])],[Paragraph("<b>Salmane El Farissi Preparatory Classes</b><br/>MPSI - MP", s["body"]), Paragraph("Sale, Morocco<br/>2020 - 2022", s["right"])]], colWidths=[140*mm,38*mm])
    edu.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),1.2)])); story.append(edu)

    story.append(section_heading("Skills", s, branded))
    story.append(Paragraph("<b>Data & AI:</b> Python, SQL, Pandas, NumPy, scikit-learn, statistics, forecasting, experimentation, data modeling, data quality, Databricks, Git, Docker.<br/><b>BI & Delivery:</b> Power BI, DAX, Excel, Power Query, Tableau, React, TypeScript, FastAPI, dashboard design, KPI systems, automation, reporting.<br/><b>Industrial & Quality:</b> supplier/process performance, PPM, OEE, FPY, scrap, downtime, 8D/CAPA, FMEA, root-cause analysis, Lean, launch/SOP governance.", s["body"]))

    story.append(section_heading("Languages & Certifications", s, branded))
    story.append(Paragraph(f'<b>Languages:</b> Arabic - Native | French - Fluent | English - C1 (TOEIC 855) &nbsp;&nbsp;&nbsp; <b>Certifications:</b> {link("https://www.linkedin.com/in/rida-melkaoui-7bab50256/details/certifications/","IBM Data Analyst Professional Certificate (2026); EF SET C1; TOEIC 855")}', s["body"]))
    doc.build(story)
    return path


ats = build("Rida_Melkaoui_Data_AI_Resume_ATS.pdf", branded=False)
branded = build("Rida_Melkaoui_Data_AI_Resume_Branded.pdf", branded=True)
for source, target in [(ats, PUBLIC / "Rida_Melkaoui_Data_AI_Resume.pdf"), (branded, PUBLIC / "Rida_Melkaoui_Data_AI_Resume_Branded.pdf")]:
    target.write_bytes(source.read_bytes())
print(ats)
print(branded)
