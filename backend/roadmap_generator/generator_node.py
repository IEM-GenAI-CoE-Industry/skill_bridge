import json
import os
from google import genai
from .roadmap_mvp_state import RoadmapState

client = genai.Client(api_key="AIzaSyDp7Xl852uwIhwReyOIA6dn65OWXjIgoa8")


def clean_json_response(text: str) -> str:
    """
    Removes ```json markdown wrapping if present
    """
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    return text.strip()


def generator_node(state: RoadmapState) -> RoadmapState:
    content = state.get("report_content", "")

    if not content:
        return {
            **state,
            "final_roadmap_json": {"error": "No report content found"}
        }

    try:
        prompt = f"""
        Generate a structured learning roadmap in STRICT JSON format.

        IMPORTANT:
        - Return ONLY JSON.
        - Do NOT include explanations.
        - Include:
            roadmap_title
            modules (list)
                skill
                week
                topic
                recommended_action
                course_link (real working link)

        Skill Report:
        {content}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        roadmap_text = response.text

        if not roadmap_text:
            raise ValueError("Model returned empty response")

        cleaned_text = clean_json_response(roadmap_text)

        roadmap_json = json.loads(cleaned_text)

        return {
            **state,
            "final_roadmap_json": roadmap_json
        }

    except Exception as e:
        return {
            **state,
            "final_roadmap_json": {
                "error": str(e),
                "raw_response": response.text if 'response' in locals() else "No response"
            }
        }