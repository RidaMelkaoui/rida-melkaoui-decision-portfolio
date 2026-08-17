import sqlite3
from config import DB_PATH, PORTFOLIO_URL, LINKEDIN_URL, CANDIDATE_NAME, CANDIDATE_PHONE, CANDIDATE_EMAIL

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Tailored InstaDeep Email Body
instadeep_subj = f"Candidature : Decision AI & Optimization Engineer — {CANDIDATE_NAME} (AIAC)"
instadeep_body = f"""Bonjour,

Je me permets de vous soumettre ma candidature pour le rôle de Decision AI & Optimization Engineer au sein d'InstaDeep.

Ingénieur d'État en Génie Industriel & Production (AIAC) et actuellement Supplier Quality Engineer chez Magna International, je conçois des systèmes d'aide à la décision opérationnels fondés sur l'optimisation mathématique et l'ingénierie des données.

Mes réalisations directement alignées avec les problématiques d'InstaDeep :
1. Route / Control — Tour de contrôle de dispatch & optimisation : Modélisation des préférences de zone sur 6 112 tournées, recherche locale sous contraintes, réduction de 2,8% du temps de trajet et 100% de respect des créneaux horaires.
2. Agent / Proof — Évaluation & observabilité IA : Banc d'évaluation sur 3 336 trajectoires d'outils IA (pass@k, répétabilité, coût et latence).
3. Stellantis R&D — Traitement automatisé des anomalies (Databricks / Python) : Cycle de traitement réduit de 2 jours à moins de 3 minutes (-98% de manipulation manuelle).

Vous trouverez ci-joint mon CV ATS ainsi que ma lettre de motivation détaillée.
Mon portfolio de projets de décision est consultable ici : {PORTFOLIO_URL}

Je serais ravi d'échanger avec votre équipe sur la manière dont mes compétences en optimisation et IA appliquée peuvent contribuer aux solutions d'InstaDeep.

Bien cordialement,
{CANDIDATE_NAME}
{CANDIDATE_PHONE} | {CANDIDATE_EMAIL}
{LINKEDIN_URL}"""

# Tailored Yassir Email Body
yassir_subj = f"Candidature : Operations & Dispatch Analytics Lead / Decision Engineer — {CANDIDATE_NAME}"
yassir_body = f"""Bonjour à l'équipe Talent & Opérations Yassir,

Je vous adresse ma candidature pour le poste d'Operations & Dispatch Analytics Lead / Decision Engineer chez Yassir.

Ingénieur d'État en Génie Industriel & Production (AIAC) et actuellement Supplier Quality Engineer chez Magna International, je combine l'ingénierie opérationnelle avec la data science (Python, SQL, Databricks, Power BI) pour optimiser les flux de dispatch et la performance sur le terrain.

Trois réalisations transférables à l'écosystème Yassir :
1. Route / Control — Optimisation du dispatch & tournées : Système d'affectation sous contraintes appris sur 6 112 historiques réels, réduisant le temps de trajet de 2,8%, éliminant 332 ré-entrées de zone et garantissant 100% de respect des délais.
2. Demand / Order — Prévision de la demande & rééquilibrage : Moteur prédictif réduisant le WAPE de 4,5% et améliorant la disponibilité à 96,7%.
3. Automatisation des opérations (Stellantis R&D) : Réduction du temps de cycle opérationnel de 2 jours à moins de 3 minutes via Python et Databricks.

Mon CV et ma lettre de motivation sont joints à ce message.
Mon portfolio complet est disponible à l'adresse suivante : {PORTFOLIO_URL}

Disponible pour un échange à votre convenance.

Bien cordialement,
{CANDIDATE_NAME}
{CANDIDATE_PHONE} | {CANDIDATE_EMAIL}
{LINKEDIN_URL}"""

cur.execute("UPDATE email_queue SET subject = ?, body_text = ? WHERE company_name = 'InstaDeep'", (instadeep_subj, instadeep_body))
cur.execute("UPDATE email_queue SET subject = ?, body_text = ? WHERE company_name = 'Yassir'", (yassir_subj, yassir_body))

conn.commit()
conn.close()
print("Updated InstaDeep and Yassir emails successfully in email_queue.")
