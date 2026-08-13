from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


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
MUTED = colors.HexColor("#545760")
LIGHT = colors.HexColor("#D7D9DF")
PAPER = colors.HexColor("#F7F6F2")

EMAIL = "ridamelkaouiofficial@gmail.com"
PHONE = "+212 620 999 885"
LINKEDIN = "https://www.linkedin.com/in/rida-melkaoui-7bab50256/"
CERTIFICATIONS = LINKEDIN + "details/certifications/"
GITHUB = "https://github.com/RidaMelkaoui"

PROJECT_LINKS = {
    "Demand / Order": GITHUB + "/retail-demand-decision-engine",
    "Route / Control": GITHUB + "/last-mile-route-control-tower",
    "Agent / Proof": GITHUB + "/agent-reliability-lab",
}


def hyperlink(url: str, label: str, color: str = "#123DDB") -> str:
    return f'<link href="{escape(url)}" color="{color}">{escape(label)}</link>'


def make_styles(branded: bool):
    return {
        "body": ParagraphStyle(
            "body", fontName="Arial", fontSize=8.35, leading=11.0,
            textColor=INK, spaceAfter=0,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Arial", fontSize=8.2, leading=10.55,
            textColor=INK, leftIndent=6*mm, bulletIndent=2*mm,
            spaceBefore=0.5*mm, spaceAfter=0,
        ),
        "role": ParagraphStyle(
            "role", fontName="Arial-Bold", fontSize=9.2, leading=10.8,
            textColor=INK, spaceAfter=0,
        ),
        "meta": ParagraphStyle(
            "meta", fontName="Arial-Italic", fontSize=7.35, leading=8.8,
            textColor=MUTED,
        ),
        "right": ParagraphStyle(
            "right", fontName="Arial", fontSize=7.35, leading=8.8,
            textColor=MUTED, alignment=TA_RIGHT,
        ),
        "section": ParagraphStyle(
            "section", fontName="Arial-Bold", fontSize=9.7, leading=11.0,
            textColor=BLUE if branded else INK,
        ),
        "skill_head": ParagraphStyle(
            "skill_head", fontName="Arial-Bold", fontSize=7.4, leading=8.7,
            textColor=BLUE if branded else INK,
        ),
        "skill_body": ParagraphStyle(
            "skill_body", fontName="Arial", fontSize=7.55, leading=9.45,
            textColor=INK,
        ),
        "small": ParagraphStyle(
            "small", fontName="Arial", fontSize=6.7, leading=8.1,
            textColor=MUTED,
        ),
    }


def content_width(branded: bool):
    return 186*mm if branded else 188*mm


def section_heading(text: str, styles, branded: bool, before=3.2*mm):
    width = content_width(branded)
    rule_color = BLUE if branded else INK
    line = Table(
        [[Paragraph(text.upper(), styles["section"]), ""]],
        colWidths=[72*mm, width - 72*mm],
    )
    line.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.7, rule_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.25*mm),
    ]))
    tuned_before = before * (0.68 if branded else 1)
    tuned_after = 1.15*mm if branded else 1.55*mm
    return KeepTogether([Spacer(1, tuned_before), line, Spacer(1, tuned_after)])


def indented_block(flowables, branded: bool, inset=4*mm):
    width = content_width(branded)
    table = Table([["", flowables]], colWidths=[inset, width - inset])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def experience_entry(company, location, role, dates, bullets, styles, branded):
    inner_width = content_width(branded) - 4*mm
    header = Table([
        [Paragraph(escape(company), styles["role"]), Paragraph(escape(location), styles["right"])],
        [Paragraph(escape(role), styles["meta"]), Paragraph(escape(dates), styles["right"])],
    ], colWidths=[inner_width - 45*mm, 45*mm])
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    flowables = [header]
    for bullet in bullets:
        flowables.append(Paragraph(bullet, styles["bullet"], bulletText="•"))
    return indented_block(flowables, branded)


