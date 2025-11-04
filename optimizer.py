from ortools.sat.python import cp_model
from typing import Dict, List, Tuple

def solve_schedule(
    costs: Dict[str, List[List[float]]],
    prefs: Dict[str, List[List[float]]],
    hours: Dict[str, List[float]],
    lam: float,
    shift_caps: List[int],
    hour_caps: List[float]
) -> Tuple[Dict[Tuple[int, int, str], int], float]:
    """
    Solve the scheduling optimization problem.
    Returns:
        solution (dict): keys are (employee, shift, day), values are 0/1
        objective_value (float): the minimized cost minus lambda*preference
    """
    days = list(costs.keys())
    num_employees = len(shift_caps)
    num_shifts = len(next(iter(costs.values()))[0])  # assume square matrix for simplicity

    model = cp_model.CpModel()

    # Decision variables: x[(e, s, day)] = 1 if employee e is assigned to shift s on day.
    x = {}
    for day in days:
        for e in range(num_employees):
            for s in range(num_shifts):
                x[(e, s, day)] = model.NewBoolVar(f"x_e{e}_s{s}_{day}")

    # Each employee works at most one shift per day
    for day in days:
        for e in range(num_employees):
            model.Add(sum(x[(e, s, day)] for s in range(num_shifts)) <= 1)

    # Total shifts per employee across the week (shift caps)
    for e in range(num_employees):
        model.Add(sum(x[(e, s, day)] for day in days for s in range(num_shifts)) <= shift_caps[e])

    # Total hours per employee across the week (hour caps)
    for e in range(num_employees):
        total_hours = []
        for day in days:
            h_vec = hours[day]
            for s in range(num_shifts):
                total_hours.append(h_vec[s] * x[(e, s, day)])
        model.Add(sum(total_hours) <= hour_caps[e])

    # Objective: minimize cost minus lambda * preference
    SCALE = 1000  # scaling to convert float costs into ints
    objective_terms = []
    for day in days:
        for e in range(num_employees):
            for s in range(num_shifts):
                cost_penalty = costs[day][e][s] - lam * prefs[day][e][s]
                int_cost = int(cost_penalty * SCALE)
                objective_terms.append(int_cost * x[(e, s, day)])
    model.Minimize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30
    status = solver.Solve(model)

    solution = {}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for key, var in x.items():
            solution[key] = int(solver.Value(var))
        objective_value = solver.ObjectiveValue() / SCALE
    else:
        objective_value = float('inf')
    return solution, objective_value
