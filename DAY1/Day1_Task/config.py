import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Provider settings
PROVIDER = os.getenv("PROVIDER", "ollama")
MODEL = os.getenv("MODEL", "qwen2.5:1.5b")

# Create client
if PROVIDER == "ollama":
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

elif PROVIDER == "groq":
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )

elif PROVIDER == "huggingface":
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_API_KEY")
    )

else:
    raise ValueError("Invalid provider")


# Private college library data
BOOKS = {
    "PY101": {
        "name": "Python Programming",
        "copies": 4,
        "fine_per_day": 5
    },

    "AI202": {
        "name": "Artificial Intelligence",
        "copies": 2,
        "fine_per_day": 10
    },

    "DB303": {
        "name": "Database Systems",
        "copies": 5,
        "fine_per_day": 7
    }
}


# Questions for the practice task
QUESTIONS = [
    "How many copies of AI202 are available?",
    "What is the fine for 5 days for AI202?",
    "Is DB303 more available than AI202, and by how many copies?",
    "Write a welcome message for new library members."
]


def banner(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)