import re
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool



# ---------------------------
# SCHEMAS
# ---------------------------

class SumaArgs(BaseModel):
    a: float = Field(..., description="Primer número")
    b: float = Field(..., description="Segundo número")

# ---------------------------
# FUNCIONES PURAS
# ---------------------------

def suma(a: float, b: float) -> str:
    return f"La suma de {a} y {b} es {a + b}"

# ---------------------------
# TOOLS
# ---------------------------

suma_tool = StructuredTool.from_function(
    func=suma,
    name="suma",
    description="Suma dos números",
    args_schema=SumaArgs,
)


# Tool Tavily (Internet)
tavily_tool = TavilySearchResults(
    max_results=5
)


#  Wikipedia
wiki_api = WikipediaAPIWrapper(
    top_k_results=3,
    doc_content_chars_max=2000
)
wikipedia_tool = Tool(
    name="wikipedia",
    func=wiki_api.run,
    description="Busca información enciclopédica en Wikipedia"
)


class Concat2Args(BaseModel):
    a: str = Field(..., description="Primera palabra")
    b: str = Field(..., description="Segunda palabra")

def concat_2(a: str, b: str) -> str:
    return f"Concatenación: {a}{b}"

concat2_tool = StructuredTool.from_function(
    func=concat_2,
    name="concat_2",
    description="Concatena dos palabras o textos",
    args_schema=Concat2Args,
)

class Concat3Args(BaseModel):
    a: str = Field(..., description="Primera palabra")
    b: str = Field(..., description="Segunda palabra")
    c: str = Field(..., description="Tercera palabra")

def concat_3(a: str, b: str, c: str) -> str:
    return f"Concatenación: {a}{b}{c}"

concat3_tool = StructuredTool.from_function(
    func=concat_3,
    name="concat_3",
    description="Concatena tres palabras o textos",
    args_schema=Concat3Args,
)


class JoinArgs(BaseModel):
    words: list[str] = Field(..., description="Lista de palabras")
    separator: str = Field(..., description="Separador entre palabras")

def join_words(words: list[str], separator: str) -> str:
    return separator.join(words)

join_tool = StructuredTool.from_function(
    func=join_words,
    name="join_words",
    description="Une una lista de palabras usando un separador",
    args_schema=JoinArgs,
)

class RepeatArgs(BaseModel):
    word: str = Field(..., description="Palabra a repetir")
    times: int = Field(..., description="Número de repeticiones")

def repeat_word(word: str, times: int) -> str:
    return " ".join([word] * times)

repeat_tool = StructuredTool.from_function(
    func=repeat_word,
    name="repeat_word",
    description="Repite una palabra un número dado de veces",
    args_schema=RepeatArgs,
)