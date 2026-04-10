# 🧬 BioFit — AI Fitness Prescription Environment

> An OpenEnv environment where AI agents learn to prescribe 
> safe, personalized workout plans based on client profiles.

## 🎯 What is BioFit?

BioFit is a reinforcement learning environment where an AI agent:
- Receives a **client profile** (age, weight, goal, injuries, equipment)
- Must **prescribe a workout plan** step by step
- Gets **scored** on safety, goal alignment, and exercise variety

## 🚀 Quick Start

### Run Locally (Package Mode)
Make sure you have your dependencies installed, then run the server using the new entry point:
```bash
pip install -e .
uvicorn server.app:app --host 0.0.0.0 --port 7860
Run with Docker

Build and run the container, ensuring the ports match the Hugging Face requirements:

Bash
docker build -t biofit .
docker run -p 7860:7860 biofit
🎮 Environment Interface
Endpoint	Method	Description
/reset	POST	Start new client session
/step	POST	Submit workout plan, get score
/state	GET	Get current session state
📊 Tasks
Level	Client	Goal	Challenge
🟢 Easy	25yo, 70kg	Weight Loss	No injuries
🟡 Medium	35yo, 85kg	Muscle Gain	Lower back pain
🔴 Hard	45yo, 95kg	Endurance	Knee + shoulder injuries
🏆 Reward Function
✅ Correct exercise types → +0.4

✅ Minimum exercises met → +0.3

✅ Variety bonus → +0.3

❌ Forbidden exercises (unsafe) → -0.2 per violation

🧪 Run Inference Check
To test the environment against the baseline constraints:

Bash
# First start the server in one terminal
uvicorn server.app:app --host 0.0.0.0 --port 7860

# Then run the inference script in a new terminal
python inference.py
📁 Project Structure
Plaintext
biofit/
├── server/              ← Core environment package
│   ├── __init__.py      
│   ├── app.py           ← FastAPI server (Entry point)
│   ├── environment.py   ← Game engine
│   ├── models.py        ← Data shapes (Pydantic)
│   └── tasks.py         ← 3 graded tasks
├── inference.py         ← AI inference test script
├── pyproject.toml       ← Package configuration
├── uv.lock              ← Dependency lockfile
├── openenv.yaml         ← OpenEnv hackathon config
├── requirements.txt     ← Dependencies
├── Dockerfile           ← Container configuration
└── README.md            

👤 Author
Built for the Scalar OpenEnv Hackathon 2026