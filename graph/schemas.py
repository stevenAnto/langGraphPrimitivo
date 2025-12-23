from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union

ToolName = Literal[
    "suma",
    "tavily",
    "wikipedia",
    "concat_words",
    "repeat_word",
]

class PlanStep(BaseModel):
    tool: ToolName
    args: Union[str, Dict[str, Any]]

class ExecutionPlan(BaseModel):
    steps: List[PlanStep]