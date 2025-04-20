import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()


def extract_resume_text(pdf_path="resume.pdf"):
    try:
        print('📄 Reading resume...')
        doc = fitz.open(pdf_path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"❌ Error reading resume: {e}")
        return "Error: Unable to read resume."


def generate_cover_letter(job_title_company, description):
    print('generating_cover_letter')
    # Load your resume from PDF
    resume_text = extract_resume_text("resume.pdf")

    prompt = f"""### Instruction:
    Using my resume below, write a precise and professional 3-paragraph cover letter tailored for the given job.
    The cover letter should be concise, engaging, and highlight my skills and experiences relevant to the job description.

    ### Resume:
    {resume_text}

    ### Job Title - Company:
    {job_title_company}

    ### Job Description:
    {description}

    ### Response:"""

    result = ""

    return result


def save_letter_to_file(text, file_name="cover_letter.txt"):
    with open(file_name, "w") as f:
        f.write(text)
    print(f"📄 Cover letter saved to {file_name}")

# ----- Usage -----

if __name__ == "__main__":

    # Sample job info
    job = {
        "title": "Data Science Intern",
        "company": "Seurat Technologies",
        "description": "We are seeking a data science intern with experience in Python, ML, and data analysis for summer 2025. Strong communication and SQL skills are a plus."
    }

    # Generate the cover letter
    letter = generate_cover_letter(
        job_title=job["title"],
        company=job["company"],
        description=job["description"],
    )

    print("\n📬 Your Cover Letter:\n")
    print(letter)

    # Save it
    save_letter_to_file(letter, file_name="cover_letter_seurat.txt")
