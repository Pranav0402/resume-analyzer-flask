from sentence_transformers import SentenceTransformer, util
import re

# ================= CONFIG =================
MODEL_NAME = "all-mpnet-base-v2"
model = SentenceTransformer(MODEL_NAME)

UNMATCHED_THRESHOLD = 0.35

ROLE_SKILLS = {
    "web developer": [
        "html", "css", "javascript", "react", "node",
        "express", "mongodb", "sql", "git", "api"
    ],
    "ai engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "nlp", "computer vision"
    ],
    "data scientist": [
        "python", "pandas", "numpy", "sql",
        "scikit-learn", "data analysis"
    ]
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


def build_suggestions(components, unmatched):
    suggestions = []

    if components.get("skills", 100) < 70:
        suggestions.append(
            "Add or emphasize more role-specific technical skills mentioned in the job description."
        )

    if components.get("experience", 100) < 60:
        suggestions.append(
            "Rewrite project or experience bullets to closely match job responsibilities."
        )

    if components.get("keywords", 100) < 70:
        suggestions.append(
            "Include exact job description keywords naturally in your resume."
        )

    if components.get("education", 100) == 0:
        suggestions.append(
            "Clearly mention your degree, certifications, or relevant coursework."
        )

    if unmatched:
        suggestions.append(
            f"Consider adding or strengthening these missing skills: {', '.join(unmatched[:5])}."
        )

    return suggestions


# ================= MAIN =================
def calculate_semantic_ats_score(resume_text, job_description):
    resume = clean_text(resume_text)
    jd = clean_text(job_description)

    # --------------------------------------------------
    # ROLE-ONLY ATS
    # --------------------------------------------------
    if len(jd.split()) <= 4 and jd in ROLE_SKILLS:
        role_skills = ROLE_SKILLS[jd]
        matched = [s for s in role_skills if s in resume]
        missing = [s for s in role_skills if s not in matched]

        score = (len(matched) / len(role_skills)) * 100

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

    # --------------------------------------------------
    # FULL JD ATS
    # --------------------------------------------------
    resume_chunks = split_chunks(resume)
    jd_chunks = split_chunks(jd)

    if not resume_chunks or not jd_chunks:
        return {
            "score": 0.0,
            "components": {},
            "matched_pairs": [],
            "unmatched": [],
            "suggestions": ["Provide a detailed job description for better ATS evaluation."]
        }

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

    jd_tokens = set(re.findall(r"\b[a-zA-Z]{3,}\b", jd))
    resume_tokens = set(re.findall(r"\b[a-zA-Z]{3,}\b", resume))
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
        "unmatched": unmatched_chunks,
        "suggestions": build_suggestions(components, unmatched_chunks)
    }
