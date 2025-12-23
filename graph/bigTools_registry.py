# graph/bigtools.py

from typing import Any, Optional, Type

from pydantic import BaseModel
from graph.tools import SumaArgs, tavily_tool, wikipedia_tool,suma_tool
from dataclasses import dataclass



@dataclass
class BigTool:
    name: str
    description: str
    tool: Any
    args_schema: Optional[Type[BaseModel]] = None

bigtools = [
    BigTool(
        name="tavily",
        description="Busca información en internet",
        tool=tavily_tool,
        args_schema=None,       # texto libre
    ),
    BigTool(
        name="wikipedia",
        description="Busca información enciclopédica, definiciones y conceptos",
        tool=wikipedia_tool,
    ),
    BigTool(
        name="suma",
        description="Suma dos números",
        tool=suma_tool,
        args_schema=SumaArgs,   # 🔥 IMPORTANTE
    ),
]
