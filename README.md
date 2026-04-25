Resume Analyzer

An AI-powered Resume Analyzer built using Flask that evaluates resumes based on ATS (Applicant Tracking System) principles, provides scoring, and suggests improvements along with job matching insights.



Features

ATS Score Calculation** – Evaluates resume based on keywords and structure
Semantic Analysis** – Uses NLP techniques for better understanding
Job Matching** – Suggests relevant roles based on resume content
Resume Enhancement** – Provides suggestions to improve resume quality
File Upload Support** – Upload and analyze resumes easily
User-Friendly UI** – Built with Flask templates

---

Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS (Jinja Templates)
* **Libraries:** NLP / Text Processing (custom logic)
* **Data Handling:** CSV (profession dataset)

---

Project Structure

```
resume-analyzer-flask/
│── app.py                  # Main Flask app
│── ats_resume_checker.py   # ATS scoring logic
│── job_matching.py         # Job matching logic
│── enhanced_resume.py      # Resume enhancement module
│── semantic_ats.py         # Semantic analysis
│── courses.py              # Course recommendations
│── templates/              # HTML templates
│── models/                 # ML / logic files (if any)
│── requirements.txt        # Dependencies
│── profession.csv          # Dataset
```

---

Installation & Setup

1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/resume-analyzer-flask.git
cd resume-analyzer-flask
```

2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python app.py
```

5. Open in browser

```
http://127.0.0.1:5000/
```

---

Screenshots (Optional but Recommended)

Add screenshots in a `/screenshots` folder and display them here.

---

Use Cases

* Students improving resumes for placements
* Job seekers optimizing ATS compatibility
* Career guidance and skill suggestions

---

Future Improvements

* Add ML model for better scoring
* Integrate real job APIs
* Resume PDF parsing improvements
* User authentication system

---

Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

Contact

**Pranav Zaware**
GitHub: https://github.com/Pranav0402



Give it a star ⭐ on GitHub!
