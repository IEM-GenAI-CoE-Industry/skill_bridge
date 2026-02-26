import os
import json
from groq import Groq
from dotenv import load_dotenv
from roadmap_mvp_state import RoadmapState

# Load environment variables
current_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(current_dir, '.env'))

# Configuration
GROKAI_API_KEY = os.getenv("grokai_api_key")
client = Groq(api_key=GROKAI_API_KEY)
MODEL_NAME = "mixtral-8x7b-32768"  # Grokai model

def generator_node(state: RoadmapState) -> RoadmapState:
    """Uses AI to turn report text into a JSON roadmap."""
    content = state.get("report_content", "")
    
    if not content or "Error" in content:
        return {"final_roadmap_json": {"error": "No valid report content to process"}}

    print(f"🧠 Node 2 (Generator): Creating roadmap using {MODEL_NAME}...")
    
    prompt = f"""
    Analyze the following Skill Report and identify the missing skills.
    Then, create a structured learning roadmap in JSON format.
    
    Report: {content}
    
    Return ONLY a JSON object with this structure:
    {{
        "roadmap_title": "...",
        "modules": [
            {{ "skill": "...", "week": 1, "topic": "...", "recommended_action": "..." }}
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = response.choices[0].message.content.strip()
        
        # Clean markdown if present
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            
        return {"final_roadmap_json": json.loads(raw_text)}
    except Exception as e:
        print(f"❌ Generator Error: {e}")
        return {"final_roadmap_json": {"error": str(e)}}