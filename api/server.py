from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.auditor_agent import analyze_skills
from agents.tutor_agent import retrieve_content
from agents.planner_agent import generate_schedule

app = Flask(__name__)
CORS(app)

# Simulated employee database
EMPLOYEES = {
    "123": {"name": "Rishi", "skills": "Python, C++, SQL"},
    "101": {"name": "Aarav", "skills": "AI/ML, Python, TensorFlow"},
    "102": {"name": "Priya", "skills": "Java, Spring Boot, MySQL"},
    "103": {"name": "Kavya", "skills": "UI/UX, Figma, HTML, CSS"}
}

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Active", "message": "Upskilling AI Router is running!"})

@app.route("/generate-learning-plan", methods=["POST"])
def main_api():
    data = request.json
    emp_id = str(data.get("employee_id"))
    roadmap_goal = data.get("roadmap")

    # Fetch employee data
    emp = EMPLOYEES.get(emp_id, {"name": "Unknown", "skills": "None"})
    
    print(f"\n--- New Request: Emp {emp_id} ({emp['name']}) -> Goal: {roadmap_goal} ---")
    
    # 1. Audit Gap (Calls your surgically edited analyze_skills)
    gap_info = analyze_skills(roadmap_goal, emp)
    
    # Extract the dynamic JSON values (with safe fallbacks)
    missing_skills = gap_info.get("missing_skills", "Core fundamentals")
    days = int(gap_info.get("estimated_days", 30))
    
    print(f"Calculated Timeline: {days} Days for {emp['name']}")
    
    # 2. Retrieve Content
    context = retrieve_content(missing_skills)
    
    # 3. Generate Plan (Passes the dynamic days to your planner)
    plan = generate_schedule(missing_skills, context, days)
    
    # Send the fully dynamic, structured data payload to the UI
    return jsonify({
        "employee": emp["name"],
        "current_level": gap_info.get("current_level", "Level 1: Beginner"),
        "target_level": gap_info.get("target_level", "Level 5: Expert"),
        "timeline": f"{days} Days",
        "missing_skills": missing_skills,
        "plan": plan
    })

if __name__ == "__main__":
    app.run(port=5000, debug=False)