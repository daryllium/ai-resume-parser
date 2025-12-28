from pydantic import BaseModel,Field

class ResumeData(BaseModel):
    name: str
    email: str
    skills: list[str]
    years_experience: int
    summary: str
    match_score: int = Field(description="A score from 0-100 based on job description match")
    missing_skills: list[str] = Field(description="Skills required by the job but missing from the resume")
    fit_explanation: str = Field(description="Explanation of why the candidate is a good fit for the job, or why they aren't.")