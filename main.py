import os
import shutil
from fastapi import BackgroundTasks, FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from processor import process_resume_file, generate_pdf_report

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    content = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; text-align: center; padding: 50px; background-color: #f7fafc; }
            .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; width: 80%; max-width: 600px; }
            textarea { width: 100%; border: 1px solid #cbd5e0; border-radius: 4px; padding: 10px; margin-bottom: 20px; }
            
            /* The Spinner CSS */
            .loader {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #3498db;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 2s linear infinite;
                display: none; /* Hidden by default */
                margin: 20px auto;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            
            input[type="submit"] {
                background: #3182ce; color: white; border: none; padding: 10px 20px; 
                border-radius: 4px; cursor: pointer; font-size: 16px;
            }
            input[type="submit"]:disabled { background: #a0aec0; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>AI Resume Analyzer</h2>
            <form id="analyzeForm" action="/upload" enctype="multipart/form-data" method="post" onsubmit="showLoading()">
                <textarea name="jd" placeholder="Paste Job Description here..." rows="10" required></textarea><br>
                <input name="file" type="file" required><br><br>
                
                <input type="submit" id="submitBtn" value="Analyze Resume">
                
                <div id="loader" class="loader"></div>
                <p id="loadingText" style="display:none; color: #4a5568;">AI is analyzing... please wait.</p>
            </form>
        </div>

        <script>
            function showLoading() {
                // Hide button, show spinner
                document.getElementById('submitBtn').disabled = true;
                document.getElementById('loader').style.display = 'block';
                document.getElementById('loadingText').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=content)


@app.post("/upload")
async def upload_resume(
    request: Request, file: UploadFile = File(...), jd: str = Form(...)
):
    # 1. Save the file temporarily
    temp_name = f"temp_{file.filename}"
    with open(temp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 2. Run your AI logic
        data = process_resume_file(temp_name, jd)
        print(f"DEBUG AI DATA: {data}")

        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "name": data.name,
                "email": data.email,
                "skills": data.skills,
                "years_experience": data.years_experience,
                "match_score": data.match_score,
                "summary": data.summary,
                "missing_skills": data.missing_skills,
                "fit_explanation": data.fit_explanation,
            },
        )
    finally:
        # 3. Clean up the file
        if os.path.exists(temp_name):
            os.remove(temp_name)


@app.post("/download-report")
async def download_report(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    score: int = Form(...),
    summary: str = Form(...),
    fit: str = Form(...),
    missing: str = Form(""),
):
    report_path = f"report_{name.replace(' ', '_')}.pdf"

    # Convert the URL string back into a Python list
    missing_list = missing.split("||") if (missing and missing != "None") else []

    # Local class to structure data for the PDF generator
    class PDFData:
        def __init__(self, name, match_score, summary, missing_skills, fit_explanation):
            self.name = name
            self.match_score = match_score
            self.summary = summary
            self.missing_skills = missing_skills
            self.fit_explanation = fit_explanation

    # Use NAMED arguments to ensure data goes to the correct field
    data_to_print = PDFData(
        name=name,
        match_score=score,
        summary=summary,
        missing_skills=missing_list,
        fit_explanation=fit,
    )

    # Generate the PDF file
    generate_pdf_report(data_to_print, report_path)

    # 1. Define a small function to remove the file
    def cleanup_file(path: str):
        if os.path.exists(path):
            os.remove(path)

    # 2. Tell FastAPI to run this AFTER the response is sent
    background_tasks.add_task(cleanup_file, report_path)

    # 3. Return the file
    return FileResponse(path=report_path, filename=f"{name}_Analysis.pdf")


# Run with: uvicorn main:app --reload
