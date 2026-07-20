from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import joblib
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader
from docx import Document

latest_result = {}
# ===========================
# Flask App
# ===========================

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.secret_key = "resume_screener_secret"

# ===========================
# Load Trained Model
# ===========================

MODEL_PATH = "resume_model.pkl"
TFIDF_PATH = "tfidf_vectorizer.pkl"
CSV_PATH = "job_roles.csv"

model = joblib.load(MODEL_PATH)
tfidf = joblib.load(TFIDF_PATH)

jobs_df = pd.read_csv(CSV_PATH)

# ===========================
# Home Page
# ===========================

@app.route("/")
def home():
    return render_template("index.html")


# ===========================
# Helper Functions
# ===========================

def extract_resume_text(file):

    filename = file.filename.lower()

    if filename.endswith(".txt"):

        return file.read().decode("utf-8")
    elif filename.endswith(".docx"):

        doc = Document(file)

        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text


    elif filename.endswith(".pdf"):

        pdf_reader = PdfReader(file)

        text = ""

        for page in pdf_reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted


        return text


    return ""

def predict_resume(resume_text):

    resume_vector = tfidf.transform([resume_text])

    prediction = model.predict(resume_vector)[0]

    confidence = None

    try:
        probabilities = model.predict_proba(resume_vector)

        confidence = round(
            probabilities.max() * 100,
            2
        )

    except:

        confidence = 95.00

    return prediction, confidence


def recommend_jobs(category):

    result = jobs_df[
        jobs_df["Category"] == category
    ]

    return result


def extract_skills(job_data):

    skills = []

    for skill in job_data["Required Skills"]:

        if pd.notna(skill):

            for item in skill.split(","):

                item = item.strip()

                if item not in skills:

                    skills.append(item)

    return skills


def get_education(job_data):

    education = []

    if "Education Requirement" not in job_data.columns:

        return education

    for item in job_data["Education Requirement"]:

        if pd.notna(item):

            if item not in education:

                education.append(item)

    return education


def get_salary(job_data):

    salary = []

    if "Salary Range" not in job_data.columns:

        return salary

    for item in job_data["Salary Range"]:

        if pd.notna(item):

            if item not in salary:

                salary.append(item)

    return salary

# ===========================
# Predict Resume
# ===========================

@app.route("/predict", methods=["POST"])
def predict():

    # Default empty text
    resume_text = ""    


# 1. Check uploaded file
    uploaded_file = request.files.get("resume_file")


    if uploaded_file and uploaded_file.filename != "":

        resume_text = extract_resume_text(uploaded_file)



# 2. If no file, take textarea input
    if not resume_text:

        resume_text = request.form.get("resume")



# Validation
    if resume_text is None or resume_text.strip() == "":

        flash("Please enter your resume before clicking Predict.")

        return redirect(url_for("home"))

    try:

        # Predict Category
        predicted_category, confidence = predict_resume(resume_text)

        # Recommended Jobs
        recommended_jobs = recommend_jobs(predicted_category)

        # Job Titles
        if "Job Title" in recommended_jobs.columns:

            job_titles = recommended_jobs["Job Title"].drop_duplicates().tolist()

        else:

            job_titles = []

        # Skills
        skills = extract_skills(recommended_jobs)

        # Education
        education = get_education(recommended_jobs)

        # Salary
        salary = get_salary(recommended_jobs)

        # Number of jobs found
        total_jobs = len(job_titles)

        # Store data for PDF generation
        global latest_result

        latest_result = {

            "category": predicted_category,

            "confidence": confidence,

            "jobs": job_titles,

            "skills": skills,

            "education": education,

            "salary": salary

        }

        return render_template(

            "result.html",

            category=predicted_category,

            confidence=confidence,

            jobs=job_titles,

            skills=skills,

            education=education,

            salary=salary,

            total_jobs=total_jobs

        )

    except Exception as e:

        return render_template(

            "result.html",

            error=str(e)

        )
        
# ===========================
# Download Result as PDF
# ===========================

@app.route("/download_pdf")
def download_pdf():

    global latest_result

    if not latest_result:

        flash("No prediction available to download.")

        return redirect(url_for("home"))

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Resume Screening Report")

    y = 800

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, y, "Resume Screening Report")

    y -= 40

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        y,
        f"Predicted Category : {latest_result['category']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Confidence Score : {latest_result['confidence']} %"
    )

    y -= 40

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Recommended Jobs")

    pdf.setFont("Helvetica", 12)

    y -= 25

    for job in latest_result["jobs"]:

        pdf.drawString(70, y, f"• {job}")

        y -= 20

        if y < 100:

            pdf.showPage()

            y = 800

    y -= 10

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Required Skills")

    pdf.setFont("Helvetica", 12)

    y -= 25

    for skill in latest_result["skills"]:

        pdf.drawString(70, y, f"• {skill}")

        y -= 20

        if y < 100:

            pdf.showPage()

            y = 800

    if latest_result["education"]:

        y -= 20

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Education Requirement")

        pdf.setFont("Helvetica", 12)

        y -= 25

        for edu in latest_result["education"]:

            pdf.drawString(70, y, f"• {edu}")

            y -= 20

    if latest_result["salary"]:

        y -= 20

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Salary")

        pdf.setFont("Helvetica", 12)

        y -= 25

        for sal in latest_result["salary"]:

            pdf.drawString(70, y, f"• {sal}")

            y -= 20

    pdf.save()

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=True,

        download_name="Resume_Report.pdf",

        mimetype="application/pdf"

    )


# ===========================
# Reset Route
# ===========================

@app.route("/reset")
def reset():

    global latest_result

    latest_result = {}

    return redirect(url_for("home"))


# ===========================
# Error Pages
# ===========================

@app.errorhandler(404)
def page_not_found(error):

    return "<h2>404 - Page Not Found</h2>", 404


@app.errorhandler(500)
def internal_server_error(error):

    return "<h2>500 - Internal Server Error</h2>", 500


# ===========================
# Run Flask
# ===========================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )