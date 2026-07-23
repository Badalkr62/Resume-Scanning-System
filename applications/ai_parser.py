import pdfplumber
import re


SKILLS_DATABASE = [

    # Programming
    "Python", "Java", "C", "C++", "C#", "PHP",

    # Web
    "HTML", "CSS", "Bootstrap", "Tailwind",
    "JavaScript", "TypeScript",

    # Frontend
    "React", "Next.js", "Angular", "Vue",

    # Backend
    "Node", "Express", "Django", "Flask",
    "FastAPI", "REST API", "GraphQL",

    # Database
    "SQL", "MySQL", "PostgreSQL",
    "MongoDB", "SQLite",

    # DevOps
    "Git", "GitHub", "Docker",
    "Kubernetes", "AWS", "Azure", "GCP",

    # AI
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "NLP",
    "AI",

    # Mobile
    "Flutter",
    "Android",
    "Kotlin",
    
]


def extract_resume_data(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # ---------------- EMAIL ----------------

    email = ""

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email_match:
        email = email_match.group()

    # ---------------- PHONE ----------------

    phone = ""
    
    education = ""
    experience = ""
    projects = []
    certifications = []

    phone_match = re.search(
        r"(\+91[\-\s]?)?[6-9]\d{9}",
        text
    )

    if phone_match:
        phone = phone_match.group()

    # ---------------- SKILLS ----------------

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS_DATABASE:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    # ---------------- EDUCATION ----------------

    education_keywords = [
        "B.Tech",
        "B.E",
        "M.Tech",
        "MCA",
        "BCA",
        "MBA",
        "B.Sc",
        "M.Sc",
        "Diploma",
        "Bachelor",
        "Master"
    ]

    education = ""

    for item in education_keywords:

        if item.lower() in text_lower:
            education = item
            break

    # ---------------- EXPERIENCE ----------------

    experience = ""

    exp_match = re.search(
        r"(\d+)\+?\s*(years|year|yrs|yr)",
        text,
        re.IGNORECASE
    )

    if exp_match:
        experience = exp_match.group()

    # ---------------- PROJECTS ----------------

    projects = []

    project_section = re.search(
        r"Projects?(.*?)(Education|Skills|Experience|Certification|$)",
        text,
        re.I | re.S
    )

    if project_section:

        lines = project_section.group(1).split("\n")

        for line in lines:

            line = line.strip()

            if len(line) > 5:
                projects.append(line)

    # ---------------- CERTIFICATIONS ----------------

    certifications = []

    cert_section = re.search(
        r"Certifications?(.*?)(Projects|Education|Experience|$)",
        text,
        re.I | re.S
    )

    if cert_section:

        lines = cert_section.group(1).split("\n")

        for line in lines:

            line = line.strip()

            if len(line) > 3:
                certifications.append(line)

    return {

        "email": email,

        "phone": phone,

        "skills": ", ".join(found_skills),

        "education": education,

        "experience": experience,

        "projects": projects,

        "certifications": certifications,

        "text": text,

    }
