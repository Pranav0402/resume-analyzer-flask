import csv
from collections import defaultdict


MIN_MATCH_PERCENT = 30.0  # 🔒 filter weak roles


def normalize(skill):
    skill = skill.lower().strip()
    mapping = {
        "js": "javascript",
        "react.js": "react",
        "node.js": "node",
        "py": "python",
        "c++": "c++",
        "ml": "machine learning",
        "ai": "artificial intelligence"
    }
    return mapping.get(skill, skill)


def run_job_matching_analysis(resume_text, csv_path):
    resume_text = resume_text.lower()

    prof_skills = defaultdict(set)

    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for s in row["Skills"].split(","):
                prof_skills[row["Profession"]].add(normalize(s))

    results = []
    detected_skills = set()

    for profession, skills in prof_skills.items():
        matched = {s for s in skills if s in resume_text}

        if not matched:
            continue

        match_percent = (len(matched) / len(skills)) * 100

        # 🚫 FILTER WEAK MATCHES
        if match_percent < MIN_MATCH_PERCENT:
            continue

        detected_skills |= matched

        results.append({
            "profession": profession,
            "match_percent": round(match_percent, 1),
            "match_count": len(matched),
            "total_skills": len(skills)
        })

    results.sort(key=lambda x: x["match_percent"], reverse=True)

    return {
        "matches": results[:5],   # top roles only
        "skills": sorted(detected_skills)
    }
