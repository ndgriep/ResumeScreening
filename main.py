from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from text_extractor import extract_text
from grade_scale import compute_similarity
from requirements_matcher import compare_requirements


app = FastAPI()

# Enable CORS (for frontend to make requests to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# Serve the upload form on the root path
@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# Process uploaded resume and job description files
@app.post("/compare/")
async def compare_resume_job(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...)
):
    resume_bytes = await resume.read()
    jd_bytes = await job_description.read()

    resume_str = extract_text(resume_bytes, resume.filename)
    jd_str = extract_text(jd_bytes, job_description.filename)

    resume_words = set(resume_str.lower().split())
    jd_words = set(jd_str.lower().split())
    match_score = compute_similarity(resume_str, jd_str)
    missing = compare_requirements(jd_str, resume_str)

    #match_score = len(resume_words & jd_words) / max(len(jd_words), 1) * 100

    return {
        "match_score": f"{match_score:.2f}%",
        "missing_requirements": missing,
        "message": "Comparison complete."
    }
