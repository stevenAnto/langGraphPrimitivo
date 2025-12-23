from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import  answer_node, executor_node, planner_node

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)
builder.add_node("executor", executor_node)
builder.add_node("answer", answer_node)

builder.set_entry_point("planner")

builder.add_edge("planner", "executor")

builder.add_conditional_edges( ##Hasta que el estado diga que pare, recien se detiende
    "executor",
    lambda state: "answer" if state["done"] else "executor"
)

builder.add_edge("answer", END)

graph = builder.compile()

