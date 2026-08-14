import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import DB_PATH, is_blacklisted

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=60.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        industry TEXT,
        city TEXT,
        country TEXT DEFAULT 'Morocco',
        career_url TEXT,
        is_blacklisted INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        salutation TEXT,
        title TEXT,
        email TEXT UNIQUE NOT NULL,
        linkedin_url TEXT,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS job_offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
        title TEXT NOT NULL,
        location TEXT,
        work_mode TEXT DEFAULT 'remote',
        url TEXT,
        priority_tier TEXT DEFAULT 'P1',
        description TEXT,
        status TEXT DEFAULT 'discovered',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE SET NULL,
        job_id INTEGER REFERENCES job_offers(id) ON DELETE SET NULL,
        role_title TEXT NOT NULL,
        resume_path TEXT,
        cover_letter_path TEXT,
        subject TEXT,
        body_text TEXT,
        status TEXT DEFAULT 'drafted',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS email_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id INTEGER REFERENCES applications(id) ON DELETE SET NULL,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
        recipient_email TEXT NOT NULL,
        recipient_name TEXT,
        company_name TEXT,
        subject TEXT NOT NULL,
        body_text TEXT NOT NULL,
        attachment_paths TEXT,
        target_timezone TEXT DEFAULT 'Africa/Casablanca',
        scheduled_time DATETIME NOT NULL,
        status TEXT DEFAULT 'pending',
        sent_at DATETIME,
        error_message TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS followups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_id INTEGER REFERENCES email_queue(id) ON DELETE CASCADE,
        contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
        initial_sent_at DATETIME NOT NULL,
        due_date DATETIME NOT NULL,
        followup_number INTEGER DEFAULT 1,
        status TEXT DEFAULT 'pending',
        scheduled_time DATETIME,
        sent_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

def upsert_company(name: str, industry: str = "", city: str = "", country: str = "Morocco", career_url: str = "", conn: Optional[sqlite3.Connection] = None) -> int:
    name_clean = name.strip()
    blacklisted = 1 if is_blacklisted(name_clean) else 0
    should_close = False
    if conn is None:
        conn = get_connection()
        should_close = True

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO companies (name, industry, city, country, career_url, is_blacklisted)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            industry = CASE WHEN excluded.industry != '' THEN excluded.industry ELSE companies.industry END,
            city = CASE WHEN excluded.city != '' THEN excluded.city ELSE companies.city END,
            country = CASE WHEN excluded.country != '' THEN excluded.country ELSE companies.country END,
            career_url = CASE WHEN excluded.career_url != '' THEN excluded.career_url ELSE companies.career_url END,
            is_blacklisted = excluded.is_blacklisted
    """, (name_clean, industry, city, country, career_url, blacklisted))
    conn.commit()
    cur.execute("SELECT id FROM companies WHERE name = ?", (name_clean,))
    row = cur.fetchone()
    if should_close:
        conn.close()
    return row["id"]

def upsert_contact(company_id: int, name: str, salutation: str, title: str, email: str, linkedin_url: str = "", conn: Optional[sqlite3.Connection] = None) -> Optional[int]:
    email_clean = email.strip().lower()
    if not email_clean or "@" not in email_clean:
        return None
    should_close = False
    if conn is None:
        conn = get_connection()
        should_close = True

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO contacts (company_id, name, salutation, title, email, linkedin_url)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
            name = excluded.name,
            salutation = excluded.salutation,
            title = excluded.title,
            linkedin_url = excluded.linkedin_url
    """, (company_id, name.strip(), salutation.strip(), title.strip(), email_clean, linkedin_url.strip()))
    conn.commit()
    cur.execute("SELECT id FROM contacts WHERE email = ?", (email_clean,))
    row = cur.fetchone()
    if should_close:
        conn.close()
    return row["id"]

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
