import pdfplumber
import re


def extract_resume_data(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    email = ""

    phone = ""

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email_match:
        email = email_match.group()

    phone_match = re.search(
        r"\+?\d[\d\s\-]{8,15}",
        text
    )

    if phone_match:
        phone = phone_match.group()

    skills = []

    keywords = [
        "Python",
        "Django",
        "Flask",
        "Java",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node",
        "Git",
        "Docker",
        "AWS"
    ]

    for skill in keywords:

        if skill.lower() in text.lower():
            skills.append(skill)

    return {

        "email": email,

        "phone": phone,

        "skills": ", ".join(skills),

        "text": text

    }