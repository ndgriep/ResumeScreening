import google.generativeai as genai
import PyPDF2 as pdf
import docx as doc
import json
import os
from dotenv import load_dotenv
import tkinter as tk # For creating a simple GUI (file dialog)
from tkinter import filedialog # For the file selection dialog

# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API with the API key from the environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = pdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a Word document."""
    text = ""
    try:
        document = doc.Document(docx_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text

def extract_resume_info(resume_text):
    """ Extracts key information from resume text using the Gemini API."""
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    Analyze the following resume and extract the following information:

    - Full Name
    - Email Address
    - Phone Number
    - LinkedIn Profile URL (if available)
    - Education (degrees, institutions, dates)
    - Work Experience (job titles, companies, dates, responsibilities)
    - Skills (list of skills)

    Resume:
    ```
    {resume_text}
    ```

    Output the extracted information in a structured JSON format. If a piece of information is not found, leave the corresponding field blank.

    Example JSON output:

    {{
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "123-456-7890",
      "linkedin": "linkedin.com/in/johndoe",
      "education": [
        {{
          "degree": "Bachelor of Science in Computer Science",
          "institution": "University of Example",
          "dates": "2018-2022"
        }}
      ],
      "work_experience": [
        {{
          "job_title": "Software Engineer",
          "company": "Example Inc.",
          "dates": "2022-Present",
          "responsibilities": "Developed and maintained web applications..."
        }}
      ],
      "skills": ["Python", "JavaScript", "SQL"]
    }}
    """
    try:
        response = model.generate_content(prompt)
        json_string = response.text
        json_string = json_string.replace('```json','').replace('```','').strip()
        extracted_data = json.loads(json_string)
        return extracted_data
    except Exception as e:
        print(f"Error extracting resume information: {e}")
        return None

def extract_resume_info_from_file(file_path):
    """Extracts resume information from a file (PDF, DOCX)."""
    try:
        if file_path.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            resume_text = extract_text_from_docx(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                resume_text = file.read()
        if resume_text:
            return extract_resume_info(resume_text)
        else:
            return None
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def get_file_path():
    """Opens a file dialog and returns the selected file path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select Resume File", filetypes=(("PDF files", "*.pdf"), ("Word files", "*.docx"), ("Text files", "*.txt"), ("All files", "*.*")))
    return file_path

# Main execution
resume_file_path = get_file_path() #get the file path from the user.

if resume_file_path:
    extracted_info = extract_resume_info_from_file(resume_file_path)

    if extracted_info:
        print(json.dumps(extracted_info, indent=2))
else:
    print("No file selected.")