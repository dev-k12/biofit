import requests

# Use your LIVE Hugging Face URL
BASE_URL = "https://thedev12-biofit.hf.space/"

def run_task(difficulty):
    # 1. The judge looks for this START tag
    print(f"[START] task={difficulty}", flush=True)
    
    total_score = 0.0
    steps_taken = 0
    
    # Reset the environment
    try:
        requests.post(f"{BASE_URL}reset", params={"difficulty": difficulty}, timeout=10)
    except Exception as e:
        print(f"Error on reset: {e}", flush=True)
        return

    # Pick a safe workout plan based on the difficulty
    if difficulty == "easy":
        plan = ["walking", "stretching", "light cardio"]
    elif difficulty == "medium":
        plan = ["dumbbell curl", "shoulder press", "chest fly"]
    else:
        plan = ["walking", "stretching", "yoga", "swimming"]

    action = {"workout_plan": plan}

    # Play 3 steps (since your max_steps is 3)
    for step_num in range(1, 4):
        try:
            step_req = requests.post(f"{BASE_URL}step", json=action, timeout=10)
            result = step_req.json()
            
            reward = result['reward']['value']
            done = result['done']
            
            total_score += reward
            steps_taken += 1
            
            # 2. The judge looks for this STEP tag
            print(f"[STEP] step={steps_taken} reward={reward}", flush=True)
            
            if done:
                break
        except Exception as e:
            print(f"Error on step: {e}", flush=True)
            break

    # 3. The judge looks for this END tag to calculate your final score
    print(f"[END] task={difficulty} score={total_score:.2f} steps={steps_taken}", flush=True)

def run_inference():
    # Run through all three difficulty levels to get a complete score
    for level in ["easy", "medium", "hard"]:
        run_task(level)

if __name__ == "__main__":
    run_inference()
