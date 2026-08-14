import sys
import argparse
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from database import get_connection, init_db
from ingest_contacts import ingest_morocco_contacts
from job_hunter import seed_and_tailor_jobs
from email_engine import queue_outreach_for_contact, process_due_emails, send_smtp_email, check_inbox_replies
from report_generator import generate_daily_report
from config import GMAIL_USER, CANDIDATE_NAME

def show_dashboard():
    conn = get_connection()
    cur = conn.cursor()

    print("\n" + "="*70)
    print(f"       CAREER OS — DECISION ENGINEER APPLICATION CONTROLLER")
    print(f"       Candidate: {CANDIDATE_NAME} ({GMAIL_USER})")
    print("="*70)

    # Metrics
    companies_count = cur.execute("SELECT COUNT(*) FROM companies WHERE is_blacklisted = 0").fetchone()[0]
    contacts_count = cur.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    jobs_count = cur.execute("SELECT COUNT(*) FROM job_offers").fetchone()[0]
    apps_count = cur.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    queue_pending = cur.execute("SELECT COUNT(*) FROM email_queue WHERE status = 'pending'").fetchone()[0]
    queue_approved = cur.execute("SELECT COUNT(*) FROM email_queue WHERE status = 'approved'").fetchone()[0]
    queue_sent = cur.execute("SELECT COUNT(*) FROM email_queue WHERE status = 'sent'").fetchone()[0]
    followups_pending = cur.execute("SELECT COUNT(*) FROM followups WHERE status = 'pending'").fetchone()[0]

    print("\n📊 PIPELINE SUMMARY METRICS:")
    print(f"   • Active Companies:     {companies_count}")
    print(f"   • Key Contacts:         {contacts_count}")
    print(f"   • Active Job Offers:    {jobs_count}")
    print(f"   • Tailored Applications:{apps_count}")
    print(f"   • Emails in Review:     {queue_pending} (awaiting approval)")
    print(f"   • Emails Approved:      {queue_approved} (scheduled for 8-9 AM local)")
    print(f"   • Emails Sent:          {queue_sent}")
    print(f"   • Follow-ups Due/Track: {followups_pending}")

    # Pending Queue Details
    pending_items = cur.execute("""
        SELECT eq.id, eq.company_name, eq.recipient_name, eq.recipient_email, eq.target_timezone, eq.scheduled_time, eq.status
        FROM email_queue eq
        ORDER BY eq.scheduled_time ASC
        LIMIT 10
    """).fetchall()

    if pending_items:
        print("\n📬 OUTREACH QUEUE (Top 10 Scheduled Deliveries):")
        print(f"   {'ID':<4} | {'Status':<9} | {'Company':<22} | {'Recipient':<22} | {'Timezone':<18} | {'Scheduled UTC'}")
        print("   " + "-"*95)
        for item in pending_items:
            status_box = f"[{'X' if item['status'] == 'approved' else ' '}] {item['status']}"
            print(f"   {item['id']:<4} | {status_box:<9} | {item['company_name'][:20]:<22} | {item['recipient_name'][:20]:<22} | {item['target_timezone']:<18} | {item['scheduled_time']}")
    else:
        print("\n📬 OUTREACH QUEUE: Empty. Run --queue-all or --daily-sweep to populate.")

    # High-Priority Jobs
    jobs = cur.execute("""
        SELECT j.priority_tier, j.title, co.name AS company, j.location, j.work_mode, j.url
        FROM job_offers j
        JOIN companies co ON j.company_id = co.id
        ORDER BY j.priority_tier ASC
        LIMIT 5
    """).fetchall()

    if jobs:
        print("\n🎯 TOP CURATED ACTIVE JOB OPPORTUNITIES:")
        for job in jobs:
            print(f"   [{job['priority_tier']}] {job['title']} @ {job['company']} ({job['location']} - {job['work_mode']})")
            print(f"       Apply: {job['url']}")

    print("\n" + "="*70 + "\n")
    conn.close()

def queue_all_contacts(limit: int = 10):
    """Queues outreach emails for the top un-emailed contacts in database."""
    conn = get_connection()
    cur = conn.cursor()
    
    contacts = cur.execute("""
        SELECT c.id, c.name, co.name AS company
        FROM contacts c
        JOIN companies co ON c.company_id = co.id
        WHERE c.status = 'pending' 
          AND co.is_blacklisted = 0
          AND c.id NOT IN (SELECT contact_id FROM email_queue)
        LIMIT ?
    """, (limit,)).fetchall()
    
    queued = 0
    for c in contacts:
        qid = queue_outreach_for_contact(c["id"])
        if qid:
            queued += 1
            
    print(f"Successfully queued {queued} outreach emails with tailored cover letters and timezone scheduling.")
    conn.close()

