import os
import json
import io
import time
import pandas as pd
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def configure_gemini():
    """Loads API key from .env and configures the Gemini model."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_API_KEY in your .env file.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-pro-latest')

def get_gemini_response(prompt: str, model, max_retries=5):
    """Gets a JSON response from the Gemini model with a retry mechanism."""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if not response.parts:
                return None
            json_text = response.text.strip().lstrip('```json').rstrip('```')
            return json.loads(json_text)
        except Exception as e:
            print(f"🛑 An error occurred (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None
    return None

def analyze_employee_sentiment(df: pd.DataFrame, model):
    """
    Analyzes a DataFrame of employee feedback using Gemini.
    Returns a markdown-formatted string report.
    """
    feedback_data_string = df.to_string()

    prompt = f"""
    You are an expert HR analyst specializing in employee sentiment and attrition risk.
    Your task is to analyze the following comprehensive employee feedback data and generate a strategic report for leadership.

    **Employee Feedback Data:**
    ```
    {feedback_data_string}
    ```

    **Your strategic report must contain these five sections:**

    1.  **Executive Summary:** A brief, one-paragraph overview of the key findings, including overall sentiment and the most critical issue to address.
    2.  **Key Strengths (Top 3):** Identify the top 3 areas where the company is performing well. Use bullet points and cite specific question categories as evidence.
    3.  **Critical Areas for Improvement (Top 3):** Identify the top 3 areas that pose the biggest risks or have the most negative feedback. Use bullet points and specify the themes.
    4.  **Attrition Risk Assessment:** Provide a risk level (Low, Medium, High). Justify the assessment by connecting the "Areas for Improvement" directly to factors that cause employees to leave.
    5.  **Actionable Recommendations:** For each "Area for Improvement" you identified, propose one specific, concrete, and actionable recommendation that HR and leadership can implement.

    Structure the output clearly with markdown headings for each section.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during analysis: {e}"

def extract_text_from_pdf(pdf_file):
    all_text = ""
    pdf_bytes = pdf_file.read()
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text: all_text += text + "\n"
        if len(all_text.strip()) > 100: return all_text.strip()
    except Exception: pass
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                pil_image = page.to_image(resolution=300).original
                all_text += pytesseract.image_to_string(pil_image, lang='eng') + "\n"
        return all_text.strip()
    except Exception as e: return None

def format_job_description(raw_jd_text: str, model):
    prompt = f"""You are an expert HR data analyst. Read the raw text of a job description below and convert it into a structured JSON object with keys: "job_title", "required_qualifications", "preferred_qualifications", "responsibilities".

    Raw Job Description Text:
    ```text
    {raw_jd_text}
    ```
    Provide ONLY the clean JSON object as the output."""
    return get_gemini_response(prompt, model)

def process_resume(resume_text: str, model):
    prompt = f"""You are an expert data extraction AI. Read the resume text below and convert it into a structured JSON object. Extract: `contact_info` (name, email, linkedin_url), `summary`, `total_experience_years`, `work_experience` (list of jobs), `education` (list of qualifications), `skills`.

    Resume Text:
    ```text
    {resume_text}
    ```
    Provide ONLY a clean JSON object."""
    return get_gemini_response(prompt, model)

def screen_resume(job_description: str, processed_resume: dict, model):
    prompt = f"""You are an expert HR Technical Recruiter AI. Analyze the candidate's structured resume against the provided job description.

    Job Description:
    ```json
    {job_description}
    ```
    Candidate's Resume Data:
    ```json
    {json.dumps(processed_resume, indent=2)}
    ```
    Provide a JSON response with: `match_score` (0-100), `summary`, `strengths` (list), `weaknesses` (list), `skills_analysis` (required_skills_found, missing_skills), `final_recommendation` ("Strongly Recommend", "Consider", "Not a Fit")."""
    return get_gemini_response(prompt, model)

def generate_cumulative_report(all_analyses: list, model):
    prompt = f"""You are a Senior Hiring Manager AI. Review the list of analysis reports for all candidates and generate a final cumulative report.

    Candidate Analysis Reports:
    ```json
    {json.dumps(all_analyses, indent=2)}
    ```
    Provide a JSON object with: `overall_summary` and `candidate_ranking` (a ranked list with rank, candidate_name, match_score, final_recommendation, justification_for_rank)."""
    return get_gemini_response(prompt, model)