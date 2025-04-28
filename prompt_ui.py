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
# Display job details
selected_job = next(job for job in jobs if job['title']+'-'+job['company'] == job_title)

with st.expander("Job Details", expanded=True):
    st.write(f"📍 Location: {selected_job['location']}")
    st.write(f"🔗 Apply Here: {selected_job['application_url']}")
    st.write(f"🧠 Keyword Focus: {selected_job['keyword']}")

st.subheader("Generate Cover Letter")

job_description = st.text_area("Job Description", f"Paste the job description of {job_title} here...")

if not job_description.strip():
    st.warning("Please paste the job description before generating.")
else:
    cover_letter = generate_cover_letter(job_title, job_description)
    st.text_area("Generated Cover Letter", cover_letter, height=300)

if st.button("Generate Cover Letter"):
    # Here you would call your LLM function to generate the cover letter
    # For now, we will just simulate it with a placeholder text
    if not job_description.strip():
        st.warning("Please paste the job description before generating.")
    else:
        cover_letter = generate_cover_letter(job_title, job_description)
        st.text_area("Generated Cover Letter", cover_letter, height=300)

st.write("---")



st.title("💬 Chat with AI Assistant")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

# Take user input
user_input = st.chat_input("Say something...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Simulate bot response (replace with your AI model)
    response = f"You said: {user_input}"  # Replace with your model's output
    st.chat_message("assistant").write(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
