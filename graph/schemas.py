from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union


class PlanStep(BaseModel):
    tool: Literal["suma", "tavily"]
    args: Union[str, Dict[str, Any]]

class ExecutionPlan(BaseModel):
    steps: List[PlanStep]