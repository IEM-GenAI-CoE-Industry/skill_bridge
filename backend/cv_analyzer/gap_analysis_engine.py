# backend/cv_analyzer/gap_analysis_engine.py

import os
import json
import sys
from dotenv import load_dotenv
from fpdf import FPDF
from google import genai

# PATH SETUP
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from llm_workflows.gap_workflow import GapAnalysisState

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = None
if api_key:
    client = genai.Client(api_key=api_key)

# CRITICAL FIX: Use 2.5-flash here too!
MODEL_NAME = "gemini-2.5-flash"

def generate_job_requirements_node(state: GapAnalysisState) -> dict:
    """Node 3: Generates required skills for the target job."""
    job_title = state.get("job_title")
    print(f"🧠 [Recruiter] Generating requirements for: {job_title}")
    
    prompt = f"""
    You are an expert Technical Recruiter.
    List the top 10 most critical technical skills required for a "{job_title}".
    
    Return ONLY a JSON list of strings. Example:
    ["Python", "React", "AWS", "SQL"]
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        text = response.text.replace("```json", "").replace("```", "").strip()
        requirements = json.loads(text)
        
        return {"target_job_requirements": requirements}
    except Exception as e:
        print(f"❌ Error generating requirements: {e}")
        return {"target_job_requirements": []}

def analyze_skill_gap_node(state: GapAnalysisState) -> dict:
    """Node 4: Compares CV skills vs Job Requirements."""
    print("🧠 [Analyst] Comparing skills...")
    
    current_skills = state.get("structured_cv_data", {}).get("skills", [])
    required_skills = state.get("target_job_requirements", [])
    
    if not current_skills:
        print("⚠️ Warning: No CV data found in state. Pipeline might be broken.")
    
    missing_skills = [skill for skill in required_skills if skill.lower() not in [s.lower() for s in current_skills]]
    
    return {"missing_skills": missing_skills}

def generate_report_pdf_node(state: GapAnalysisState) -> dict:
    """Node 5: Generates a PDF report of the gaps."""
    print("📄 [Reporter] Generating PDF...")
    
    job_title = state.get("job_title", "Job")
    missing = state.get("missing_skills", [])
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Skill Gap Report: {job_title}", ln=True, align='C')
    pdf.ln(10)
    
    if missing:
        pdf.cell(200, 10, txt="Missing Skills:", ln=True)
        for skill in missing:
            pdf.cell(200, 10, txt=f"- {skill}", ln=True)
    else:
        pdf.cell(200, 10, txt="No significant skill gaps found!", ln=True)
        
    output_path = os.path.join(BASE_DIR, "output", f"Skill_Report_{job_title.replace(' ', '')}.pdf")
    pdf.output(output_path)
    print(f"✅ PDF Saved: {output_path}")
    
    return {"pdf_path": output_path}