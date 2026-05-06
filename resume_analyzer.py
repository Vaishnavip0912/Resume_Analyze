import streamlit as st
import PyPDF2

# -------- PDF TEXT EXTRACTION --------
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    
    return text.lower()


# -------- SKILL DATABASE --------
skills_db = [
    "python", "java", "c++", "ai", "machine learning",
    "deep learning", "sql", "firebase", "javascript",
    "html", "css", "react", "node", "api"
]


# -------- AGENTS --------
def extract_skills(resume):
    return [skill for skill in skills_db if skill in resume]

def match_skills(resume_skills, job_skills):
    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]
    return matched, missing

def calculate_score(matched, job_skills):
    if len(job_skills) == 0:
        return 0
    return round((len(matched) / len(job_skills)) * 10, 2)

def suggest(score, missing):
    if score < 5:
        return f"Low match. Add skills: {missing}"
    elif score < 8:
        return f"Good profile. Improve by adding: {missing}"
    else:
        return "Strong profile. Well aligned with job role."


# -------- UI --------
st.title("📄 AI Resume Analyzer (ATS + Agent System)")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if uploaded_file and job_desc:
    st.success("File uploaded successfully ✅")

    resume_text = extract_text_from_pdf(uploaded_file)

    # Extract job skills
    job_skills = [skill for skill in skills_db if skill in job_desc.lower()]

    if st.button("Analyze Resume"):
        st.write("\n[AI Agent Processing...]\n")

        resume_skills = extract_skills(resume_text)
        matched, missing = match_skills(resume_skills, job_skills)
        score = calculate_score(matched, job_skills)
        advice = suggest(score, missing)

        st.subheader("📊 Results")

        st.write("**Resume Skills:**", resume_skills)
        st.write("**Job Required Skills:**", job_skills)

        st.write("**Matched Skills:**", matched)
        st.write("**Missing Skills:**", missing)

        st.write("**ATS Score:**", score, "/10")

        st.write("**Suggestion:**", advice)