# graph/bigtools.py

from typing import Any
from graph.tools import tavily_tool, wikipedia_tool,suma_tool
from dataclasses import dataclass



@dataclass
class BigTool:
    """Contenedor para herramientas con metadata para selección por embeddings"""
    name: str
    description: str
    tool: Any

bigtools = [
    BigTool(
        name="tavily",
        description="Busca información actualizada en internet, noticias y sitios web",
        tool=tavily_tool,
    ),
    BigTool(
        name="wikipedia",
        description="Busca información enciclopédica, definiciones y conceptos",
        tool=wikipedia_tool,
    ),
        BigTool(
        name="suma",
        description="Realiza operaciones de suma entre dos numeros. Util para calculos matematicos simples de suma",
        tool=suma_tool,
    ),
]
