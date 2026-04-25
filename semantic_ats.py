from sentence_transformers import SentenceTransformer, util
import re

# ================= MODEL =================
MODEL_NAME = "all-mpnet-base-v2"
model = SentenceTransformer(MODEL_NAME)

UNMATCHED_THRESHOLD = 0.35

# ================= HARD-CODED ROLE FALLBACK =================
ROLE_SKILLS = {
    "web developer": [
        "html", "css", "javascript", "react",
        "node", "express", "mongodb", "sql", "git", "api"
    ],
    "ai engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "nlp", "computer vision"
    ],
    "data scientist": [
        "python", "pandas", "numpy",
        "sql", "scikit-learn", "data analysis"
    ],
    "devops engineer": [
        "docker", "kubernetes", "aws",
        "ci cd", "jenkins", "linux", "terraform"
    ]
}

# ================= TOKEN FILTERS =================
GENERIC_TERMS = {
    "developer", "engineer", "analyst", "intern", "fresher",
    "software", "web", "fullstack", "backend", "frontend",
    "role", "position", "job", "work", "experience",
    "skills", "knowledge", "responsibilities", "requirements"
}

STOPWORDS = {
    "and", "the", "with", "for", "this", "that",
    "will", "have", "team", "ability", "strong"
}

# ================= HELPERS =================
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+#]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def split_chunks(text: str, min_len=10):
    return [
        c.strip()
        for c in re.split(r"[.\n!?;]+", text)
        if len(c.strip()) >= min_len
    ]


def extract_general_skills(text: str):
    """
    Dynamic skill extraction.
    Returns a set of valid skill-like tokens.
    """
    tokens = re.findall(r"\b[a-zA-Z+#]{3,}\b", text.lower())
    return {
        t for t in tokens
        if t not in STOPWORDS and t not in GENERIC_TERMS
    }


def build_suggestions(components, missing):
    suggestions = []

    if components.get("skills", 100) < 70:
        suggestions.append("Add more role-specific technical skills.")

    if components.get("experience", 100) < 60:
        suggestions.append("Rewrite project descriptions to align with job responsibilities.")

    if components.get("keywords", 100) < 70:
        suggestions.append("Include exact job description keywords naturally.")

    if components.get("education", 100) == 0:
        suggestions.append("Clearly mention your degree or certifications.")

    if missing:
        suggestions.append(
            f"Consider adding or strengthening these skills: {', '.join(missing[:5])}."
        )

    return suggestions


# ================= MAIN ATS =================
def calculate_semantic_ats_score(resume_text, job_description):
    resume = clean_text(resume_text)
    jd = clean_text(job_description)

    # ==================================================
    # SHORT JD → HYBRID MODE
    # ==================================================
    if len(jd.split()) <= 4:

        # -------- STEP 1: GENERAL EXTRACTION --------
        jd_skills = extract_general_skills(jd)
        resume_skills = extract_general_skills(resume)

        # -------- STEP 2: FALLBACK TO ROLE SKILLS --------
        if not jd_skills and jd in ROLE_SKILLS:
            jd_skills = set(ROLE_SKILLS[jd])

        matched = sorted(jd_skills & resume_skills)
        missing = sorted(jd_skills - resume_skills)

        # Neutral fallback score
        score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 50.0

        components = {
            "skills": round(score, 1),
            "experience": 0.0,
            "keywords": round(score, 1),
            "education": 0.0
        }

        return {
            "score": round(score, 1),
            "components": components,
            "matched_pairs": [
                {
                    "jd": f"Required skill: {skill}",
                    "resume": f"Found in resume: {skill}",
                    "similarity": 100.0
                }
                for skill in matched
            ],
            "unmatched": missing,
            "suggestions": build_suggestions(components, missing)
        }

    # ==================================================
    # FULL JD → SEMANTIC ATS
    # ==================================================
    resume_chunks = split_chunks(resume)
    jd_chunks = split_chunks(jd)

    resume_emb = model.encode(resume_chunks, convert_to_tensor=True)
    jd_emb = model.encode(jd_chunks, convert_to_tensor=True)

    cosine_scores = util.cos_sim(jd_emb, resume_emb)
    best_scores, best_indices = cosine_scores.max(dim=1)

    matched_pairs = []
    strong_matches = 0
    unmatched_chunks = []

    for i, score in enumerate(best_scores):
        sim = float(score)
        matched_pairs.append({
            "jd": jd_chunks[i],
            "resume": resume_chunks[int(best_indices[i])],
            "similarity": round(sim * 100, 2)
        })

        if sim >= UNMATCHED_THRESHOLD:
            strong_matches += 1
        else:
            unmatched_chunks.append(jd_chunks[i])

    experience_score = strong_matches / len(jd_chunks)

    jd_tokens = extract_general_skills(jd)
    resume_tokens = extract_general_skills(resume)

    keyword_score = (
        len(jd_tokens & resume_tokens) / len(jd_tokens)
        if jd_tokens else 0
    )

    education_score = 1.0 if any(
        k in resume for k in ["bachelor", "b.tech", "degree"]
    ) else 0.0

    components = {
        "skills": round(keyword_score * 100, 1),
        "experience": round(experience_score * 100, 1),
        "keywords": round(keyword_score * 100, 1),
        "education": round(education_score * 100, 1)
    }

    total_score = (
        experience_score * 0.4 +
        keyword_score * 0.3 +
        education_score * 0.3
    ) * 100

    return {
        "score": round(total_score, 1),
        "components": components,
        "matched_pairs": matched_pairs[:8],
        "unmatched": sorted(jd_tokens - resume_tokens),
        "suggestions": build_suggestions(components, sorted(jd_tokens - resume_tokens))
    }
