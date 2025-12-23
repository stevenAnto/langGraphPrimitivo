from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import  router_node, answer_node
from graph.router import bigtool_router

builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("answer", answer_node)

builder.set_entry_point("router")
builder.add_edge("router", "answer")
builder.add_edge("answer", END)

graph = builder.compile()

