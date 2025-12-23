from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union


class PlanStep(BaseModel):
    task: str          # intención en lenguaje natural
    input: str         # texto concreto de esa tarea

class ExecutionPlan(BaseModel):
    steps: List[PlanStep]