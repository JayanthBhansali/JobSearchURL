from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
template = """### Instruction:
Using my resume below, write a precise and professional 3-paragraph cover letter tailored for the given job.
The cover letter should be concise, engaging, and highlight my skills and experiences relevant to the job description.

### Resume:
{resume_text}

### Job Title - Company:
{job_title_company}

### Job Description:
{description}
""",
    input_variables=["resume_text", "job_title_company", "description"],
    output_parser=None,
    partial_variables={},
    template_format="f-string",
    validate_template=True,
    template_name="cover_letter_template",
)

template.save("cover_letter_template.json")