import fitz  # PyMuPDF
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os

from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HUGGING_FACE_API_KEY")

login(token=token)

def extract_resume_text(pdf_path="resume.pdf"):
    try:
        print('📄 Reading resume...')
        doc = fitz.open(pdf_path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"❌ Error reading resume: {e}")
        return "Error: Unable to read resume."


def load_llm_pipeline(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    try:    
        print('🧠 Loading TinyLlama...1')
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        print('🧠 Loading TinyLlama...2')
        model = AutoModelForCausalLM.from_pretrained(model_id)
        print('🧠 Loading TinyLlama...3')
        return pipeline("text-generation", model=model, tokenizer=tokenizer)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def generate_cover_letter(job_title, company, description, resume_text, generator):
    print('generating_cover_letter')
    prompt = f"""### Instruction:
Using the resume below, write a precise and professional 3-paragraph cover letter tailored for the given job.

### Resume:
{resume_text}

### Job Title:
{job_title}

### Company:
{company}

### Job Description:
{description}

### Response:"""

    output = generator(
        prompt,
        max_new_tokens=350,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

    result = output[0]["generated_text"].split("### Response:")[-1].strip()
    return result

def save_letter_to_file(text, file_name="cover_letter.txt"):
    with open(file_name, "w") as f:
        f.write(text)
    print(f"📄 Cover letter saved to {file_name}")

# ----- Usage -----

if __name__ == "__main__":
    # Load your resume from PDF
    resume_text = extract_resume_text("resume.pdf")

    # Sample job info
    job = {
        "title": "Data Science Intern",
        "company": "Seurat Technologies",
        "description": "We are seeking a data science intern with experience in Python, ML, and data analysis for summer 2025. Strong communication and SQL skills are a plus."
    }

    # Load the LLM
    generator = load_llm_pipeline()

    # Generate the cover letter
    letter = generate_cover_letter(
        job_title=job["title"],
        company=job["company"],
        description=job["description"],
        resume_text=resume_text,
        generator=generator
    )

    print("\n📬 Your Cover Letter:\n")
    print(letter)

    # Save it
    save_letter_to_file(letter, file_name="cover_letter_seurat.txt")
