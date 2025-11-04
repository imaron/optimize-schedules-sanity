from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
from optimizer import solve_schedule
from formula_engine import compute_summary

app = FastAPI(title="Scheduling Brain")

# Pydantic models to validate the request
class TeamMember(BaseModel):
    id: str
    name: str
    role: str
    max_hours: float
    max_shifts: int

class DayData(BaseModel):
    costs: List[List[float]]
    prefs: List[List[float]]
    hours: List[float]

class ScheduleRequest(BaseModel):
    lambda_weight: float
    team_members: List[TeamMember]
    days: Dict[str, DayData]

@app.post("/optimize")
async def optimize(req: ScheduleRequest):
    """Endpoint to run the scheduling optimizer."""
    # Extract matrices and caps from the request
    costs = {day: data.costs for day, data in req.days.items()}
    prefs = {day: data.prefs for day, data in req.days.items()}
    hours = {day: data.hours for day, data in req.days.items()}
    shift_caps = [m.max_shifts for m in req.team_members]
    hour_caps = [m.max_hours for m in req.team_members]

    # Run the optimization
    solution, obj_value = solve_schedule(
        costs, prefs, hours, req.lambda_weight, shift_caps, hour_caps
    )

    # Compute summary metrics (weekly hours, totals, etc.)
    summary = compute_summary(solution, hours)

    return {
        "objective": obj_value,
        "solution": solution,
        "summary": summary
    }
