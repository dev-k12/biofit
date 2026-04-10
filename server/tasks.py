from .models import ClientProfile, Action

# server/tasks.py

# Define the 3 tasks exactly as they appear in openenv.yaml
TASKS = {
    "easy": {
        "client_profile": {
            "age": 25, 
            "weight": 70, 
            "goal": "weight loss", 
            "injuries": [], 
            "equipment": ["dumbbells"]
        }
    },
    "medium": {
        "client_profile": {
            "age": 35, 
            "weight": 85, 
            "goal": "muscle gain", 
            "injuries": ["lower back pain"], 
            "equipment": ["dumbbells", "barbell"]
        }
    },
    "hard": {
        "client_profile": {
            "age": 45, 
            "weight": 95, 
            "goal": "endurance", 
            "injuries": ["knee", "shoulder"], 
            "equipment": ["none"]
        }
    }
}

def get_task(difficulty: str) -> dict:
    """Returns the task for the given difficulty level."""
    return TASKS.get(difficulty.lower(), TASKS["easy"])

def get_client_profile(difficulty: str) -> dict:
    """Returns the client profile for the given difficulty level."""
    task = get_task(difficulty)
    return task["client_profile"]

def grade_action(client_profile: dict, action) -> float:
    """
    Grades the AI's workout plan based on safety, variety, and goal alignment.
    Returns a float strictly between 0.01 and 0.99.
    """
    score = 0.0
    
    # 1. Safely extract the workout plan from the action object
    workout_plan = []
    if isinstance(action, dict):
        workout_plan = action.get("workout_plan", [])
    elif hasattr(action, "workout_plan"):  # If it's a Pydantic model
        workout_plan = action.workout_plan
        
    if not isinstance(workout_plan, list):
        workout_plan = []
        
    # Convert everything to lowercase for easy checking
    plan_lower = [str(ex).lower() for ex in workout_plan]
    
    # ---------------------------------------------------------
    # SCORING LOGIC (Matching your openenv.yaml rules)
    # ---------------------------------------------------------
    
    # Rule 1: Minimum Exercises Met (+0.3)
    if len(plan_lower) >= 3:
        score += 0.3
        
    # Rule 2: Variety Bonus (+0.3)
    if len(set(plan_lower)) >= 3:
        score += 0.3
        
    # Rule 3: Goal Alignment (+0.4)
    goal = client_profile.get("goal", "").lower()
    goal_met = False
    
    for ex in plan_lower:
        # Check cardio/endurance goals
        if goal in ["weight loss", "endurance"] and any(word in ex for word in ["walk", "run", "swim", "stretch", "yoga", "cardio"]):
            goal_met = True
        # Check muscle gain goals
        elif goal == "muscle gain" and any(word in ex for word in ["curl", "press", "lift", "row", "fly", "squat"]):
            goal_met = True
            
    if goal_met:
        score += 0.4
        
    # Rule 4: Safety/Injury Penalties (-0.2 per violation)
    injuries = client_profile.get("injuries", [])
    for ex in plan_lower:
        if "lower back pain" in injuries and any(bad in ex for bad in ["deadlift", "row", "heavy"]):
            score -= 0.2
        if "knee" in injuries and any(bad in ex for bad in ["squat", "lunge", "jump"]):
            score -= 0.2
        if "shoulder" in injuries and any(bad in ex for bad in ["press", "push", "overhead"]):
            score -= 0.2

    # ---------------------------------------------------------
    # THE CRITICAL PHASE 2 FIX
    # Force the score strictly into the (0, 1) range
    # ---------------------------------------------------------
    return max(0.01, min(0.99, float(score)))
