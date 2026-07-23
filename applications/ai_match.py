import re


def normalize(skill):
    skill = skill.lower().strip()

    replacements = {
        "react.js": "react",
        "reactjs": "react",
        "node.js": "node",
        "nodejs": "node",
        "express.js": "express",
        "expressjs": "express",
        "mongodb": "mongodb",
        "mongo db": "mongodb",
        "javascript": "javascript",
        "js": "javascript",
        "machine learning": "ml",
        "artificial intelligence": "ai",
    }

    return replacements.get(skill, skill)


def calculate_match_score(job_skills, resume_skills):

    if not job_skills or not resume_skills:
        return 0, [], []

    job_list = [
        normalize(i)
        for i in re.split(r",|\n", job_skills)
        if i.strip()
    ]

    resume_list = [
        normalize(i)
        for i in re.split(r",|\n", resume_skills)
        if i.strip()
    ]

    matched = []
    missing = []

    for skill in job_list:
        if skill in resume_list:
            matched.append(skill.title())
        else:
            missing.append(skill.title())

    score = round((len(matched) / len(job_list)) * 100)

    return score, matched, missing