import json
from langchain_core.prompts import PromptTemplate
from agents.auditor_agent import get_llm

def generate_schedule(missing_skills: str, retrieved_content: str, days: int) -> list:
    # First Guardrail: Empty content check
    if not retrieved_content or retrieved_content.strip() == "":
        return [{"week": 0, "topic": "No internal training materials found for these skills."}]

    # --- NEW LOGIC: Convert Days to Weeks ---
    # If the auditor says 30 days, this converts it to roughly 4 weeks. (max ensures at least 1 week)
    weeks = max(1, days // 7)

    llm = get_llm()
    
    # --- UPGRADED PROMPT: Rust-Only Guardrail + Weekly Paragraphs ---
    prompt_text = """
    You are a strict corporate learning planner. 
    
    CRITICAL RULE 1 - RUST ONLY: This system is exclusively built for teaching the Rust programming language. 
    If the requested skills are NOT related to Rust, you MUST reject it by outputting this exact fallback array and nothing else:
    [{{ "week": 0, "topic": "Access Denied: This learning platform is strictly configured for Rust upskilling only. Please submit a Rust-related capability goal." }}]
    
    CRITICAL RULE 2 - WEEKLY FORMAT: Build a {weeks}-week learning plan strictly using the 'Reference material' provided below.
    Instead of daily bullet points, each week MUST have a rich, detailed paragraph explaining the concepts to be mastered. 
    At the end of each paragraph, provide an official reference link (e.g., to doc.rust-lang.org) if applicable.
    
    Skills to learn: {missing_skills}
    Reference material: {content}
    
    CRITICAL INSTRUCTIONS FOR JSON:
    1. Output ONLY a valid JSON array. Do NOT wrap in ```json markdown blocks. Use double quotes ("").
    2. Use the keys "week" (int) and "topic" (string).
    
    Format Example:
    [{{ "week": 1, "topic": "This week focuses on... Reference: https://..." }}, {{ "week": 2, "topic": "..." }}]
    """
    
    prompt = PromptTemplate.from_template(prompt_text)
    response = (prompt | llm).invoke({
        "weeks": weeks, 
        "missing_skills": missing_skills, 
        "content": retrieved_content
    }).content
    
    # Safely parse the JSON response
    clean_json = response.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(clean_json)
    except json.JSONDecodeError as e:
        print(f"Planner JSON Decode Error: {e}")
        return [{"week": 0, "topic": "Error generating valid schedule from AI."}]