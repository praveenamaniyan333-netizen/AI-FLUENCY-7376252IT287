"""Day 3: Ask the LLM questions without any external tool."""

import sys
import os

# Reuse the configuration from Day1_Practice
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day1_Practice")
    )
)

from config import client, MODEL


questions = [
    "What is a variable in Python?",
    "What is the current number of available copies of AI202 in our library?",
    "What is the purpose of a database?"
]


def ask_llm(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Answer using only your own knowledge. "
                    "Do not use external tools. "
                    "Keep your answer short and clear, within 2 or 3 sentences. "
                    "If you do not have enough information to answer reliably, "
                    "say so instead of guessing."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


print("=" * 60)
print("DAY 3 - WITHOUT TOOL")
print("=" * 60)

for i, question in enumerate(questions, start=1):
    print(f"\nQuestion {i}: {question}")
    print("Answer:")
    print(ask_llm(question))