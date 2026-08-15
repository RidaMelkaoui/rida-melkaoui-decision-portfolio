import smtplib
import imaplib
import email
from email.header import decode_header
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pytz

from config import (
    GMAIL_USER, GMAIL_APP_PASSWORD, CANDIDATE_NAME, CANDIDATE_TITLE,
    CANDIDATE_EMAIL, CANDIDATE_PHONE, PORTFOLIO_URL, LINKEDIN_URL,
    SEND_WINDOW_START_HOUR, SEND_WINDOW_END_HOUR, FOLLOWUP_DAYS,
    get_timezone_for_country, is_blacklisted, PROJECT_ROOT, MASTER_RESUME_PATH, DATA_DIR
)
from database import get_connection

def calculate_next_send_time(target_tz_name: str = "Africa/Casablanca") -> datetime:
    """Calculates the next valid 08:30 AM slot in the recipient's timezone."""
    try:
        tz = pytz.timezone(target_tz_name)
    except Exception:
        tz = pytz.timezone("Africa/Casablanca")
    
    now_in_tz = datetime.now(tz)
    target_slot = now_in_tz.replace(hour=SEND_WINDOW_START_HOUR, minute=30, second=0, microsecond=0)
    
    # If 09:00 AM has already passed today in that timezone, schedule for tomorrow at 08:30 AM
    if now_in_tz.hour >= SEND_WINDOW_END_HOUR:
        target_slot += timedelta(days=1)
    
    # Return as local naive or UTC string for SQLite
    return target_slot.astimezone(pytz.utc).replace(tzinfo=None)

def compose_outreach_email(
    company_name: str,
    contact_name: str,
    salutation: str = "",
    role_title: str = "Decision Engineer / BI & Data Analytics",
    is_french: bool = True
) -> Tuple[str, str]:
    """Composes a high-impact, professional email body tailored to industrial/data decision making."""
    
    greeting = f"Bonjour {salutation} {contact_name}," if is_french and salutation else (
        f"Bonjour {contact_name}," if is_french else f"Dear {contact_name},"
    )

    if is_french:
        subject = f"Candidature / Profil Ingénieur Décision & BI - {CANDIDATE_NAME} - {company_name}"
        body = f"""{greeting}

Je me permets de vous contacter pour vous soumettre ma candidature en tant qu'Ingénieur Décision / Business Intelligence & Data Analytics chez {company_name}.

Ingénieur d'État en Génie Industriel & Production (AIAC) et actuellement Supplier Quality Engineer chez Magna International, je combine l'expertise opérationnelle industrielle avec l'ingénierie de la donnée (Python, SQL, Databricks, Power BI). 

Je ne conçois pas de simples tableaux de bord passifs : je conçois des systèmes d'aide à la décision opérationnels avec files d'exception et suivi automatisé de la performance.

Quelques preuves concrètes de mon travail :
1. Stellantis R&D : Automatisation du flux de traitement des anomalies BOM en Python/Databricks, réduisant le temps de cycle de 2 jours à moins de 3 minutes (-98% de manipulation manuelle).
2. Magna International : Développement d'un centre de commande BI SQE unifiant la gouvernance fournisseurs, les jalons de lancement et les alertes automatisées.
3. Systèmes Décisionnels : M5 Demand Engine (prévision & simulation de politique de stock) et Last-Mile Route Control Tower (optimisation logistique).

Vous pouvez tester et inspecter mes interfaces décisionnelles et démonstrateurs en direct sur mon portfolio :
🔗 {PORTFOLIO_URL}

Vous trouverez ci-joint mon CV actualisé ainsi qu'une lettre de motivation ciblée.

Je serais honoré d'échanger avec vous sur les projets et défis d'ingénierie de données et de performance chez {company_name}.

Bien cordialement,

{CANDIDATE_NAME}
{CANDIDATE_TITLE}
Tél : {CANDIDATE_PHONE}
Email : {CANDIDATE_EMAIL}
LinkedIn : {LINKEDIN_URL}
Portfolio : {PORTFOLIO_URL}
"""
    else:
        subject = f"Application / Decision & Operations BI Engineer - {CANDIDATE_NAME} - {company_name}"
        body = f"""{greeting}

I am reaching out to introduce my profile for Decision Engineering and Operations BI / Data Analytics opportunities at {company_name}.

As an Industrial & Production Engineer (AIAC) currently managing Supplier Quality at Magna International, I bridge operational workflows with data & decision engineering (Python, SQL, Databricks, Power BI).

My operating philosophy: "The dashboard is not the deliverable. The operating decision is." I build end-to-end decision tools with exception queues, risk indicators, and automated action loops.

Key verified accomplishments:
• Stellantis R&D: Python + Databricks BOM anomaly pipeline that reduced processing time from 2 days to <3 minutes.
• Magna International: SQE BI command center tracking launch readiness, milestones, and automated alerts across global programs.
• Live Decision Engines: M5 retail demand forecasting simulation and last-mile route control towers.

You can inspect my interactive decision systems and verified evidence trails here:
🔗 {PORTFOLIO_URL}

Please find attached my tailored resume and cover letter. I would welcome the opportunity to discuss how my background can support {company_name}'s operational and data objectives.

Best regards,

{CANDIDATE_NAME}
{CANDIDATE_TITLE}
Phone: {CANDIDATE_PHONE}
Email: {CANDIDATE_EMAIL}
LinkedIn: {LINKEDIN_URL}
Portfolio: {PORTFOLIO_URL}
"""
    return subject, body