def approve_queue(item_id: str = "all"):
    conn = get_connection()
    cur = conn.cursor()
    if item_id == "all":
        cur.execute("UPDATE email_queue SET status = 'approved' WHERE status = 'pending'")
        print("Approved ALL pending outreach emails in queue for automated dispatch.")
    else:
        cur.execute("UPDATE email_queue SET status = 'approved' WHERE id = ?", (int(item_id),))
        print(f"Approved outreach email ID #{item_id} for automated dispatch.")
    conn.commit()
    conn.close()

def mark_status(email_or_id: str, new_status: str):
    conn = get_connection()
    cur = conn.cursor()
    if email_or_id.isdigit():
        cur.execute("UPDATE contacts SET status = ? WHERE id = ?", (new_status, int(email_or_id)))
    else:
        cur.execute("UPDATE contacts SET status = ? WHERE email = ?", (new_status, email_or_id.strip()))
    conn.commit()
    conn.close()
    print(f"Updated contact {email_or_id} status to '{new_status}'.")

def main():
    parser = argparse.ArgumentParser(description="Career OS — Decision Engineer Application Controller")
    parser.add_argument("--status", action="store_true", help="Display application pipeline dashboard and review queue")
    parser.add_argument("--daily-sweep", action="store_true", help="Execute complete morning sweep: ingest, seed jobs, generate PDFs, queue emails")
    parser.add_argument("--queue-contacts", type=int, default=0, help="Queue N contacts for outreach")
    parser.add_argument("--approve", type=str, help="Approve email queue item (provide ID or 'all')")
    parser.add_argument("--dispatch", action="store_true", help="Send all approved emails due for their 8-9 AM local window")
    parser.add_argument("--force", action="store_true", help="Force immediate dispatch without waiting for 8-9 AM window")
    parser.add_argument("--dry-run", action="store_true", help="Simulate dispatch without sending actual emails")
    parser.add_argument("--check-replies", action="store_true", help="Scan Gmail inbox via IMAP and remove replying contacts")
    parser.add_argument("--report", action="store_true", help="Generate and update the Daily Application & Submission Briefing Report")
    parser.add_argument("--test-email", type=str, help="Send a test verification email to specified address")
    parser.add_argument("--mark-replied", type=str, help="Mark contact as replied (stops follow-ups)")
    parser.add_argument("--mark-stop", type=str, help="Mark contact as stopped/rejected")

    args = parser.parse_args()

    init_db()

    if args.daily_sweep:
        print("\n🚀 Executing Daily Morning Career OS Sweep...")
        check_inbox_replies()
        ingest_morocco_contacts()
        seed_and_tailor_jobs()
        queue_all_contacts(limit=10)
        rep_file = generate_daily_report()
        show_dashboard()
        print(f"\n📋 Daily Briefing Report generated at: {rep_file}")
    elif args.check_replies:
        print("\n🔍 Scanning Gmail inbox for candidate replies...")
        replies = check_inbox_replies()
        print(f"Detected {len(replies)} new replies from contacts.")
        for r in replies:
            print(f"  • {r['name']} ({r['email']}): {r['subject']}")
        generate_daily_report()
    elif args.report:
        rep_file = generate_daily_report()
        print(f"\n📋 Daily Briefing Report updated at: {rep_file}")
    elif args.test_email:
        print(f"\n📧 Sending test verification email to {args.test_email}...")
        ok, msg = send_smtp_email(
            to_email=args.test_email,
            subject=f"Test Verification — Career OS Pipeline ({CANDIDATE_NAME})",
            body_text=f"Hello!\n\nThis is a verification test from Career OS for {CANDIDATE_NAME}.\nSMTP authentication and TLS pipeline are working properly.\n\nBest regards,\nCareer OS Automated Engine"
        )
        print("Result:", "SUCCESS" if ok else f"FAILED: {msg}")
    elif args.queue_contacts:
        queue_all_contacts(limit=args.queue_contacts)
        generate_daily_report()
        show_dashboard()
    elif args.approve:
        approve_queue(args.approve)
        generate_daily_report()
        show_dashboard()
    elif args.dispatch:
        print(f"\n📤 Processing Dispatches (Force: {args.force}, Dry-Run: {args.dry_run})...")
        res = process_due_emails(dry_run=args.dry_run, force=args.force)
        print(f"Dispatched {len(res)} emails.")
        for r in res:
            print(f"  • ID #{r['id']} -> {r['recipient']}: {r['status']}")
        generate_daily_report()
    elif args.mark_replied:
        mark_status(args.mark_replied, "replied")
        generate_daily_report()
    elif args.mark_stop:
        mark_status(args.mark_stop, "checked")
        generate_daily_report()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
