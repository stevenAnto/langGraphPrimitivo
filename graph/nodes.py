import json
import re
from langchain_openai import ChatOpenAI
from graph.llm import llm
from graph.state import AgentState
from graph.router import bigtool_router
from graph.schemas import ExecutionPlan
from graph.bigTools_registry import bigtools


def planner_node(state):
    print("antes planer_node ")
    print(state)
    user_input = state["user_input"]

    tools_description = build_tools_description(bigtools)

    planner_llm = llm.with_structured_output(
        ExecutionPlan,
        method="function_calling"
    )

    plan = planner_llm.invoke(f"""
You are a planner.

Available tools:
{tools_description}

Rules:
- Choose the correct tool
- args MUST match the argument schema EXACTLY
- Return JSON only

User request:
{user_input}
""")

    print("PLAN PARSED OK:", plan)
    print("despues plan_node")
    print(state)

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
    tool_wrapper = bigtool_router.get_tool_by_name(step.tool)

    raw_args = step.args

    if isinstance(raw_args, str):
        try:
            tool_args = json.loads(raw_args)
        except json.JSONDecodeError:
            tool_args = raw_args
    else:
        tool_args = raw_args

    result = tool_wrapper.tool.invoke(tool_args)
    print("despues executor_node")
    print(state)

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