def generate_resume_summary(text):
    text_l = text.lower()

    structure = []
    formatting = []

    # -------- STRUCTURE RULES --------
    if "professional summary" not in text_l:
        structure.append(
            "Add a 2–3 line professional summary highlighting AI/ML projects, full-stack skills, and academic background."
        )

    if "project" in text_l:
        structure.append(
            "Group all academic projects under a dedicated 'Academic Projects' section and list the most relevant AI/ML projects first."
        )

    if "skills" in text_l:
        structure.append(
            "Reorganize the skills section into clear categories such as Programming Languages, Web Technologies, AI/ML, Tools, and Databases."
        )

    if "certification" in text_l or "certificate" in text_l:
        structure.append(
            "Move certifications to a separate 'Certifications & Achievements' section to improve ATS visibility."
        )

    if "education" in text_l:
        structure.append(
            "Keep the Education section concise and place it after Skills for a fresher profile."
        )

    # -------- FORMATTING RULES --------
    formatting.extend([
        "Use consistent bullet styles across all project descriptions.",
        "Maintain uniform spacing between sections and headings.",
        "Keep font size consistent for section titles and subheadings.",
        "Limit resume length to one page by prioritizing relevant projects and skills."
    ])

    return structure, formatting
