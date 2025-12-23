# graph/bigtools.py

from typing import Any, Optional, Type

from pydantic import BaseModel

from dataclasses import dataclass
from graph.tools import (
    SumaArgs,
    Concat2Args,
    Concat3Args,
    JoinArgs,
    RepeatArgs,
    suma_tool,
    concat2_tool,
    concat3_tool,
    join_tool,
    repeat_tool,
    tavily_tool,
    wikipedia_tool
)



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
        args_schema=SumaArgs,
    ),
    BigTool(
        name="concat_2",
        description="Concatena dos palabras o textos",
        tool=concat2_tool,
        args_schema=Concat2Args,
    ),
    BigTool(
        name="concat_3",
        description="Concatena tres palabras o textos",
        tool=concat3_tool,
        args_schema=Concat3Args,
    ),
    BigTool(
        name="join_words",
        description="Une varias palabras con un separador",
        tool=join_tool,
        args_schema=JoinArgs,
    ),
    BigTool(
        name="repeat_word",
        description="Repite una palabra varias veces",
        tool=repeat_tool,
        args_schema=RepeatArgs,
    ),
]
