import os
import json
import requests
from openai import OpenAI

# Use your LIVE Hugging Face URL
BASE_URL = "https://thedev12-biofit.hf.space/"

def get_llm_action(client_profile):
    """Calls the Hackathon's LLM proxy to get a workout plan."""
    # 1. Grab the API credentials injected by the Scalar Validator
    api_key = os.environ.get("API_KEY", "dummy-key")
    base_url = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
    
    # 2. Initialize the OpenAI client pointing to their proxy
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # 3. Give the AI the client profile and ask for JSON back
    prompt = f"""
    You are an AI fitness trainer. Review this client profile and prescribe a safe workout plan.
    Client Profile: {json.dumps(client_profile)}
    
    Return ONLY a raw JSON object with a single key "workout_plan" containing a list of exercise strings.
    Example: {{"workout_plan": ["walking", "light stretching"]}}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # The proxy usually intercepts this
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = response.choices[0].message.content
        
        # Strip out any markdown blocks if the AI includes them
        if content.startswith("```json"):
            content = content.replace("```json\n", "").replace("\n```", "")
            
        return json.loads(content)
    except Exception as e:
        print(f"LLM Error: {e}", flush=True)
        # Fallback just in case the API times out so the script doesn't crash
        return {"workout_plan": ["walking", "stretching"]}

def run_task(difficulty):
    print(f"[START] task={difficulty}", flush=True)
    
    total_score = 0.0
    steps_taken = 0
    client_profile = {}
    
    # 1. Reset the environment
    try:
        res = requests.post(f"{BASE_URL}reset", params={"difficulty": difficulty}, timeout=10)
        obs = res.json()
        client_profile = obs.get('client_profile', {})
    except Exception as e:
        print(f"Error on reset: {e}", flush=True)
        return

    # 2. Play 3 steps using the LLM Brain
    for step_num in range(1, 4):
        # Ask the LLM to generate the action!
        action = get_llm_action(client_profile)
        
        try:
            step_req = requests.post(f"{BASE_URL}step", json=action, timeout=10)
            result = step_req.json()
            
            reward = result['reward']['value']
            done = result['done']
            
            total_score += reward
            steps_taken += 1
            
            print(f"[STEP] step={steps_taken} reward={reward}", flush=True)
            
            if done:
                break
        except Exception as e:
            print(f"Error on step: {e}", flush=True)
            break

    print(f"[END] task={difficulty} score={total_score:.2f} steps={steps_taken}", flush=True)

def run_inference():
    for level in ["easy", "medium", "hard"]:
        run_task(level)

if __name__ == "__main__":
    run_inference()
