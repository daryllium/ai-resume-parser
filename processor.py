from ollama import chat
from pymupdf4llm import to_markdown

from models import ResumeData

from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def process_resume_file(file_path, job_description):
    # 1. Extract Text
    resume_text = to_markdown(file_path)

    # 2. Setup Prompt
    prompt = f"""
        You are an expert recruiter. Compare the resume text against the job description.
        
        Resume Text: {resume_text}
        Job Description: {job_description}

        INSTRUCTIONS:
        1. SUMMARY: Write a 2-3 sentence professional overview of the candidate's background.
        2. MATCH_SCORE: Provide an integer (0-100) based on how well their skills match the JD.
        3. MISSING_SKILLS: List specific technical or soft skills mentioned in the JD that are NOT in the resume.
        4. FIT_EXPLANATION: Provide a detailed paragraph explaining why they are or are not a good fit.
        5. DATA FORMAT: Return ONLY a JSON object matching the requested schema. Do not leave any fields empty.
        """
    
    # 3. Call LLM
    response = chat(model="llama3.2", messages=[
        {
            'role': "user",
            'content': prompt,
        }
    ],format=ResumeData.model_json_schema())

    # 4. Validate and Return Response
    validated_model = ResumeData.model_validate_json(response['message']['content'])
    return validated_model

def generate_pdf_report(data, output_path):
    # Setup the document
    doc = SimpleDocTemplate(output_path, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"Analysis Report: {data.name}", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Match Score with color logic
    score_style = ParagraphStyle(
        'ScoreStyle',
        parent=styles['Heading2'],
        textColor=colors.green if data.match_score > 60 else colors.red
    )
    story.append(Paragraph(f"Match Score: {data.match_score}%", score_style))
    story.append(Spacer(1, 12))

    # Sections
    sections = [
        ("Executive Summary", data.summary),
        ("Missing Skills", ", ".join(data.missing_skills) if isinstance(data.missing_skills, list) else data.missing_skills),
        ("Job Fit Analysis", data.fit_explanation)
    ]

    for title, content in sections:
        story.append(Paragraph(title, styles['Heading3']))
        clean_content = str(content) if content else "None"
        story.append(Paragraph(clean_content, styles['BodyText']))
        story.append(Spacer(1, 12))

    # Build the file
    doc.build(story)