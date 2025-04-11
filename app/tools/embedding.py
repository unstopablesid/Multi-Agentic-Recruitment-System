from typing import List
import requests
from langchain_core.embeddings import Embeddings

class OllamaEmbeddings(Embeddings):
    def __init__(self, model_name: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model_name,
                    "prompt": text
                }
            )
            if response.status_code == 200:
                embeddings.append(response.json()["embedding"])
            else:
                raise Exception(f"Error getting embeddings: {response.text}")
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": self.model_name,
                "prompt": text
            }
        )
        if response.status_code == 200:
            return response.json()["embedding"]
        else:
            raise Exception(f"Error getting embedding: {response.text}") 