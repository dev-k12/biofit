import requests
import json
import time

BASE_URL = "https://thedev12-biofit.hf.space/"

def run_inference():
    print(f"🚀 Starting Inference Check for BioFit...")
    
    try:
        reset_req = requests.post(f"{BASE_URL}reset", params={"difficulty": "easy"}, timeout=10)
        obs = reset_req.json()
        print(f"✅ Reset Successful. Client Profile: {obs.get('client_profile')}")
    except Exception as e:
        print(f"❌ Reset Failed: {e}")
        return

    action = {"workout_plan": ["walking", "stretching", "light cardio"]}
    
    try:
        step_req = requests.post(f"{BASE_URL}step", json=action, timeout=10)
        result = step_req.json()
        score = result['reward']['value']
        print(f"✅ Step Successful. Reward Score: {score}")
    except Exception as e:
        print(f"❌ Step Failed: {e}")

if __name__ == "__main__":
    run_inference()