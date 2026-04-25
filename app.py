from flask import Flask, request, render_template, jsonify, redirect, url_for
from PyPDF2 import PdfReader
from docx import Document
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

from job_matching import run_job_matching_analysis
from enhanced_resume import generate_resume_summary
from semantic_ats import calculate_semantic_ats_score
from ats_resume_checker import analyze_resume_ats

app = Flask(__name__)
RESULT_STORE = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFESSION_CSV = os.path.join(BASE_DIR, "profession.csv")


# ---------------- FILE TEXT EXTRACTION ----------------
def extract_text_from_file(file):
    name = file.filename.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join(p.extract_text() or "" for p in reader.pages)

    if name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    raise ValueError("Unsupported file format")


# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- ANALYZE ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files.get("resume")
    jd = request.form.get("job_description", "").strip()
    analysis_type = request.form.get("analysis_type")

    if not resume or resume.filename == "":
        return jsonify({"error": "Resume required"}), 400

    resume_text = extract_text_from_file(resume)
    if len(resume_text) < 50:
        return jsonify({"error": "Resume text too short"}), 400

    rid = str(uuid.uuid4())

    # ---------------- JOB PREDICTION ----------------
    if analysis_type == "job_prediction":
        result = run_job_matching_analysis(resume_text, PROFESSION_CSV)
        RESULT_STORE[rid] = {"type": "job", "data": result}
        return jsonify({"redirect": url_for("results", rid=rid, view="job")})

    # ---------------- ATS COMPATIBILITY ----------------
    if analysis_type == "ats_match":
        if not jd:
            return jsonify({"error": "Job description required"}), 400

        result = calculate_semantic_ats_score(resume_text, jd.lower())
        RESULT_STORE[rid] = {"type": "ats", "data": result}
        return jsonify({"redirect": url_for("results", rid=rid, view="ats")})

    # ---------------- ATS RESUME CHECKER ----------------
    if analysis_type == "resume_ats":
        result = analyze_resume_ats(resume_text)
        RESULT_STORE[rid] = {"type": "resume_ats", "data": result}
        return jsonify({"redirect": url_for("results", rid=rid, view="resume_ats")})

    # ---------------- RESUME SUMMARY ----------------
    if analysis_type == "resume_summary":
        structure, formatting = generate_resume_summary(resume_text)
        RESULT_STORE[rid] = {
            "type": "summary",
            "data": {"structure": structure, "formatting": formatting}
        }
        return jsonify({"redirect": url_for("results", rid=rid, view="summary")})

    return jsonify({"error": "Invalid analysis type"}), 400



# ---------------- RESULTS (TABS) ----------------
@app.route("/results")
def results():
    rid = request.args.get("rid")
    view = request.args.get("view")

    if rid not in RESULT_STORE:
        return redirect(url_for("index"))

    payload = RESULT_STORE[rid]
    data = payload["data"]

    if view == "job":
        return render_template(
            "job_results.html",
            result=data,
            active_tab="job"
        )

    if view == "ats":
        return render_template(
            "ats_score_results.html",
            result=data,
            show_pairs=True,
            show_missing=True,
            active_tab="ats"
        )

    if view == "resume_ats":
        return render_template(
            "ats_resume_checker.html",
            result=data,
            active_tab="resume_ats"
        )

    if view == "summary":
        return render_template(
            "resume_summary.html",
            result=data,
            active_tab="summary"
        )

    return redirect(url_for("index"))



# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
