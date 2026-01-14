# backend/cv_analyzer/cv_generator.py

import os
import sys
import json
from jinja2 import Environment, FileSystemLoader

# PATH SETUP
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from llm_workflows.gap_workflow import GapAnalysisState

# CONFIGURATION
# Templates are in: backend/cv_analyzer/data
TEMPLATE_DIR = os.path.join(BASE_DIR, 'cv_analyzer', 'data')
# Output goes to: backend/output
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_and_save_node(state: GapAnalysisState) -> dict:
    """
    LangGraph Node: Renders the CV.
    Features:
    - Merges verified skills.
    - Creates 'personal_info' adapter.
    - Interactive Template Selection if default is missing.
    """
    print("\n" + "="*40)
    print("🎨 [Writer] Preparing final CV...")
    print("="*40)

    # 1. Retrieve Data
    structured_data = state.get("structured_cv_data", {}).copy() if state.get("structured_cv_data") else None
    template_choice = state.get("template_selection", "1")
    user_name = state.get("user_name", "Candidate")
    new_verified_skills = state.get("new_skills_to_add", [])

    if not structured_data:
        raise RuntimeError("CV Data Missing: Cannot render CV.")

    # 2. INJECT NEW SKILLS
    if new_verified_skills:
        print(f"   🔗 Merging {len(new_verified_skills)} verified skills...")
        current_skills = structured_data.get("skills", [])
        
        # Ensure current_skills is a list
        if isinstance(current_skills, str):
            current_skills = [s.strip() for s in current_skills.split(',')]
            
        # Merge, deduplicate, and sort
        merged_skills = list(set(current_skills + new_verified_skills))
        structured_data["skills"] = merged_skills

    # 3. DATA ADAPTER (Prevents 'undefined' errors)
    if "personal_info" not in structured_data:
        # print("   🔧 Adapting data structure...")
        structured_data["personal_info"] = {
            "name": structured_data.get("name", "Unknown"),
            "email": structured_data.get("email", ""),
            "phone": structured_data.get("phone", ""),
            "linkedin": structured_data.get("linkedin", ""),
            "github": structured_data.get("github", ""),
            "location": structured_data.get("location", ""),
            "portfolio": structured_data.get("portfolio", "")
        }

    # 4. RESOLVE TEMPLATE FILENAME
    if str(template_choice).isdigit():
        template_filename = f"template_{template_choice}.tex"
    elif not str(template_choice).endswith(".tex"):
        template_filename = f"{template_choice}.tex"
    else:
        template_filename = template_choice
    
    # 5. CHECK & INTERACTIVE SELECTION
    template_path = os.path.join(TEMPLATE_DIR, template_filename)
    
    # If the specific template requested doesn't exist, ask the user.
    if not os.path.exists(template_path):
        print(f"\n⚠️  Template '{template_filename}' not found in data folder.")
        
        # List available .tex files in backend/cv_analyzer/data
        if os.path.exists(TEMPLATE_DIR):
            available_templates = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith('.tex')]
        else:
            available_templates = []
            
        if not available_templates:
            raise FileNotFoundError(f"CRITICAL: No .tex templates found in {TEMPLATE_DIR}")

        print("\n📂 Available Templates:")
        for i, t in enumerate(available_templates, 1):
            print(f"   {i}. {t}")
            
        # Loop until valid input
        while True:
            try:
                choice = input(f"\n👉 Select a template number (1-{len(available_templates)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(available_templates):
                    template_filename = available_templates[idx]
                    print(f"✅ Selected: {template_filename}")
                    break
                else:
                    print("❌ Invalid number. Try again.")
            except ValueError:
                print("❌ Please enter a number.")

    # 6. RENDER
    try:
        print(f"   📝 Rendering with: {template_filename}...")
        
        env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            block_start_string=r'\BLOCK{', block_end_string=r'}', 
            variable_start_string=r'\VAR{', variable_end_string=r'}',
            comment_start_string=r'\#{', comment_end_string=r'}', 
            line_statement_prefix='%%', trim_blocks=True, lstrip_blocks=True
        )
        
        template = env.get_template(template_filename)
        
        # Pass data in two ways to support different template styles
        rendered_tex = template.render(
            data=structured_data, 
            **structured_data
        )
        
        safe_name = user_name.replace(" ", "_").replace(".", "")
        output_filename = f"{safe_name}_Optimized_{template_filename}"
        final_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(final_path, 'w', encoding='utf-8') as f:
            f.write(rendered_tex)
            
        print(f"✅ Final CV saved to: {final_path}")
        return {"final_cv_path": final_path}
        
    except Exception as e:
        print(f"❌ Rendering Error: {e}")
        raise RuntimeError(f"Failed to render PDF: {e}")