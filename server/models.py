from pydantic import BaseModel
from typing import List, Optional

class ClientProfile(BaseModel):
    age: int
    weight_kg: float
    goal: str  # "weight_loss", "muscle_gain", "endurance"
    injuries: List[str] = []
    equipment: List[str] = []  # "dumbbells", "barbell", "none"

class Action(BaseModel):
    workout_plan: List[str]  # list of exercises prescribed

class Observation(BaseModel):
    client_profile: ClientProfile
    feedback: str
    step_number: int

class State(BaseModel):
    client_profile: ClientProfile
    current_step: int
    done: bool
    total_score: float

class Reward(BaseModel):
    value: float  # 0.0 to 1.0
    reason: str