"""Day 3: Ask the LLM questions with one external tool."""

import sys
import os
import json

# Reuse config.py from Day1_Practice
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day1_Practice")
    )
)

from config import client, MODEL
from my_tool import lookup_book, TOOL_SCHEMA


questions = [
    "What is a variable in Python?",
    "What is the current number of available copies of AI202 in our library?",
    "What is the purpose of a database?"
]


def ask_llm_with_tool(question):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Answer questions briefly and clearly in 1 or 2 sentences. "
                "Use the lookup_book tool only when the question requires "
                "current library book availability information. "
                "Do not use the tool for general knowledge questions."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # First LLM call
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[TOOL_SCHEMA],
        tool_choice="auto"
    )

    message = response.choices[0].message

    # If no tool is needed
    if not message.tool_calls:
        return {
            "tool_call": None,
            "answer": message.content
        }

    # Tool was requested
    tool_call = message.tool_calls[0]

    print("\n--- TOOL CALL ---")
    print("Tool:", tool_call.function.name)
    print("Arguments:", tool_call.function.arguments)

    arguments = json.loads(tool_call.function.arguments)

    if tool_call.function.name == "lookup_book":
        tool_result = lookup_book(arguments["book_code"])
    else:
        tool_result = "Unknown tool requested."

    print("Tool result:")
    print(tool_result)

    # Add the assistant's tool request
    messages.append(message)

    # Add the tool result
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_result
        }
    )

    # Second LLM call to produce final answer
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return {
        "tool_call": tool_call.function.name,
        "answer": final_response.choices[0].message.content
    }


print("=" * 60)
print("DAY 3 - WITH ONE TOOL")
print("=" * 60)

for i, question in enumerate(questions, start=1):

    print("\n" + "=" * 60)
    print(f"Question {i}: {question}")

    result = ask_llm_with_tool(question)

    print("\nFinal Answer:")
    print(result["answer"])