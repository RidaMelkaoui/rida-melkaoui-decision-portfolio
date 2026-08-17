import json
import sqlite3
from typing import List, Dict
from config import is_blacklisted
from database import get_connection, upsert_company
from document_generator import generate_cover_letter_pdf

# Curated High-Fit Seed Opportunities (P1 to P6)
CURATED_OPPORTUNITIES = [
    {
        "company": "Lunar Energy",
        "industry": "CleanTech / Manufacturing & Supply Chain IoT",
        "city": "San Francisco",
        "country": "USA",
        "title": "Operations BI Engineer",
        "work_mode": "Remote",
        "priority_tier": "P1",
        "url": "https://job-boards.greenhouse.io/lunarenergy",
        "description": "Owns BI dashboarding, internal tool building, and workflow automation for manufacturing, supply chain, quality, and fulfillment teams. Tracks OEE, yield, downtime, cycle time, throughput."
    },
    {
        "company": "Lokad",
        "industry": "Supply Chain Quantitative Decision Intelligence",
        "city": "Paris",
        "country": "France",
        "title": "Supply Chain Scientist / Decision Engineer",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P1",
        "url": "https://www.lokad.com/careers",
        "description": "Translates complex supply chain operations into quantitative decision systems (demand forecasting, inventory buffers, price optimization) using predictive algorithms."
    },
    {
        "company": "Alpaca",
        "industry": "FinTech / API Infrastructure",
        "city": "London / Europe",
        "country": "UK",
        "title": "Senior Analytics Engineer (Operations)",
        "work_mode": "Remote",
        "priority_tier": "P1",
        "url": "https://boards.greenhouse.io/alpaca",
        "description": "Builds scalable data models, dbt pipelines, and operational decision dashboards for cross-functional business and finance teams."
    },
    {
        "company": "Extend",
        "industry": "Warranty & Logistics Tech Scaleup",
        "city": "San Francisco",
        "country": "USA",
        "title": "Analytics Engineer (Operations Systems)",
        "work_mode": "Remote",
        "priority_tier": "P2",
        "url": "https://boards.greenhouse.io/extend",
        "description": "Ensures data integrity across operational and fulfillment systems, building analytics for automated shipping protection."
    },
    {
        "company": "Sight Machine",
        "industry": "Manufacturing Data Platform / Industrial AI",
        "city": "San Francisco",
        "country": "USA",
        "title": "Solutions & Manufacturing Data Engineer",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P3",
        "url": "https://sightmachine.com/careers",
        "description": "Transforms real-time shop-floor and PLC data into operational decision insights for enterprise manufacturers."
    },
    {
        "company": "Tulip Interfaces",
        "industry": "Frontline Operations Apps for Manufacturing",
        "city": "Boston / Munich",
        "country": "Germany",
        "title": "Manufacturing Data & Operations Engineer",
        "work_mode": "Hybrid / Relocation",
        "priority_tier": "P3",
        "url": "https://tulip.co/careers/",
        "description": "Builds frontline operations apps, data integrations, and analytics for factory floor operators and quality engineers."
    },
    {
        "company": "project44",
        "industry": "Real-Time Supply Chain Visibility",
        "city": "Chicago / Amsterdam",
        "country": "Netherlands",
        "title": "Supply Chain Analytics Engineer",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P4",
        "url": "https://boards.greenhouse.io/project44",
        "description": "Builds predictive analytics and tracking pipelines for global multimodal supply chains."
    },
    {
        "company": "Freterium",
        "industry": "Digital Freight & Logistics SaaS",
        "city": "Casablanca",
        "country": "Morocco",
        "title": "Operations Data Analyst / Engineer",
        "work_mode": "Hybrid / Remote",
        "priority_tier": "P5",
        "url": "https://www.freterium.com/careers",
        "description": "Builds transport tracking, route optimization, and operational visibility for logistics and manufacturing clients across Morocco & MENA."
    },
    {
        "company": "Capgemini Engineering",
        "industry": "Engineering & Technology Consulting",
        "city": "Casablanca",
        "country": "Morocco",
        "title": "Business Analyst Junior / Decision Engineer",
        "work_mode": "Hybrid",
        "priority_tier": "P6",
        "url": "https://www.capgemini.com/ma-en/jobs/454212-fr_FR%2Bsap_btp/",
        "description": "Collects and translates business needs, structures data workflows, aligns technical teams, and validates delivery against operational outcomes."
    },
    {
        "company": "Celonis",
        "industry": "Process Mining & Execution Management",
        "city": "Munich / Madrid",
        "country": "Germany",
        "title": "Value & Process Intelligence Engineer",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P1",
        "url": "https://www.celonis.com/careers",
        "description": "Combines process mining, SQL data modeling, and operational KPI optimization to identify execution bottlenecks and automate workflow decisions."
    },
    {
        "company": "o9 Solutions",
        "industry": "Enterprise Supply Chain Decision Management",
        "city": "Amsterdam / London",
        "country": "Netherlands",
        "title": "Supply Chain Decision Architect",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P1",
        "url": "https://o9solutions.com/careers",
        "description": "Builds integrated business planning, demand forecasting models, and inventory optimization decision graphs for complex supply chains."
    },
    {
        "company": "Kinaxis",
        "industry": "Supply Chain Concurrent Planning & Optimization",
        "city": "London / Europe",
        "country": "UK",
        "title": "Operations Research & Supply Chain Analyst",
        "work_mode": "Remote",
        "priority_tier": "P2",
        "url": "https://www.kinaxis.com/en/careers",
        "description": "Designs concurrent planning algorithms, safety stock simulations, and exception-monitoring workflows for global manufacturing operations."
    },
    {
        "company": "Chari",
        "industry": "B2B E-commerce & FMCG Logistics SaaS",
        "city": "Casablanca",
        "country": "Morocco",
        "title": "Operations & Logistics Data Analyst",
        "work_mode": "Hybrid",
        "priority_tier": "P5",
        "url": "https://chari.co/",
        "description": "Optimizes last-mile delivery routes, warehouse picking throughput, and inventory replenishment forecasting for retail distribution across Morocco."
    },
    {
        "company": "Shippeo",
        "industry": "Real-Time Transportation Visibility Platform",
        "city": "Paris",
        "country": "France",
        "title": "Supply Chain Data & BI Engineer",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P1",
        "url": "https://www.shippeo.com/careers",
        "description": "Builds tracking data pipelines, predictive ETA models, and carrier quality scorecards for multimodal supply chain networks."
    },
    {
        "company": "Sennder",
        "industry": "Digital Road Freight Forwarding",
        "city": "Berlin",
        "country": "Germany",
        "title": "Operations Analytics & BI Engineer",
        "work_mode": "Remote",
        "priority_tier": "P1",
        "url": "https://www.sennder.com/careers",
        "description": "Develops carrier matching analytics, freight pricing models, and automated exception queues for European road transportation."
    },
    {
        "company": "Samsara",
        "industry": "Connected Operations IoT & Industrial Telematics",
        "city": "London / Europe",
        "country": "UK",
        "title": "Operations BI & Analytics Engineer",
        "work_mode": "Remote",
        "priority_tier": "P1",
        "url": "https://www.samsara.com/company/careers/",
        "description": "Transforms IoT telemetry and vehicle asset data into operational decision intelligence and predictive fleet workflows."
    },
    {
        "company": "Forto",
        "industry": "Digital Freight Forwarding & Supply Chain Tech",
        "city": "Berlin",
        "country": "Germany",
        "title": "Supply Chain Data & Trade Analytics Engineer",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P1",
        "url": "https://www.forto.com/careers/",
        "description": "Designs freight pricing algorithms, lane predictability models, and automated supply chain visibility workflows."
    },
    {
        "company": "InstaDeep",
        "industry": "Decision-Making AI & Enterprise Optimization",
        "city": "Paris / London / Casablanca",
        "country": "France",
        "title": "Decision AI & Optimization Engineer",
        "work_mode": "Remote / Hybrid",
        "priority_tier": "P1",
        "url": "https://www.instadeep.com/careers",
        "description": "Applies deep reinforcement learning and mathematical programming to industrial routing, scheduling, and operational decision systems."
    },
    {
        "company": "Cognite",
        "industry": "Industrial DataOps & AI for Manufacturing",
        "city": "Oslo / Europe",
        "country": "Norway",
        "title": "Industrial Solutions & Data Engineer",
        "work_mode": "Remote",
        "priority_tier": "P2",
        "url": "https://www.cognite.com/en/careers",
        "description": "Unifies OT and IT data across manufacturing plants to build contextualized decision tools and predictive maintenance pipelines."
    },
    {
        "company": "Transporeon",
        "industry": "Transportation Management Platform",
        "city": "Amsterdam / Europe",
        "country": "Netherlands",
        "title": "Logistics Network Data Analyst",
        "work_mode": "Remote",
        "priority_tier": "P2",
        "url": "https://www.transporeon.com/en/careers",
        "description": "Analyzes global transport network flows, slot booking bottlenecks, and carrier spot-rate trends to automate logistics decisions."
    },
    {
        "company": "Yassir",
        "industry": "On-Demand Mobility & Logistics Tech Scaleup",
        "city": "Casablanca",
        "country": "Morocco",
        "title": "Operations & Dispatch Analytics Lead",
        "work_mode": "Hybrid / Remote",
        "priority_tier": "P5",
        "url": "https://yassir.com/careers/",
        "description": "Optimizes on-demand driver dispatch, pricing elasticity, and fulfillment SLAs across North African metro areas."
    }
]

