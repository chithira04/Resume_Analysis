# Smart Resume Screener & Job Recommendation Portal-Capstone Project

## Overview

The aim of this project is to build an intelligent and user-friendly web application
that automatically analyzes uploaded resumes using NLP-driven Machine Learning
models and identifies the most suitable job roles for each candidate. Along with
predicting role fit, the system recommends relevant job openings from the
database and highlights key strengths and skill gaps, helping users improve their
career readiness.

This dual-purpose platform not only assists HR professionals by automating the
initial screening process but also empowers job seekers with personalized career
insights, making the hiring process smarter, faster, and more effective for both
sides.

---

## Features

- Upload resume in PDF format
- Extract resume text
- NLP-based text preprocessing
- TF-IDF feature extraction
- Machine Learning-based job category prediction
- Recommend top matching job roles
- Responsive Flask web application
- Bootstrap-based user interface

---

## Technologies Used

### Frontend
- HTML5
- CSS3
- Bootstrap 5

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- TF-IDF Vectorizer
- K-Nearest Neighbors (KNN)

### Libraries
- Pandas
- NumPy
- PyPDF2
- Pickle

---

## Project Structure

```
capstone_project/
│
├── app.py
├── requirements.txt
├── README.md
├── job_roles.csv
│
├── model/
│   ├── knn_model.pkl
│   └── tfidf.pkl
│
├── uploads/
│
├── utils/
│   └── resume_parser.py
│
├── templates/
│   ├── index.html
│   └── result.html
│

```

---

## Dataset

The dataset contains various job categories and related job titles used to train the machine learning model.

Example columns:

- Job Title
- Category
- Education Requirement

---

## Machine Learning Pipeline

```
Resume PDF
      │
      ▼
Text Extraction
      │
      ▼
Text Cleaning
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Machine Learning Model
(KNN)
      │
      ▼
Predicted Job Category
      │
      ▼
Job Recommendation
      │
      ▼
Display Result
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/chithira04/Resume_Analysis
```

Move into the project directory

```bash
cd Resume_Analysis
```

Install the required packages

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000

```
---

## Screenshoot

Are in the screenshots folder.

---

## Model Performance

The following machine learning models were evaluated:

| Model | Accuracy |
|--------|----------|
| Decision Tree | 100% |
| Random Forest | 100% |
| Linear SVM | 100% |
| KNN | 93.85% |
| Logistic Regression | 58.46% |
| Naive Bayes | 36.92% |

For deployment, KNN can be used to predict job categories.

---

## Application Workflow

1. Upload a resume (PDF)
2. Extract resume text
3. Convert text into TF-IDF vectors
4. Predict the job category
5. Display the predicted category
6. Recommend top matching job roles

---

## Future Enhancements

- Skill gap analysis
- Resume match score
- HR dashboard
- Candidate ranking
- Resume support for DOCX format
- Online job API integration
- User authentication
- Resume improvement suggestions

---

## Author

Chithira CV

Aswin George

Anandhakrishnan S

Nandagopal K

---

## License

This project is developed for educational and academic purposes.