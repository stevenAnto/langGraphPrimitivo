import json
import re
from langchain_openai import ChatOpenAI
from graph.llm import llm
from graph.state import AgentState
from graph.router import bigtool_router
from graph.schemas import ExecutionPlan
from graph.bigTools_registry import bigtools


def planner_node(state):
    print("antes planner_node")
    print(state)

    user_input = state["user_input"]

    planner_llm = llm.with_structured_output(
        ExecutionPlan,
        method="function_calling"
    )

    plan = planner_llm.invoke(f"""
    You are a TASK DECOMPOSER for a tool-based system.

    Your job is to split the user request into the MINIMUM number of
    EXECUTABLE tasks.

    Definition:
    - A task MUST be solvable by calling exactly ONE tool.
    - Do NOT split into reasoning steps.
    - Do NOT include internal thinking steps.
    - Do NOT include "identify", "analyze", "return" steps.

    Each task must be something that a single function could execute.

    Return JSON only.

    User request:
    {user_input}
    """)

    print("PLAN PARSED OK")
    print(plan)

    return {
        "plan": plan.steps,
        "step_index": 0,
        "results": [],
        "done": False
    }


def executor_node(state):
    print("antes executor_node")
    print(state)

    plan = state["plan"]
    i = state["step_index"]

    if i >= len(plan):
        return {"done": True}

    step = plan[i]

    semantic_text = f"{step.task}. {step.input}"

    selected_tool = bigtool_router.select_tool(semantic_text)
    print("tool seleccionada:", selected_tool.name)

    if selected_tool.args_schema:
        tool_args = extract_args(
            llm=llm,
            tool=selected_tool,
            user_input=semantic_text
        )
        tool_args = tool_args.dict()
    else:
        tool_args = semantic_text

    print("args extraidos:", tool_args)

    result = selected_tool.tool.invoke(tool_args)

    return {
        "results": state["results"] + [result],
        "step_index": i + 1,
        "done": False
    }

def answer_node(state: AgentState):
    print("antes answer_node")
    print(state)
    prompt = f"""
Usa los siguientes resultados para responder al usuario:

Pregunta:
{state["user_input"]}

Resultados:
{state["results"]}
"""

    response = llm.invoke(prompt)
    print("despues answer_node")
    print(state)
    return {"final_answer": response.content}



####Funciones auxiliares#######

def build_tools_description(bigtools):
    blocks = []

    for t in bigtools:
        if t.args_schema:
            fields = []
            for name, field in t.args_schema.model_fields.items():
                fields.append(
                    f"- {name}: {field.annotation.__name__}"
                )
            args_desc = "\n".join(fields)
        else:
            args_desc = "- args: string"

        blocks.append(
            f"""
Tool name: {t.name}
Description: {t.description}
Arguments:
{args_desc}
"""
        )

    return "\n".join(blocks)



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