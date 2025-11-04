from collections import defaultdict
from typing import Dict, Tuple, Any

def compute_summary(
    solution: Dict[Tuple[int, int, str], int],
    hours: Dict[str, list]
) -> Dict[str, Any]:
    """
    Compute basic summary metrics from the solution:
      - weekly hours per employee
      - total assigned shifts
    """
    emp_hours = defaultdict(float)
    for (e, s, day), assigned in solution.items():
        if assigned:
            emp_hours[e] += hours[day][s]
    summary = {
        "weekly_hours": dict(emp_hours),
        "total_assigned_shifts": sum(solution.values())
    }
    return summary
