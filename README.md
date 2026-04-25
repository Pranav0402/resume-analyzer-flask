# AI Resume Analyzer (Flask + ATS Scoring)

An intelligent Resume Analyzer built with Flask that evaluates resumes using ATS (Applicant Tracking System) principles. It provides a score, matches relevant job roles, and suggests improvements to increase selection chances.

---

Key Highlights

* ATS-based resume scoring using keyword matching
* Semantic analysis for better understanding of resume content
* Job role matching based on skills and domain
* Actionable suggestions to improve resume quality
* Fast and simple web interface using Flask

---

Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS (Jinja Templates)
* **Data Processing:** NLP-based text analysis
* **Dataset:** CSV (profession/job roles)

---

Project Structure

```bash
resume-analyzer-flask/
│── app.py                  # Main Flask application
│── ats_resume_checker.py   # ATS scoring logic
│── job_matching.py         # Job role matching
│── enhanced_resume.py      # Resume improvement suggestions
│── semantic_ats.py         # Semantic analysis
│── courses.py              # Course recommendations
│── templates/              # HTML templates (UI)
│── models/                 # Supporting modules/models
│── requirements.txt        # Dependencies
│── profession.csv          # Dataset
│── README.md
│── .gitignore
```

---

Installation & Setup

Clone the repository

```bash
git clone https://github.com/Pranav0402/resume-analyzer-flask.git
cd resume-analyzer-flask
```

Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open in browser

```
http://127.0.0.1:5000/
```

---

How It Works

1. User uploads a resume
2. System extracts and processes text
3. ATS score is calculated using keyword matching
4. Resume is analyzed semantically
5. Relevant job roles are suggested
6. Improvement tips are generated

---

Screenshots

> Add your screenshots inside a `/screenshots` folder

```
screenshots/
│── home.png
│── upload.png
│── result.png
```

Example:

```md
![Home](screenshots/home.png)
![Result](screenshots/result.png)
```

---

Use Cases

* Students preparing for campus placements
* Job seekers optimizing resumes for ATS systems
* Career guidance and skill gap identification

---

Future Improvements

* Integration with real job APIs (LinkedIn, Indeed)
* Advanced ML model for scoring
* Resume PDF parsing enhancements
* User login & dashboard

---

Contributing

Contributions are welcome. Feel free to fork the repo and submit a pull request.

---

Author

**Pranav Zaware**
GitHub: https://github.com/Pranav0402

---
