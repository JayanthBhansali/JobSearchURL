import fitz  # PyMuPDF
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, load_prompt
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model= 'gemini-1.5-pro', temperature=0.2, max_tokens=2000)

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
    template = load_prompt("cover_letter_template.json")
    prompt = template.invoke({
        "job_title_company": job_title_company, 
        "description": description, 
        "resume_text": resume_text,
    })
    result = model.invoke(prompt)
    print('generated_cover_letter')

    return result.content


def save_letter_to_file(text, file_name="cover_letter.txt"):
    with open(file_name, "w") as f:
        f.write(text)
    print(f"📄 Cover letter saved to {file_name}")

# ----- Usage -----

if __name__ == "__main__":

    # Sample job info
    job = {
        "company-title": "Data Science Intern-Seurat Technologies",
        "description": "We are seeking a data science intern with experience in Python, ML, and data analysis for summer 2025. Strong communication and SQL skills are a plus."
    }

    # Generate the cover letter
    letter = generate_cover_letter(
        job_title_company = job["company-title"],
        description = job["description"],
    )

    print("\n📬 Your Cover Letter:\n")
    print(letter)

    # Save it
    save_letter_to_file(letter, file_name="cover_letter_seurat.txt")
