from typing import Any, Dict, TypedDict, List, Optional

class AgentState(TypedDict):
    user_input: str
    plan: List[Any]
    step_index: int
    results: List[Any]
    done: bool                # condición de salida
