# graph/router.py
from langchain_openai import OpenAIEmbeddings
from graph.bigTools_registry import bigtools
import numpy as np

class EmbeddingBasedRouter:
    def __init__(self, tools, embeddings, k=1):
        self.tools = tools
        self.embeddings = embeddings
        self.k = k
        
        # Pre-calcular embeddings de las descripciones de las tools (solo una vez)
        self.tool_embeddings = self._compute_tool_embeddings()
    
    def _compute_tool_embeddings(self):
        """Calcula embeddings de las descripciones de las tools"""
        descriptions = [f"{tool.name}: {tool.description}" for tool in self.tools]
        return self.embeddings.embed_documents(descriptions)
    
    def select_tool(self, query: str):
        """Selecciona la tool más relevante usando similitud de embeddings"""
        # Embedding de la query del usuario
        query_embedding = self.embeddings.embed_query(query)
        
        # Calcular similitud coseno con cada tool
        similarities = []
        for tool_emb in self.tool_embeddings:
            similarity = np.dot(query_embedding, tool_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(tool_emb)
            )
            similarities.append(similarity)
        
        # Seleccionar las top-k tools
        top_indices = np.argsort(similarities)[-self.k:][::-1]
        selected_tools = [self.tools[i] for i in top_indices]
        
        return selected_tools[0] if self.k == 1 else selected_tools

# Crear el router
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
bigtool_router = EmbeddingBasedRouter(
    tools=bigtools,
    embeddings=embeddings,
    k=1
)
