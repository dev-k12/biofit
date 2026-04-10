from .models import ClientProfile, Action, Observation, State, Reward
from .tasks import get_task, grade_action
import random

class BioFitEnvironment:
    def __init__(self):
        self.client_profile = None
        self.current_step = 0
        self.max_steps = 3
        self.total_score = 0.0
        self.task = None

    def reset(self, difficulty: str = "easy") -> Observation:
        self.task = get_task(difficulty)
        self.client_profile = self.task["client_profile"]
        self.current_step = 0
        self.total_score = 0.0
        return Observation(
            client_profile=self.client_profile,
            feedback="New client loaded. Prescribe a workout plan.",
            step_number=self.current_step
        )

    def step(self, action: Action) -> tuple[Observation, Reward, bool]:
        score = grade_action(self.task, action)
        reward = Reward(
            value=score,
            reason=f"Step {self.current_step + 1} scored {score:.2f}"
        )
        self.total_score += score
        self.current_step += 1
        done = self.current_step >= self.max_steps

        observation = Observation(
            client_profile=self.client_profile,
            feedback=f"Score so far: {self.total_score:.2f}. Keep going!" if not done else "Session complete!",
            step_number=self.current_step
        )
        return observation, reward, done

    def state(self) -> State:
        return State(
            client_profile=self.client_profile,
            current_step=self.current_step,
            done=self.current_step >= self.max_steps,
            total_score=self.total_score
        )