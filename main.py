from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

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
    resume_text = await resume.read()
    jd_text = await job_description.read()

    resume_str = resume_text.decode("utf-8", errors="ignore")
    jd_str = jd_text.decode("utf-8", errors="ignore")

    resume_words = set(resume_str.lower().split())
    jd_words = set(jd_str.lower().split())
    match_score = len(resume_words & jd_words) / max(len(jd_words), 1) * 100

    return {
        "match_score": f"{match_score:.2f}%",
        "message": "Comparison complete."
    }
