import os
from datetime import datetime
from pathlib import Path
from config import PROJECT_ROOT, DELIVERABLES_DIR, CANDIDATE_NAME, CANDIDATE_TITLE, PORTFOLIO_URL, GMAIL_USER
from database import get_connection

def generate_daily_report() -> str:
    """Generates a comprehensive Daily Application & Submission Briefing Report in Markdown."""
    
    conn = get_connection()
    cur = conn.cursor()
    
    today_str = datetime.now().strftime("%d %B %Y")
    now_ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # 1. Summary Metrics
    c_count = cur.execute("SELECT COUNT(*) FROM companies WHERE is_blacklisted = 0").fetchone()[0]
    contact_count = cur.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    job_count = cur.execute("SELECT COUNT(*) FROM job_offers").fetchone()[0]
    app_count = cur.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    queue_pending = cur.execute("SELECT COUNT(*) FROM email_queue WHERE status = 'pending'").fetchone()[0]
    queue_approved = cur.execute("SELECT COUNT(*) FROM email_queue WHERE status = 'approved'").fetchone()[0]
    queue_sent = cur.execute("SELECT COUNT(*) FROM email_queue WHERE status = 'sent'").fetchone()[0]
    replies_count = cur.execute("SELECT COUNT(*) FROM contacts WHERE status = 'replied'").fetchone()[0]
    followups_count = cur.execute("SELECT COUNT(*) FROM followups WHERE status = 'pending'").fetchone()[0]

    # 2. Active Job Offers with Tailored Documents
    jobs = cur.execute("""
        SELECT j.id, j.priority_tier, j.title, co.name AS company, j.location, j.work_mode, j.url, j.description,
               a.cover_letter_path, a.resume_path
        FROM job_offers j
        JOIN companies co ON j.company_id = co.id
        LEFT JOIN applications a ON j.id = a.job_id
        ORDER BY j.priority_tier ASC, j.id ASC
    """).fetchall()

    # 3. Scheduled & Dispatched Emails
    emails = cur.execute("""
        SELECT eq.id, eq.company_name, eq.recipient_name, eq.recipient_email, eq.target_timezone,
               eq.scheduled_time, eq.status, eq.sent_at
        FROM email_queue eq
        ORDER BY eq.scheduled_time ASC
    """).fetchall()

    # 4. Monitored Follow-ups
    followups = cur.execute("""
        SELECT f.id, c.name AS contact_name, co.name AS company, c.email, f.initial_sent_at, f.due_date, f.status
        FROM followups f
        JOIN contacts c ON f.contact_id = c.id
        JOIN companies co ON c.company_id = co.id
        ORDER BY f.due_date ASC
    """).fetchall()

    conn.close()

    # Build Markdown Content
    lines = [
        f"# Career OS — Daily Application & Submission Briefing Report",
        f"**Candidate:** {CANDIDATE_NAME} ({CANDIDATE_TITLE})  ",
        f"**Date:** {today_str} | **Sender Account:** `{GMAIL_USER}`  ",
        f"**Live Portfolio:** [{PORTFOLIO_URL}]({PORTFOLIO_URL})  ",
        f"\n---\n",
        f"## 1. Executive Summary & Pipeline Metrics",
        f"\n| Metric | Count | Description |",
        f"| :--- | :--- | :--- |",
        f"| **Active Qualified Companies** | **{c_count}** | Excludes blacklisted firms (Aptiv, Alten, Magna, Valeo) |",
        f"| **Decision-Maker Contacts** | **{contact_count}** | Direct leadership & recruitment contacts |",
        f"| **Target Job Offers** | **{job_count}** | Curated & discovered roles (P1 to P6) |",
        f"| **Tailored PDF Packages** | **{app_count}** | Ready 3-Pillar Cover Letters in `deliverables/applications/` |",
        f"| **Emails in Review** | **{queue_pending}** | Pending your approval |",
        f"| **Emails Approved for Dispatch** | **{queue_approved}** | Scheduled for 08:30 AM recipient local time |",
        f"| **Total Emails Dispatched** | **{queue_sent}** | Delivered via authenticated Gmail SMTP |",
        f"| **Active Responses Detected** | **{replies_count}** | Automatically paused from future queues |",
        f"| **Scheduled 7-Day Follow-ups** | **{followups_count}** | Active follow-up tracking loops |",
        f"\n---\n",
        f"## 2. Active Web ATS Opportunities (1-Click Submission Packages)",
        f"\nFor each target role, your customized **3-Pillar Cover Letter PDF** and **Decision Engineer Resume** are already generated. Click the direct link below to submit in 60 seconds:\n",
    ]

    for j in jobs:
        cl_path = j["cover_letter_path"] if j["cover_letter_path"] else "Auto-generated upon request"
        cl_link = f"[{Path(cl_path).name}](file:///{cl_path.replace(chr(92), '/')})" if j["cover_letter_path"] and Path(cl_path).exists() else "`Pending Generation`"
        
        lines.extend([
            f"### [{j['priority_tier']}] {j['title']} — **{j['company']}**",
            f"- **Work Mode / Location:** {j['work_mode']} ({j['location']})",
            f"- **Direct Application URL:** [{j['url']}]({j['url']})",
            f"- **Tailored Cover Letter PDF:** {cl_link}",
            f"- **Role Scope:** {j['description']}",
            f"- **Fast Submission Checklist:**",
            f"  1. Open the [Application Link]({j['url']}).",
            f"  2. Upload the tailored PDF ({cl_link}) and master resume.",
            f"  3. Include portfolio link: `{PORTFOLIO_URL}`",
            f"\n"
        ])

    lines.extend([
        f"---\n",
        f"## 3. Direct Email Outreach Queue (Timezone-Aware Delivery)",
        f"\nAll outreach emails are scheduled for **08:30 AM in each recipient's local timezone**:\n",
        f"| ID | Status | Company | Key Contact | Recipient Email | Timezone | Scheduled Time |",
        f"| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ])

    for e in emails:
        sent_info = e["sent_at"] if e["sent_at"] else e["scheduled_time"]
        status_badge = f"**{e['status'].upper()}**"
        lines.append(f"| #{e['id']} | {status_badge} | {e['company_name']} | {e['recipient_name']} | `{e['recipient_email']}` | {e['target_timezone']} | {sent_info} |")

    if followups:
        lines.extend([
            f"\n---\n",
            f"## 4. Active Follow-Up Monitoring Loops (7-Day Cadence)",
            f"\n| Follow-up ID | Company | Contact | Email | Sent Date | Next Due Date | Status |",
            f"| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])
        for f in followups:
            lines.append(f"| #{f['id']} | {f['company']} | {f['contact_name']} | `{f['email']}` | {f['initial_sent_at']} | {f['due_date']} | {f['status']} |")

    lines.extend([
        f"\n---\n",
        f"## 5. Daily Execution Commands Reference",
        f"\n```powershell",
        f"# 1. Run daily morning sweep (hunt, generate tailored PDFs, queue emails, write report):",
        f"python run_career_os.py --daily-sweep",
        f"",
        f"# 2. Approve all pending outreach emails:",
        f"python run_career_os.py --approve all",
        f"",
        f"# 3. Dispatch due emails (at 8:00-9:00 AM local window):",
        f"python run_career_os.py --dispatch",
        f"",
        f"# 4. Scan Gmail inbox for new replies (automatically removes replying contacts):",
        f"python run_career_os.py --check-replies",
        f"```",
        f"\n*Report generated by Career OS Engine at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    ])

    report_content = "\n".join(lines)
    
    # Save main report
    main_report_path = PROJECT_ROOT / "deliverables" / "DAILY_APPLICATION_REPORT.md"
    with open(main_report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    # Save historical archive report
    reports_archive_dir = PROJECT_ROOT / "deliverables" / "reports"
    reports_archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = reports_archive_dir / f"REPORT_{now_ts}.md"
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return str(main_report_path)

if __name__ == "__main__":
    report_file = generate_daily_report()
    print("Daily Report generated at:", report_file)
