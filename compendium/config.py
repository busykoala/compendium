from dataclasses import dataclass


@dataclass
class Config:
    embeddings_model: str = "text-embedding-3-large"
    chat_model: str = "gpt-4"
    vectorstore_dir: str = "output/vectorstore"
