from pydantic import BaseModel
from typing import List, Dict

class EmployeeGraph(BaseModel):
    employee_name: str
    skills: Dict[str, int]

class PlanRequest(BaseModel):
    employee_id: str
    roadmap: str

class DailyPlan(BaseModel):
    day: int
    topic: str

class PlanResponse(BaseModel):
    employee: str
    timeline: str
    plan: List[DailyPlan]