from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from text_extract import extract_text
from gemini_analyzer import initialize_api, extract_resume_info, analyze_resume_against_job
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...)
):
    resume_bytes = await resume.read()
    jd_bytes = await job_description.read()

    resume_str = extract_text(resume_bytes, resume.filename)
    jd_str = extract_text(jd_bytes, job_description.filename)

    model = initialize_api()
    resume_data = extract_resume_info(resume_str, model)
    if not resume_data or "error" in resume_data:
        return {"error": "Resume analysis failed.", "raw": resume_data.get("raw_response", "")}

    analysis = analyze_resume_against_job(resume_data, jd_str, model)
    return analysis
