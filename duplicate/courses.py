import os
import json
from typing import List, Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def recommend_courses(existing_skills: List[str], target_role: Optional[str] = None) -> Dict[str, Any]:
    prompt = f"""
    Given these technical skills: {', '.join(existing_skills) or 'None'},
    suggest 3–5 online courses that would help the user upskill for the role: {target_role or 'unspecified'}.

    For each course, include:
    - Course Name
    - Platform (Coursera, Udemy, etc.)
    - Skills Covered
    - Difficulty Level (Beginner/Intermediate/Advanced)
    - Duration Estimate
    - Justification

    Provide a JSON object with:
    {{
        "analysis": "...summary of skill gaps...",
        "recommendations": [
            {{
                "name": "Course Title",
                "platform": "Udemy",
                "skills_covered": "...",
                "difficulty": "Intermediate",
                "duration": "4 weeks",
                "justification": "Why this course is suitable"
            }}
        ],
        "target_role": "...job title..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}],
            response_format="json",  # ✅ THIS is the correct format
            temperature=0.3
        )
        parsed = json.loads(response.choices[0].message.content)
        parsed['metadata'] = {
            'input_skills': existing_skills,
            'target_role': target_role,
            'total_skills_analyzed': len(existing_skills)
        }
        return parsed

    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to generate recommendations"
        }
