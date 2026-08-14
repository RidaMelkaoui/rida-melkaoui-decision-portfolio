import csv
from pathlib import Path
from config import DATA_DIR, is_blacklisted
from database import init_db, upsert_company, upsert_contact, get_connection

RAW_CSV_PATH = DATA_DIR / "raw_morocco_contacts.csv"

def ingest_morocco_contacts():
    init_db()
    if not RAW_CSV_PATH.exists():
        print(f"File not found: {RAW_CSV_PATH}")
        return

    imported_contacts = 0
    skipped_blacklisted = 0
    total_rows = 0

    conn = get_connection()
    with open(RAW_CSV_PATH, mode="r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 6:
                continue
            total_rows += 1
            company_raw = row[0].strip()
            salutation = row[1].strip()
            last_name = row[2].strip()
            full_name = row[3].strip() if len(row) > 3 and row[3].strip() else last_name
            function_title = row[4].strip() if len(row) > 4 else ""
            email = row[5].strip() if len(row) > 5 else ""

            if not company_raw or not email or "@" not in email:
                continue

            # Check blacklist rule
            if is_blacklisted(company_raw):
                skipped_blacklisted += 1
                continue

            company_id = upsert_company(
                name=company_raw,
                industry="Automotive / Aerospace / Industrial Engineering",
                city="Morocco",
                country="Morocco",
                conn=conn
            )

            contact_id = upsert_contact(
                company_id=company_id,
                name=full_name if full_name else last_name,
                salutation=salutation,
                title=function_title,
                email=email,
                conn=conn
            )
            if contact_id:
                imported_contacts += 1
    conn.close()

    print(f"\n--- Ingestion Summary ---")
    print(f"Total Rows Processed: {total_rows}")
    print(f"Qualified Contacts Ingested: {imported_contacts}")
    print(f"Blacklisted Skipped (Aptiv/Alten/Magna/Valeo): {skipped_blacklisted}")

    # Verify counts in SQLite
    conn = get_connection()
    c_count = conn.execute("SELECT COUNT(*) FROM companies WHERE is_blacklisted = 0").fetchone()[0]
    p_count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    conn.close()
    print(f"Active Non-Blacklisted Companies in DB: {c_count}")
    print(f"Active Decision-Maker Contacts in DB: {p_count}")

if __name__ == "__main__":
    ingest_morocco_contacts()
