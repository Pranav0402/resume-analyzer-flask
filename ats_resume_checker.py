import re

def analyze_resume_ats(resume_text):
    text = resume_text.lower()

    score = 100
    issues = []
    suggestions = []

    # -------- SECTION CHECKS --------
    sections = {
        "skills": "skills",
        "education": "education",
        "experience": "experience",
        "project": "project"
    }

    for name, key in sections.items():
        if key not in text:
            score -= 10
            issues.append(f"Missing '{name.capitalize()}' section")
            suggestions.append(f"Add a clear '{name.capitalize()}' section")

    # -------- LENGTH CHECK --------
    word_count = len(text.split())
    if word_count < 250:
        score -= 10
        issues.append("Resume is too short")
        suggestions.append("Add more project or experience details")

    if word_count > 800:
        score -= 10
        issues.append("Resume is too long")
        suggestions.append("Keep resume concise (1 page preferred)")

    # -------- FORMAT CHECK --------
    if re.search(r"\|_|={3,}", resume_text):
        score -= 10
        issues.append("Complex formatting detected")
        suggestions.append("Avoid tables and complex layouts for ATS")

    score = max(score, 0)

    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions
    }