# Additional High-Growth Industrial & Tech Contacts
CURATED_CONTACTS = [
    {"company": "InstaDeep", "name": "Karim Beguir", "title": "Co-founder & CEO", "email": "recruitment@instadeep.com", "country": "France"},
    {"company": "InstaDeep", "name": "Talent Acquisition Team", "title": "Head of People & Hiring", "email": "careers@instadeep.com", "country": "France"},
    {"company": "Freterium", "name": "Mehdi Cherif Alami", "title": "Co-founder & CEO", "email": "contact@freterium.com", "country": "Morocco"},
    {"company": "Freterium", "name": "Talent & Growth Lead", "title": "Operations Hiring Lead", "email": "talent@freterium.com", "country": "Morocco"},
    {"company": "Chari", "name": "Ismael Belkhayat", "title": "Co-founder & CEO", "email": "contact@chari.co", "country": "Morocco"},
    {"company": "Chari", "name": "Recruitment Department", "title": "Talent Lead", "email": "jobs@chari.co", "country": "Morocco"},
    {"company": "Lokad", "name": "Joannes Vermorel", "title": "Founder & CEO", "email": "contact@lokad.com", "country": "France"},
    {"company": "Yassir", "name": "Operations Hiring Team", "title": "Talent Acquisition Lead", "email": "careers@yassir.com", "country": "Morocco"},
    {"company": "Thales", "name": "Équipe Recrutement Maroc", "title": "Responsable Recrutement & RH", "email": "recrutement.maroc@thalesgroup.com", "country": "Morocco"},
    {"company": "Siemens Energy", "name": "Talent Acquisition Morocco", "title": "HR & Operations Lead", "email": "careers.morocco@siemens-energy.com", "country": "Morocco"},
    {"company": "Schneider Electric", "name": "Direction des Ressources Humaines", "title": "Talent Lead Maroc", "email": "recruitment.morocco@se.com", "country": "Morocco"},
    {"company": "STMicroelectronics", "name": "Ressources Humaines Bouskoura", "title": "Site Talent Lead", "email": "recrutement.bouskoura@st.com", "country": "Morocco"},
    {"company": "Safran Electrical & Power", "name": "Service Recrutement & Mobilité", "title": "Talent Acquisition", "email": "recrutement.sep@safrangroup.com", "country": "Morocco"},
    {"company": "Nexans", "name": "Direction RH & Développement", "title": "Talent Lead", "email": "rh.maroc@nexans.com", "country": "Morocco"},
    {"company": "Hitachi Energy", "name": "Talent Acquisition Hub", "title": "HR Lead Morocco", "email": "morocco.careers@hitachienergy.com", "country": "Morocco"}
]

