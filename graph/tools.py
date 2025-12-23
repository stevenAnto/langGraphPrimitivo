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
