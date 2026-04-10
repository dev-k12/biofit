from .models import ClientProfile, Action

TASKS = {
    "easy": {
        "client_profile": ClientProfile(
            age=25,
            weight_kg=70.0,
            goal="weight_loss",
            injuries=[],
            equipment=["dumbbells"]
        ),
        "ideal_keywords": ["cardio", "walking", "cycling", "jumping jacks"],
        "forbidden_keywords": ["heavy squat", "deadlift", "bench press"],
        "min_exercises": 2
    },
    "medium": {
        "client_profile": ClientProfile(
            age=35,
            weight_kg=85.0,
            goal="muscle_gain",
            injuries=["lower back pain"],
            equipment=["dumbbells", "barbell"]
        ),
        "ideal_keywords": ["dumbbell curl", "shoulder press", "chest fly", "leg press"],
        "forbidden_keywords": ["deadlift", "heavy squat"],
        "min_exercises": 3
    },
    "hard": {
        "client_profile": ClientProfile(
            age=45,
            weight_kg=95.0,
            goal="endurance",
            injuries=["knee injury", "shoulder pain"],
            equipment=["none"]
        ),
        "ideal_keywords": ["walking", "stretching", "yoga", "swimming", "light cardio"],
        "forbidden_keywords": ["running", "jumping", "squat", "press", "lift"],
        "min_exercises": 4
    }
}

def get_task(difficulty: str) -> dict:
    return TASKS.get(difficulty, TASKS["easy"])

def grade_action(task: dict, action: Action) -> float:
    score = 0.0
    plan = [ex.lower() for ex in action.workout_plan]

    if len(plan) >= task["min_exercises"]:
        score += 0.3

    ideal_hits = sum(1 for kw in task["ideal_keywords"] if any(kw in ex for ex in plan))
    score += min(0.4, ideal_hits * 0.1)

    forbidden_hits = sum(1 for kw in task["forbidden_keywords"] if any(kw in ex for ex in plan))
    score -= forbidden_hits * 0.2

    if len(set(plan)) == len(plan):
        score += 0.3

    return max(0.0, min(1.0, round(score, 2)))