
"""Configuration for the standalone Day 8 project."""

import hashlib
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"

# Load environment variables from this project's .env file
load_dotenv(BASE_DIR / ".env")

EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "hash").lower()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()


class HashEmbeddings(Embeddings):
    """Simple offline embeddings for lab practice."""

    def __init__(self, dimensions=256):
        self.dimensions = dimensions

    def _embed(self, text):
        vector = [0.0] * self.dimensions
        words = re.findall(r"[a-z0-9]+", text.lower())

        for word in words:
            digest = hashlib.sha256(word.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        # Normalize the vector
        magnitude = sum(value * value for value in vector) ** 0.5

        if magnitude:
            vector = [value / magnitude for value in vector]

        return vector

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)


def get_embeddings():
    """Return the configured embedding model."""

    if EMBED_PROVIDER == "hash":
        return HashEmbeddings(dimensions=256)

    raise ValueError(
        f"Unsupported EMBED_PROVIDER={EMBED_PROVIDER!r}. "
        "This standalone version supports 'hash'."
    )


def get_vectorstore():
    """Return the persistent Chroma vector store."""

    return Chroma(
        collection_name="college_handbook",
        persist_directory=str(DB_DIR),
        embedding_function=get_embeddings(),
        collection_metadata={"hnsw:space": "cosine"},
    )


def get_model():
    """Return the configured chat model."""

    if LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "qwen2.5:3b"),
            temperature=0,
        )

    if LLM_PROVIDER in ("openai", "groq"):
        from langchain_openai import ChatOpenAI

        if LLM_PROVIDER == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            base_url = os.getenv(
                "GROQ_BASE_URL",
                "https://api.groq.com/openai/v1",
            )
            model_name = os.getenv(
                "GROQ_MODEL",
                "openai/gpt-oss-20b",
            )
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = None
            model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if not api_key:
            raise ValueError(
                f"Set the API key for provider {LLM_PROVIDER!r} in .env"
            )

        kwargs = {
            "model": model_name,
            "api_key": api_key,
            "temperature": 0,
        }

        if base_url:
            kwargs["base_url"] = base_url

        return ChatOpenAI(**kwargs)

    raise ValueError(
        f"Unsupported LLM_PROVIDER={LLM_PROVIDER!r}"
    )