def project_entry(title, label, narrative, styles, branded):
    title_line = (
        f'<b>{hyperlink(PROJECT_LINKS[title], title)}</b> '
        f'<font color="#545760">— {escape(label)}</font>'
    )
    return indented_block([
        Paragraph(title_line, styles["role"]),
        Spacer(1, 0.45*mm),
        Paragraph(narrative, styles["body"]),
    ], branded)


def draw_page(canvas, doc, branded):
    canvas.saveState()
    if branded:
        canvas.setFillColor(BLUE)
        canvas.rect(0, A4[1] - 6*mm, A4[0], 6*mm, stroke=0, fill=1)
        canvas.setFillColor(ORANGE)
        canvas.rect(A4[0] - 7*mm, 0, 7*mm, A4[1], stroke=0, fill=1)
        canvas.setStrokeColor(colors.HexColor("#C8CAD0"))
        canvas.setLineWidth(0.35)
        canvas.line(11*mm, 8*mm, A4[0] - 11*mm, 8*mm)
        canvas.setFont("Arial", 5.7)
        canvas.setFillColor(MUTED)
        canvas.drawString(11*mm, 4.8*mm, "RIDA MELKAOUI / INDUSTRIAL ENGINEER / DATA + AI / BI")
    canvas.restoreState()


