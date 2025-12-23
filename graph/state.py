from typing import Any, TypedDict, List, Optional

class AgentState(TypedDict, total=False):
    user_input: str
    tool_calls: List[Any]
    results: list
    final_answer: str
