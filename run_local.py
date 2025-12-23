
from dotenv import load_dotenv
load_dotenv()
import os
from graph.graph import graph
from graph.state import AgentState

print("API KEY LOADED:", os.getenv("OPENAI_API_KEY") is not None)

initial_state: AgentState = {
    "user_input": "Busca en internet quien fue Alan Garcia",
    "plan": None,
    "results": [],
    "final_answer": None
}

final_state = graph.invoke(initial_state)

print("FINAL STATE:")
print(final_state)