def resume_story(branded: bool):
    styles = make_styles(branded)
    width = content_width(branded)
    story = []

    name_style = ParagraphStyle(
        "name", fontName="Arial-Bold", fontSize=20.5 if branded else 18.7,
        leading=21.2, textColor=INK,
    )
    title_style = ParagraphStyle(
        "title", fontName="Arial-Bold", fontSize=9.25, leading=10.8,
        textColor=BLUE,
    )
    contact_style = ParagraphStyle(
        "contact", fontName="Arial", fontSize=6.9, leading=8.45,
        textColor=INK,
    )
    header_left = [
        Paragraph("RIDA MELKAOUI", name_style),
        Paragraph("INDUSTRIAL ENGINEER | DATA, AI & BUSINESS INTELLIGENCE", title_style),
        Spacer(1, 1.8*mm),
        Paragraph(
            f'{hyperlink("mailto:" + EMAIL, EMAIL)}  |  {PHONE}  |  Kenitra, Morocco<br/>'
            f'{hyperlink(LINKEDIN, "LinkedIn")}  |  {hyperlink(GITHUB, "GitHub")}  |  '
            f'{hyperlink("https://ridamelkaoui.github.io/rida-melkaoui-decision-portfolio/", "Portfolio")}',
            contact_style,
        ),
    ]
    if branded:
        portrait = Image(
            str(ROOT / "public" / "images" / "rida-header-cutout.png"),
            width=19*mm, height=25.5*mm, kind="proportional",
        )
        header = Table([[header_left, portrait]], colWidths=[width - 23*mm, 23*mm])
        header.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(header)
    else:
        story.extend(header_left)

    story.append(section_heading("Profile", styles, branded, before=2.6*mm))
    story.append(indented_block([
        Paragraph(
            "Industrial &amp; Production Engineer who combines supplier-quality ownership with data analytics, "
            "BI and applied AI. At Magna, leads electronics and metal supplier quality across international programs "
            "and builds the operating views used to track launch readiness, issues and actions. Translates industrial "
            "problems into measurable decision products with Python, SQL and Power BI.",
            styles["body"],
        )
    ], branded))

    story.append(section_heading("Professional Experience", styles, branded))
    story.append(experience_entry(
        "MAGNA INTERNATIONAL", "Kenitra, Morocco",
        "Supplier Quality Engineer — Electronics & Metal Commodities", "Mar 2026 — Present",
        [
            "Own supplier-quality performance for electronics and metal commodities across China, South Korea, Spain, Slovakia, Germany and Morocco, using launch readiness, 8D/CAPA status and open-issue risk to focus escalation.",
            "Developed X-Rey, a full SQE BI and workflow system covering nomination, Safe Launch and SOP; unified ownership, milestones, PPAP/DVP evidence, critical parts and open issues across <b>6 control modules</b> and <b>4 lifecycle gates</b>.",
            "Implemented KPI views and an automated notification pipeline for missing baselines, overdue actions and gate risks, keeping responsibilities and deadlines visible across the supplier portfolio.",
        ], styles, branded,
    ))
    story.append(Spacer(1, 1.1*mm if branded else 1.55*mm))
    story.append(experience_entry(
        "STELLANTIS R&D", "Casablanca, Morocco",
        "Engineering Intern — Data Analytics, Process Optimization & AI", "Feb 2025 — Aug 2025",
        [
            "Mapped the E-BOM/M-BOM anomaly process and built a Python application plus structured Databricks model for detection, prioritization and traceability; reduced the validated treatment cycle from <b>2 days to under 3 minutes</b> (<b>−98% manual handling</b>, <b>100% project test-case reliability</b>).",
        ], styles, branded,
    ))
    story.append(Spacer(1, 1.1*mm if branded else 1.55*mm))
    story.append(experience_entry(
        "SANY — FORGE DE BAZAS", "Casablanca, Morocco",
        "Engineering Intern — Process Digitalization & Maintenance", "Jul 2024 — Sep 2024",
        [
            "Built a Unity/NLP assistant that structured access to maintenance and spare-parts knowledge, replacing fragmented shop-floor search with a guided information flow.",
        ], styles, branded,
    ))
    story.append(Spacer(1, 1.1*mm if branded else 1.55*mm))
    story.append(experience_entry(
        "3D SMART FACTORY", "Mohammedia, Morocco",
        "Data Analyst Intern", "Aug 2023 — Sep 2023",
        [
            "Structured Power BI and Excel reporting around OEE, FPY, scrap and downtime, giving Lean reviews a single view of production loss drivers and bottlenecks.",
        ], styles, branded,
    ))

    story.append(section_heading("Projects", styles, branded))
    story.append(project_entry(
        "Demand / Order", "Forecasting & replenishment",
        "Created to answer what to replenish and where to review exceptions, this cutoff-safe Python engine models 900 M5 item-store series, challenges forecasts against calibration-selected seasonal baselines and translates the winning signal into inventory-policy scenarios. It improved WAPE by <b>4.5%</b> and simulated <b>1,528 fewer lost units</b> at <b>96.7% fulfilled demand</b> on a 28-day holdout.",
        styles, branded,
    ))
    story.append(Spacer(1, 1.0*mm if branded else 1.35*mm))
    story.append(project_entry(
        "Route / Control", "Optimization & operations",
        "To help dispatchers balance time windows with coherent routes, learned zone-order preferences from 6,112 public histories, combined directed travel times with constrained local search, and surfaced exceptions in a control tower. On a separate 13-route cohort, the policy cut simulated drive time <b>2.8%</b>, kept <b>100% timed-package adherence</b> and removed <b>332 zone re-entries</b>.",
        styles, branded,
    ))
    story.append(Spacer(1, 1.0*mm if branded else 1.35*mm))
    story.append(project_entry(
        "Agent / Proof", "AI evaluation & observability",
        "Built an evaluation lab to decide whether a tool-using AI agent is repeatable enough to release, analyzing 3,336 official trajectories across pass@k, repeatability, cost, latency and failure modes. The pinned GPT-4.1 telecom cohort exposed a <b>14.9-point gap</b> between one-shot and repeatable success.",
        styles, branded,
    ))

    story.append(section_heading("Education", styles, branded))
    education = Table([
        [
            Paragraph("<b>Mohammed VI International Civil Aviation Academy (AIAC)</b><br/>Engineering Degree — Industrial &amp; Production Engineering", styles["body"]),
            Paragraph("Nouaceur, Morocco<br/>2022 — 2025", styles["right"]),
        ],
        [
            Paragraph("<b>Salmane El Farissi Preparatory Classes</b><br/>MPSI — MP", styles["body"]),
            Paragraph("Salé, Morocco<br/>2020 — 2022", styles["right"]),
        ],
    ], colWidths=[width - 42*mm, 42*mm])
    education.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 4*mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.15*mm),
    ]))
    story.append(education)

    story.append(section_heading("Skills", styles, branded))
    skills = [
        ("DATA & ANALYTICS", "Python · SQL · Pandas · NumPy · scikit-learn · statistics · forecasting · experimentation · data modeling · Databricks"),
        ("BI & DELIVERY", "Power BI · DAX · Excel · Power Query · Tableau · React · TypeScript · FastAPI · Git · Docker · KPI systems · automation"),
        ("INDUSTRIAL & QUALITY", "Supplier/process performance · PPM · OEE · FPY · 8D/CAPA · FMEA · root-cause analysis · Lean · launch/SOP governance"),
    ]
    skill_table = Table([[Paragraph(head, styles["skill_head"]), Paragraph(body, styles["skill_body"])] for head, body in skills], colWidths=[40*mm, width - 44*mm])
    skill_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 4*mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.35*mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.85*mm),
    ]))
    story.append(skill_table)

    story.append(section_heading("Languages", styles, branded, before=2.75*mm))
    story.append(indented_block([
        Paragraph("<b>Arabic</b> — Native &nbsp;&nbsp;&nbsp; <b>French</b> — Fluent &nbsp;&nbsp;&nbsp; <b>English</b> — C1 (TOEIC 855; EF SET 62/100)", styles["body"])
    ], branded))

    story.append(section_heading("Certifications", styles, branded, before=2.75*mm))
    cert_table = Table([[
        Paragraph(hyperlink(CERTIFICATIONS, "IBM Data Analyst Professional Certificate") + "<br/><font color='#545760'>IBM / Coursera · 2026</font>", styles["small"]),
        Paragraph(hyperlink(CERTIFICATIONS, "EF SET English Certificate — C1") + "<br/><font color='#545760'>EF SET · 62/100</font>", styles["small"]),
        Paragraph(hyperlink(CERTIFICATIONS, "TOEIC Listening & Reading — C1") + "<br/><font color='#545760'>Score 855</font>", styles["small"]),
    ]], colWidths=[(width - 4*mm)/3]*3)
    cert_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 4*mm),
        ("LEFTPADDING", (1, 0), (-1, 0), 2*mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(cert_table)
    return story


def build(filename: str, branded: bool):
    path = OUT / filename
    doc = BaseDocTemplate(
        str(path), pagesize=A4,
        leftMargin=11*mm,
        rightMargin=13*mm if branded else 11*mm,
        topMargin=7*mm,
        bottomMargin=8*mm if branded else 7*mm,
        title="Rida Melkaoui — Industrial Engineer, Data and AI",
        author="Rida Melkaoui",
        subject="Industrial engineering, data analytics, applied AI and business intelligence resume",
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([
        PageTemplate(id="resume", frames=[frame], onPage=lambda canvas, document: draw_page(canvas, document, branded))
    ])
    doc.build(resume_story(branded))
    return path


ats = build("Rida_Melkaoui_Data_AI_Resume_ATS.pdf", branded=False)
branded = build("Rida_Melkaoui_Data_AI_Resume_Branded.pdf", branded=True)

for source, target in [
    (ats, PUBLIC / "Rida_Melkaoui_Data_AI_Resume.pdf"),
    (branded, PUBLIC / "Rida_Melkaoui_Data_AI_Resume_Branded.pdf"),
]:
    target.write_bytes(source.read_bytes())

print(ats)
print(branded)
