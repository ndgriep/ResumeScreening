import re

def extract_requirements(text: str) -> set:
    requirements = set()

    # Degrees
    if re.search(r"\bmaster'?s\b", text, re.IGNORECASE):
        requirements.add("Master's Degree")
    if re.search(r"\bbachelor'?s\b", text, re.IGNORECASE):
        requirements.add("Bachelor's Degree")

    # Experience
    exp_matches = re.findall(r"\d+\+?\s+years?\s+(?:of\s+)?(?:experience|exp)", text, re.IGNORECASE)
    requirements.update(exp_matches)

    # Simple skill keyword matching (expandable)
    skill_keywords = ["python", "docker", "react", "sql", "tensorflow", "java"]
    for skill in skill_keywords:
        if skill in text.lower():
            requirements.add(skill.capitalize())

    return requirements

def compare_requirements(job_text: str, resume_text: str) -> list:
    job_reqs = extract_requirements(job_text)
    resume_reqs = extract_requirements(resume_text)
    missing = job_reqs - resume_reqs
    return list(missing)