def seed_and_tailor_jobs():
    """Seeds verified target job offers into the database and generates tailored PDF packages."""
    conn = get_connection()
    cur = conn.cursor()
    
    seeded_count = 0
    for item in CURATED_OPPORTUNITIES:
        if is_blacklisted(item["company"]):
            continue
        
        company_id = upsert_company(
            name=item["company"],
            industry=item["industry"],
            city=item["city"],
            country=item["country"],
            career_url=item["url"],
            conn=conn
        )
        
        # Check if job offer already exists
        cur.execute("SELECT id FROM job_offers WHERE company_id = ? AND title = ?", (company_id, item["title"]))
        existing_job = cur.fetchone()
        if existing_job:
            job_id = existing_job["id"]
        else:
            cur.execute("""
                INSERT INTO job_offers (company_id, title, location, work_mode, url, priority_tier, description, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'discovered')
            """, (company_id, item["title"], f"{item['city']}, {item['country']}", item["work_mode"], item["url"], item["priority_tier"], item["description"]))
            job_id = cur.lastrowid
            seeded_count += 1

            # Automatically generate tailored cover letter PDF
            pdf_path = generate_cover_letter_pdf(
                company_name=item["company"],
                role_title=item["title"],
                location=f"{item['city']}, {item['country']}",
                work_mode=item["work_mode"]
            )

            cur.execute("""
                INSERT INTO applications (company_id, job_id, role_title, cover_letter_path, status)
                VALUES (?, ?, ?, ?, 'tailored')
            """, (company_id, job_id, item["title"], pdf_path))

    # Seed curated high-growth contacts
    seeded_contacts = 0
    for c in CURATED_CONTACTS:
        if is_blacklisted(c["company"]):
            continue
        co_id = upsert_company(name=c["company"], country=c.get("country", "Morocco"), conn=conn)
        cur.execute("SELECT id FROM contacts WHERE email = ?", (c["email"].strip(),))
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO contacts (company_id, name, title, email, status)
                VALUES (?, ?, ?, ?, 'pending')
            """, (co_id, c["name"], c["title"], c["email"].strip()))
            seeded_contacts += 1

    conn.commit()
    conn.close()
    print(f"Successfully seeded {seeded_count} new job opportunities and {seeded_contacts} new key contacts.")

if __name__ == "__main__":
    seed_and_tailor_jobs()
