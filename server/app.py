import uvicorn
from fastapi import FastAPI
from .models import Action
from .environment import BioFitEnvironment

app = FastAPI(title="BioFit", description="AI Fitness Prescription Environment")

env = BioFitEnvironment()

@app.get("/")
def root():
    return {"name": "BioFit", "status": "running"}

@app.post("/reset")
def reset(difficulty: str = "easy"):
    obs = env.reset(difficulty)
    return obs

@app.post("/step")
def step(action: Action):
    obs, reward, done = env.step(action)
    return {"observation": obs, "reward": reward, "done": done}

@app.get("/state")
def state():
    return env.state()

# --- THE NEW ADDITION FOR THE VALIDATOR ---
def main():
    """Entry point for the OpenEnv validator and multi-mode deployment."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
