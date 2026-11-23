from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
import json

def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash") 

def analyze_skills(roadmap: str, skills: dict) -> str:
    llm = get_llm()
    prompt_text = """
    Roadmap: {roadmap}
    Employee Skills: {skills}
    
    Analyze the learning gap. Output ONLY valid JSON using double quotes with these exact keys:
    {{
        "missing_skills": "comma-separated list of technical skills",
        "current_level": "e.g., Level 1: Beginner",
        "target_level": "e.g., Level 5: Expert",
        "estimated_days": 14
    }}
    """


    prompt = PromptTemplate.from_template(prompt_text)
    chain = prompt | llm
    response = chain.invoke({"roadmap": roadmap, "skills": skills}).content

    try:
        clean_json = response.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except json.JSONDecodeError:
        # If it fails, return a safe default so the UI doesn't say "undefined"
        return {
            "missing_skills": "Core fundamentals", 
            "current_level": "Level 1", 
            "target_level": "Level 5", 
            "estimated_days": 25
        }