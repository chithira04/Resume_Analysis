from flask import Flask, render_template, request
import pickle
import os
import pandas as pd

from utils.resume_parser import extract_text


app = Flask(__name__)

# Load ML model
model = pickle.load(open("model/knn_model.pkl","rb"))
tfidf = pickle.load(open("model/tfidf.pkl","rb"))

# Load job database
jobs = pd.read_csv("job_roles.csv")

# Home page
@app.route("/")
def home():
    return render_template( "index.html")

# Prediction
@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["resume"]

    if file.filename == "":
        return "No file selected"
    path = os.path.join("uploads",file.filename)
    file.save(path)

    # Extract resume text
    resume_text = extract_text(path)

    # Convert text to vector
    vector = tfidf.transform([resume_text])

    # Predict category
    category = model.predict(vector)[0]

    # Job recommendation
    recommended_jobs = jobs[jobs["Category"] == category ]
    job_list = recommended_jobs["Job Title"].head(5).tolist()
    # required_skills = set()

    # for skills in recommended_jobs["Required Skills"]:
    #     if pd.notna(skills):
    #         for skill in skills.split(","):
    #             required_skills.add(skill.strip().lower())
    best_job = recommended_jobs.iloc[0]

    required_skills = {
    skill.strip().lower()
    for skill in best_job["Required Skills"].split("|")
}
    candidate_skills = [
    "python", "java", "c", "c++", "sql", "mysql",
    "flask", "django", "html", "css", "javascript",
    "pandas", "numpy", "matplotlib", "seaborn",
    "machine learning", "deep learning", "tensorflow",
    "keras", "pytorch", "scikit-learn", "nlp",
    "power bi", "excel", "tableau", "git", "github",
    "aws", "docker"
]
    candidate_skills = set(skill.lower() for skill in candidate_skills)
    matched_skills = sorted(candidate_skills & required_skills)

    missing_skills = sorted(required_skills - candidate_skills)
    if len(required_skills) > 0:
        fit_score = round(
            (len(matched_skills) / len(required_skills)) * 100
        )
    else:
        fit_score = 0
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Learn {skill.title()}")

    if fit_score < 50:
        suggestions.append("Complete beginner-level projects.")
        suggestions.append("Take online certification courses.")
    elif fit_score < 75:
        suggestions.append("Build advanced portfolio projects.")
        suggestions.append("Practice coding interview questions.")
    else:
        suggestions.append("Your resume is strong for this role.")
        suggestions.append("Start applying for relevant jobs.")
    return render_template("result.html",category=category,jobs=job_list,resume=resume_text[:500],fit_score=fit_score,
    matched_skills=matched_skills,
    missing_skills=missing_skills,
    suggestions=suggestions)


if __name__=="__main__":
    app.run(debug=True)



# Resume PDF
#       ↓
# Load tfidf.pkl
#       ↓
# Convert resume into TF-IDF vector
#       ↓
# Load knn_model.pkl
#       ↓
# Predict Job Category