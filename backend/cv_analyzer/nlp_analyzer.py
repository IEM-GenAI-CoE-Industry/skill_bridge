# backend/cv_analyzer/nlp_analyzer.py

import os
import json
import sys
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai 

# PATH SETUP
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from llm_workflows.gap_workflow import GapAnalysisState

# CONFIGURATION
load_dotenv() 
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Client
client = None
if api_key:
    client = genai.Client(api_key=api_key)

# CRITICAL FIX: Use 2.5-flash to avoid 'Quota Exceeded' (429) errors
MODEL_NAME = "gemini-2.5-flash"

def cv_reader_node(state: GapAnalysisState) -> dict:
    """Node 1: Reads the PDF file."""
    file_path = state.get("cv_file_path")
    print(f"🧠 [Reader] Reading file: {os.path.basename(file_path)}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return {"cv_text": text}
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        raise ValueError("Failed to read file. Ensure it is a valid PDF.")

def extract_data_node(state: GapAnalysisState) -> dict:
    """Node 2: Extracts structured JSON with STRICT schema."""
    print(f"🧠 [Extractor] Structuring data using {MODEL_NAME}...")
    cv_text = state.get("cv_text")
    
    prompt = f"""
    You are a professional Resume Parser. Extract data from this text into a strict JSON format.
    
    CRITICAL RULES:
    1. "experience" MUST be a list of objects with keys: "title", "company", "dates", "description".
    2. "description" should be a short summary string, NOT a list.
    3. If "dates" are missing, estimate them from context or put "Present".
    
    JSON STRUCTURE:
    {{
        "name": "Candidate Name",
        "email": "candidate@email.com",
        "phone": "Phone Number",
        "linkedin": "https://linkedin.com/in/...",
        "github": "https://github.com/...",
        "location": "City, Country",
        "summary": "Professional summary...",
        "skills": ["Skill A", "Skill B", "Skill C"],
        "experience": [
            {{
                "title": "Software Engineer",
                "company": "Tech Corp",
                "dates": "Jan 2020 - Present",
                "description": "Developed web applications using React and Python."
            }}
        ],
        "education": [
            {{
                "degree": "B.Sc Computer Science",
                "institution": "University Name",
                "year": "2023"
            }}
        ],
        "projects": [
            {{
                "title": "Project Name",
                "technologies": "Python, AI",
                "description": "Built an AI agent."
            }}
        ]
    }}

    RESUME TEXT:
    {cv_text[:15000]}
    
    Return ONLY valid JSON. No Markdown.
    """
    
    try:
        if not client:
            raise ValueError("Gemini Client not initialized. Check .env file.")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        # Clean response
        raw_text = response.text
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].strip()
            
        data = json.loads(raw_text)
        
        # Validation
        if "name" not in data: data["name"] = "Candidate"
        
        print("✅ Extraction Complete.")
        return {
            "structured_cv_data": data, 
            "user_name": data.get("name", "Candidate")
        }
        
    except Exception as e:
        print(f"❌ LLM Extraction Error: {e}")
        # IMPORTANT: Returning empty dict causes the "CV Data Missing" error later!
        return {"structured_cv_data": {}}