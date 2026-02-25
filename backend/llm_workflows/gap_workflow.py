# backend/llm_workflows/gap_workflow.py
from typing import TypedDict, List, Dict, Any

class GapAnalysisState(TypedDict):
    # Input
    cv_file_path: str
    job_title: str
    
    # Processing
    cv_text: str
    structured_cv_data: Dict[str, Any]  # {"name": "...", "skills": [...]}
    user_name: str
    
    # Analysis
    job_requirements: str
    skill_report: Dict[str, Any]        # {"missing_skills": [...], "analysis_summary": "..."}
    
    # Verification (Interactive)
    new_skills_to_add: List[str]
    skills_for_roadmap: List[str]
    
    # Output
    pdf_path: str                       # Path to generated report
    final_cv_path: str                  # Path to final .tex/.pdf