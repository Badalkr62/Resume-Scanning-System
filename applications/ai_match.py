import re


def calculate_match_score(job_skills, resume_skills):

    if not job_skills or not resume_skills:
        return 0, [], []

    job_list = [
        skill.strip().lower()
        for skill in re.split(r",|\n", job_skills)
        if skill.strip()
    ]

    resume_list = [
        skill.strip().lower()
        for skill in re.split(r",|\n", resume_skills)
        if skill.strip()
    ]

    matched = []

    missing = []

    for skill in job_list:

        if skill in resume_list:
            matched.append(skill.title())
        else:
            missing.append(skill.title())

    score = int((len(matched) / len(job_list)) * 100) if job_list else 0

    return score, matched, missing