def send_smtp_email(
    to_email: str,
    subject: str,
    body_text: str,
    attachment_paths: List[str] = None
) -> Tuple[bool, str]:
    """Dispatches email with PDF attachments using Gmail SMTP."""
    
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return False, "Gmail credentials not configured in .env"
    
    try:
        msg = MIMEMultipart()
        msg["From"] = f"{CANDIDATE_NAME} <{GMAIL_USER}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body_text, "plain", "utf-8"))

        if attachment_paths:
            for path_str in attachment_paths:
                p = Path(path_str)
                if p.exists():
                    with open(p, "rb") as f:
                        part = MIMEApplication(f.read(), Name=p.name)
                        part["Content-Disposition"] = f'attachment; filename="{p.name}"'
                        msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())

        return True, "Success"
    except Exception as e:
        return False, str(e)

def queue_outreach_for_contact(
    contact_id: int,
    role_title: str = "Decision Engineer / BI & Data Analytics",
    is_french: bool = True
) -> Optional[int]:
    """Generates documents and queues an email for a specific contact."""
    conn = get_connection()
    cur = conn.cursor()
    
    row = cur.execute("""
        SELECT c.id AS contact_id, c.name AS contact_name, c.salutation, c.title AS contact_title, c.email,
               co.name AS company_name, co.country, co.city, co.is_blacklisted
        FROM contacts c
        JOIN companies co ON c.company_id = co.id
        WHERE c.id = ?
    """, (contact_id,)).fetchone()
    
    if not row or row["is_blacklisted"] or is_blacklisted(row["company_name"]):
        conn.close()
        return None

    # Determine timezone and schedule time
    target_tz = get_timezone_for_country(row["country"])
    scheduled_utc = calculate_next_send_time(target_tz)

    # Compose subject & body
    subject, body = compose_outreach_email(
        company_name=row["company_name"],
        contact_name=row["contact_name"],
        salutation=row["salutation"],
        role_title=role_title,
        is_french=is_french
    )

    # Check for tailored cover letter and master resume
    clean_co = "".join(c if c.isalnum() else "_" for c in row["company_name"]).strip("_")
    cl_path = PROJECT_ROOT / "deliverables" / "applications" / clean_co / f"Rida_Melkaoui_Cover_Letter_{clean_co}.pdf"
    
    # Resolve master resume PDF
    master_resume = None
    for cand in [
        MASTER_RESUME_PATH,
        PROJECT_ROOT / "deliverables" / "final-profile" / "Rida_Melkaoui_Data_AI_Resume_ATS.pdf",
        PROJECT_ROOT / "public" / "documents" / "Rida_Melkaoui_Data_AI_Resume.pdf",
        DATA_DIR / "Rida_Melkaoui_Resume.pdf"
    ]:
        if cand and cand.exists():
            master_resume = cand
            break

    attachments = []
    if cl_path.exists():
        attachments.append(str(cl_path))
    if master_resume:
        attachments.append(str(master_resume))

    attachment_str = ",".join(attachments)

    cur.execute("""
        INSERT INTO email_queue (
            contact_id, recipient_email, recipient_name, company_name,
            subject, body_text, attachment_paths, target_timezone, scheduled_time, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (row["contact_id"], row["email"], row["contact_name"], row["company_name"],
          subject, body, attachment_str, target_tz, scheduled_utc.strftime("%Y-%m-%d %H:%M:%S")))
    
    email_id = cur.lastrowid
    conn.commit()
    conn.close()
    return email_id

def process_due_emails(dry_run: bool = False, force: bool = False) -> List[Dict]:
    """Dispatches all emails that have reached their scheduled time slot (or all approved if force=True)."""
    conn = get_connection()
    cur = conn.cursor()
    
    now_utc = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if force:
        due_items = cur.execute("""
            SELECT eq.*, c.status AS contact_status
            FROM email_queue eq
            JOIN contacts c ON eq.contact_id = c.id
            WHERE eq.status = 'approved' AND c.status NOT IN ('replied', 'rejected', 'checked')
        """).fetchall()
    else:
        due_items = cur.execute("""
            SELECT eq.*, c.status AS contact_status
            FROM email_queue eq
            JOIN contacts c ON eq.contact_id = c.id
            WHERE eq.status = 'approved' AND eq.scheduled_time <= ? AND c.status NOT IN ('replied', 'rejected', 'checked')
        """, (now_utc,)).fetchall()

    # Resolve master resume fallback for dispatch
    resolved_master_resume = None
    for cand in [
        MASTER_RESUME_PATH,
        PROJECT_ROOT / "deliverables" / "final-profile" / "Rida_Melkaoui_Data_AI_Resume_ATS.pdf",
        PROJECT_ROOT / "public" / "documents" / "Rida_Melkaoui_Data_AI_Resume.pdf",
        DATA_DIR / "Rida_Melkaoui_Resume.pdf"
    ]:
        if cand and cand.exists():
            resolved_master_resume = cand
            break

    results = []
    for item in due_items:
        attachments = [p for p in item["attachment_paths"].split(",") if p and Path(p).exists()] if item["attachment_paths"] else []
        
        # Ensure master resume is always included in attachments
        has_resume = any("resume" in p.lower() or "cv" in p.lower() for p in attachments)
        if not has_resume and resolved_master_resume:
            attachments.append(str(resolved_master_resume))
        
        if dry_run:
            results.append({"id": item["id"], "recipient": item["recipient_email"], "status": "dry_run_ready"})
            continue

        success, err = send_smtp_email(
            to_email=item["recipient_email"],
            subject=item["subject"],
            body_text=item["body_text"],
            attachment_paths=attachments
        )

        sent_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if success:
            cur.execute("UPDATE email_queue SET status = 'sent', sent_at = ? WHERE id = ?", (sent_time, item["id"]))
            cur.execute("UPDATE contacts SET status = 'emailed' WHERE id = ?", (item["contact_id"],))
            # Schedule 7-day follow-up
            due_followup = (datetime.utcnow() + timedelta(days=FOLLOWUP_DAYS)).strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("""
                INSERT INTO followups (email_id, contact_id, initial_sent_at, due_date, status)
                VALUES (?, ?, ?, ?, 'pending')
            """, (item["id"], item["contact_id"], sent_time, due_followup))
            results.append({"id": item["id"], "recipient": item["recipient_email"], "status": "sent"})
        else:
            cur.execute("UPDATE email_queue SET status = 'failed', error_message = ? WHERE id = ?", (err, item["id"]))
            results.append({"id": item["id"], "recipient": item["recipient_email"], "status": "failed", "error": err})

    conn.commit()
    conn.close()
    return results

def check_inbox_replies() -> List[Dict]:
    """Scans Gmail Inbox via IMAP to automatically detect replies and remove contacts from future queues."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return []
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Get all active contact emails to monitor
    monitored_contacts = cur.execute("SELECT id, email, name FROM contacts").fetchall()
    contact_map = {row["email"].lower(): row for row in monitored_contacts}
    
    detected_replies = []
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select("INBOX")

        # Search for recent messages in the inbox
        status, messages = mail.search(None, "ALL")
        if status == "OK":
            email_ids = messages[0].split()
            # Check the latest 50 messages to stay fast and responsive
            for e_id in email_ids[-50:]:
                _, msg_data = mail.fetch(e_id, "(RFC822.HEADER)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        from_header = msg.get("From", "")
                        subject_header = msg.get("Subject", "")
                        
                        # Extract sender email address
                        sender_email = ""
                        if "<" in from_header and ">" in from_header:
                            sender_email = from_header.split("<")[1].split(">")[0].strip().lower()
                        else:
                            sender_email = from_header.strip().lower()

                        if sender_email in contact_map:
                            contact_info = contact_map[sender_email]
                            c_id = contact_info["id"]
                            
                            # Mark contact as replied in DB
                            cur.execute("UPDATE contacts SET status = 'replied' WHERE id = ?", (c_id,))
                            # Cancel pending / approved emails in queue for this contact
                            cur.execute("UPDATE email_queue SET status = 'replied_cancelled' WHERE contact_id = ? AND status IN ('pending', 'approved')", (c_id,))
                            # Cancel pending follow-ups
                            cur.execute("UPDATE followups SET status = 'replied' WHERE contact_id = ?", (c_id,))
                            
                            detected_replies.append({
                                "contact_id": c_id,
                                "email": sender_email,
                                "name": contact_info["name"],
                                "subject": subject_header
                            })

        mail.logout()
    except Exception as ex:
        print(f"Error checking IMAP replies: {ex}")
    
    conn.commit()
    conn.close()
    return detected_replies

if __name__ == "__main__":
    print("Email engine loaded successfully.")
    print("Testing timezone calculator for Morocco:", calculate_next_send_time("Africa/Casablanca"))
    print("Checking inbox replies...")
    replies = check_inbox_replies()
    print("Detected replies:", len(replies))
