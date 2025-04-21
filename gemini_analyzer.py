import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def initialize_api():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY in environment variables")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

def clean_json_string(json_string):
    cleaned = re.sub(r'```(?:json)?\s*|\s*```', '', json_string.strip())
    cleaned = re.sub(r',\s*}', '}', cleaned)
    cleaned = re.sub(r',\s*]', ']', cleaned)
    return cleaned

def extract_resume_info(resume_text, model):
    prompt = f"""
    Analyze the following resume and extract structured information in JSON:

    RESUME:
    {resume_text}

    Format:
    {{
      "personal_info": {{
        "name": "", "email": "", "phone": "", "location": ""
      }},
      "education": [{{ "degree": "", "institution": "", "dates": "", "gpa": "" }}],
      "work_experience": [{{ "title": "", "company": "", "dates": "", "responsibilities": [] }}],
      "skills": [], "certifications": [], "summary": ""
    }}

    Format the output as valid JSON only.
    """

    try:
        response = model.generate_content(prompt)
        json_string = clean_json_string(response.text)
        return json.loads(json_string)
    except Exception as e:
        return {"error": f"Failed to parse resume info: {e}", "raw_response": response.text}

def analyze_resume_against_job(resume_data, job_description, model):
    resume_json = json.dumps(resume_data, indent=2)
    prompt = f"""
    Evaluate the following resume (in JSON) against the job description.

    RESUME:
    {resume_json}

    JOB DESCRIPTION:
    {job_description}

    Return the result as JSON with:
    {{
      "match_score": "0-100",
      "strengths": [],
      "weaknesses": [],
      "missing_skills": [],
      "matching_skills": [],
      "recommendations": [],
      "summary": ""
    }}

    Respond with only valid JSON.
    """

    try:
        response = model.generate_content(prompt)
        json_string = clean_json_string(response.text)
        return json.loads(json_string)
    except Exception as e:
        return {"error": f"Failed to parse analysis: {e}", "raw_response": response.text}
