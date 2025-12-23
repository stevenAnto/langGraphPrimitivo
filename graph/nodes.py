import re
from langchain_openai import ChatOpenAI
from graph.llm import llm
from graph.state import AgentState
from graph.router import bigtool_router




def router_node(state: AgentState):
    """Selecciona y ejecuta la tool usando embeddings (NO LLM para selección)"""
    user_input = state["user_input"]
    
    print("\n=== ROUTER NODE - INICIO ===")
    print(f"User Input: {user_input}")
    
    # AQUÍ SE USA EMBEDDINGS (barato) para seleccionar la tool
    selected_bigtool = bigtool_router.select_tool(user_input)
    print(f"Tool seleccionada: {selected_bigtool.name}")
    print(f"Descripcion de la tool: {selected_bigtool.description}")
    
    # Ejecutar la tool seleccionada
    print(f"Ejecutando tool: {selected_bigtool.name}")
    args = extract_args(llm, selected_bigtool.tool, user_input)
    tool_result = selected_bigtool.tool.invoke(args.dict()) ## Clave para pasar los arguemtnos adecuados


    #tool_result = selected_bigtool.tool.invoke({"query": user_input})
    print(f"Resultado de la tool: {tool_result}")
    print("=== ROUTER NODE - FIN ===\n")
    
    return {
        "plan": f"Tool seleccionada con embeddings: {selected_bigtool.name}",
        "results": [tool_result]
    }


def answer_node(state: AgentState):
    """Genera respuesta final (aquí SÍ usamos LLM pero solo una vez)"""
    user_input = state["user_input"]
    results = state.get("results", [])
    
    print("\n=== ANSWER NODE - INICIO ===")
    print(f"User Input: {user_input}")
    print(f"Results recibidos: {results}")
    
    if not results:
        print("No hay resultados disponibles")
        return {"final_answer": "No encontre informacion relevante."}
    
    # Solo UNA llamada al LLM para generar la respuesta final
    prompt = f"""Responde la pregunta del usuario usando esta informacion:

Pregunta: {user_input}

Informacion:
{results[0]}

Responde de forma clara y concisa."""
    
    print("Generando respuesta final con LLM...")
    response = llm.invoke(prompt)
    print(f"Respuesta generada: {response.content[:200]}...")
    print("=== ANSWER NODE - FIN ===\n")
    
    return {"final_answer": response.content}


def extract_args(llm, tool, user_input: str):
    prompt = f"""
Extrae los argumentos para esta herramienta.

Herramienta: {tool.name}
Descripción: {tool.description}
Schema: {tool.args_schema.schema_json()}

Texto del usuario:
"{user_input}"

Devuelve SOLO JSON válido. No markdown. No texto adicional.
"""
    response = llm.invoke(prompt)
    raw = response.content.strip()

    #  LIMPIAR ```json ``` si existen
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    return tool.args_schema.parse_raw(raw)