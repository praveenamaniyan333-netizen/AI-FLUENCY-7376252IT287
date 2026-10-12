"""
Day 2:
ReAct Agent

Uses the existing tools.py from Day1_Practice.

Scenario:
College Library Book Rental

ReAct cycle:

Thought -> Action -> Observation -> Final Answer
"""

import json
import sys
from pathlib import Path


# ---------------------------------------------------------
# Import Day 1 config.py and tools.py
# ---------------------------------------------------------

DAY1_PATH = (
    Path(__file__).resolve().parent.parent
    / "Day1_Practice"
)

sys.path.insert(0, str(DAY1_PATH))


from config import client, MODEL, banner
from tools import TOOLS, TOOL_FUNCTIONS


# ---------------------------------------------------------
# Question
# ---------------------------------------------------------

QUESTION = (
    "How much will it cost to borrow AI202 for 3 days?"
)


SYSTEM_PROMPT = """
You are a college library assistant.

You have access to a tool called get_book_details.
Use this tool whenever you need book information such as
the rental price.

You also have a calculator tool for arithmetic.

Never guess book information.

Follow the ReAct process:

Thought -> Action -> Observation -> Final Answer

For the user's question:
1. Get the book details using the appropriate tool.
2. Use the calculator if arithmetic is required.
3. Use the observation to produce the final answer.

Give a concise final answer.
"""


def react_agent(question, max_steps=6):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # -------------------------------------------------
        # REASON
        # -------------------------------------------------

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            parallel_tool_calls=False,
            temperature=0
        )

        message = response.choices[0].message

        # -------------------------------------------------
        # FINAL ANSWER
        # -------------------------------------------------

        if not message.tool_calls:

            print("\nFINAL ANSWER:")
            print(message.content.strip())

            return message.content.strip()

        # -------------------------------------------------
        # THOUGHT
        # -------------------------------------------------

        if message.content:

            print(f"\nTHOUGHT {step}:")
            print(message.content.strip())

        # -------------------------------------------------
        # ASSISTANT TOOL CALL
        # -------------------------------------------------

        assistant_tool_calls = []

        for call in message.tool_calls:

            assistant_tool_calls.append(
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
            )

        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": assistant_tool_calls
            }
        )

        # -------------------------------------------------
        # ACTION + OBSERVATION
        # -------------------------------------------------

        for call in message.tool_calls:

            tool_name = call.function.name

            arguments = json.loads(
                call.function.arguments or "{}"
            )

            print(f"\nACTION {step}:")
            print(f"Tool: {tool_name}")
            print(f"Arguments: {arguments}")

            function = TOOL_FUNCTIONS.get(tool_name)

            if function is None:

                result = f"Unknown tool: {tool_name}"

            else:

                try:

                    result = function(**arguments)

                except Exception as error:

                    result = f"Tool error: {error}"

            print("\nOBSERVATION:")
            print(result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                }
            )

    print(
        "\nStopped: maximum number of ReAct steps reached."
    )

    return "No final answer."


if __name__ == "__main__":

    banner("DAY 2: ReACT AGENT")

    print("SCENARIO: College Library Book Rental")

    print("\nQUESTION:")
    print(QUESTION)

    print("\n" + "=" * 70)

    react_agent(QUESTION)