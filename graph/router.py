# graph/router.py
from langchain_openai import OpenAIEmbeddings
from graph.bigTools_registry import bigtools
import numpy as np

class EmbeddingBasedRouter:
    """
    Router de tools basado en embeddings.
    
    - get_tool_by_name(): resolución directa (usado por el planner)
    - select_tool(): fallback semántico si el planner falla
    """

    def __init__(self, tools, embeddings, k: int = 1):
        self.tools = tools
        self.embeddings = embeddings
        self.k = k

        # 🔥 Índice por nombre (rápido y seguro)
        self.tool_map = {tool.name: tool for tool in tools}

        # Pre-calcular embeddings de descripciones (1 sola vez)
        self.tool_embeddings = self._compute_tool_embeddings()

    # -------------------------
    # EMBEDDINGS
    # -------------------------

    def _compute_tool_embeddings(self):
        descriptions = [
            f"{tool.name}: {tool.description}"
            for tool in self.tools
        ]
        return self.embeddings.embed_documents(descriptions)

    def select_tool(self, query: str):
        """
        Selecciona la tool más relevante usando similitud coseno.
        Útil como fallback cuando el planner no acierta.
        """
        query_embedding = self.embeddings.embed_query(query)

        similarities = []
        for tool_emb in self.tool_embeddings:
            similarity = np.dot(query_embedding, tool_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(tool_emb)
            )
            similarities.append(similarity)

        top_indices = np.argsort(similarities)[-self.k:][::-1]
        selected_tools = [self.tools[i] for i in top_indices]

        return selected_tools[0] if self.k == 1 else selected_tools

    # -------------------------
    # RESOLUCIÓN DIRECTA
    # -------------------------

    def get_tool_by_name(self, name: str):
        """
        Devuelve una tool por nombre exacto.
        Lanza error claro si no existe.
        """
        tool = self.tool_map.get(name)

        if not tool:
            raise ValueError(
                f"Tool '{name}' no registrada. "
                f"Disponibles: {list(self.tool_map.keys())}"
            )

        return tool


# -------------------------
# INSTANCIA GLOBAL
# -------------------------

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

bigtool_router = EmbeddingBasedRouter(
    tools=bigtools,
    embeddings=embeddings,
    k=1,
)
