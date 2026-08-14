import os
from pathlib import Path
from dotenv import load_dotenv

# Root Directory Paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DELIVERABLES_DIR = PROJECT_ROOT / "deliverables" / "applications"
DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "career_os.db"

# Load .env
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Candidate Profile
CANDIDATE_NAME = os.getenv("CANDIDATE_NAME", "Rida Melkaoui")
CANDIDATE_TITLE = os.getenv("CANDIDATE_TITLE", "Industrial Engineer | Decision & Data Analytics Engineer")
CANDIDATE_EMAIL = os.getenv("CANDIDATE_EMAIL", "ridamelkaouiofficial@gmail.com")
CANDIDATE_PHONE = os.getenv("CANDIDATE_PHONE", "+212 620 999 885")
CANDIDATE_LOCATION = os.getenv("CANDIDATE_LOCATION", "Kenitra / Salé, Morocco")
PORTFOLIO_URL = os.getenv("PORTFOLIO_URL", "https://ridamelkaoui.github.io/rida-melkaoui-decision-portfolio/")
LINKEDIN_URL = os.getenv("LINKEDIN_URL", "https://www.linkedin.com/in/rida-melkaoui-7bab50256/")

# Email Credentials
GMAIL_USER = os.getenv("GMAIL_USER", "ridamelkaouiofficial@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "")

# Strict Exclusion Blacklist (User Explicit Requirement)
EXCLUDED_COMPANIES = [
    "aptiv",
    "alten",
    "magna",
    "magna international",
    "valeo",
    "sany",
]

def is_blacklisted(company_name: str) -> bool:
    if not company_name:
        return False
    normalized = company_name.strip().lower()
    return any(b in normalized for b in EXCLUDED_COMPANIES)

# Dispatch & Scheduling Rules
SEND_WINDOW_START_HOUR = 8   # 08:00 AM local time
SEND_WINDOW_END_HOUR = 9     # 09:00 AM local time
FOLLOWUP_DAYS = 7            # 7-day follow-up cadence

# Default Timezone Mappings
TIMEZONE_MAP = {
    "morocco": "Africa/Casablanca",
    "ma": "Africa/Casablanca",
    "france": "Europe/Paris",
    "fr": "Europe/Paris",
    "germany": "Europe/Berlin",
    "de": "Europe/Berlin",
    "uk": "Europe/London",
    "united kingdom": "Europe/London",
    "netherlands": "Europe/Amsterdam",
    "nl": "Europe/Amsterdam",
    "spain": "Europe/Madrid",
    "es": "Europe/Madrid",
    "usa": "America/New_York",
    "us": "America/New_York",
    "canada": "America/Toronto",
    "ca": "America/Toronto",
    "remote": "Africa/Casablanca",  # Default baseline for remote when country not specified
}

def get_timezone_for_country(country: str) -> str:
    if not country:
        return "Africa/Casablanca"
    c_lower = country.strip().lower()
    return TIMEZONE_MAP.get(c_lower, "Africa/Casablanca")
