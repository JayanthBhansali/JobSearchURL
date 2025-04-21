import streamlit as st
import json
from generate_cover_letter import generate_cover_letter


import sys
print("🔍 Running Python from:", sys.executable)


st.header('Cover Letter Generator')

with open("jobright_jobs.json", "r") as f:
    jobs = json.load(f)

job_description = {}

job_title = st.selectbox("Select Job Title", [job['title']+'-'+job['company'] for job in jobs])
job_location = st.text_input("Location:", [job['location'] for job in jobs if job['title']+'-'+job['company'] == job_title][0])
job_application_url = st.text_input("Application URL:", [job['application_url'] for job in jobs if job['title']+'-'+job['company'] == job_title][0])
job_keyword = st.text_input("Keyword:", [job['keyword'] for job in jobs if job['title']+'-'+job['company'] == job_title][0])

st.subheader("Generate Cover Letter")

job_description = st.text_area("Job Description", f"Paste the job description of {job_title} here...")

if st.button("Generate Cover Letter"):
    # Here you would call your LLM function to generate the cover letter
    # For now, we will just simulate it with a placeholder text
    cover_letter = generate_cover_letter(job_title, job_description)

    st.text_area("Generated Cover Letter", cover_letter, height=300)
st.write("---")

