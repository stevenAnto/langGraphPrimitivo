from graph.state import AgentState

def should_continue(state: AgentState) -> str:
    print("\n🔀 [EDGE should_continue]")
    print("Estado recibido:")
    print(state)

    results_count = len(state["results"])
    print(f"Cantidad de resultados: {results_count}")

    if results_count < 2:
        decision = "search"
    else:
        decision = "answer"

    print(f"Decisión tomada: {decision}")
    print("🔀 [EDGE END]\n")

    return decision
