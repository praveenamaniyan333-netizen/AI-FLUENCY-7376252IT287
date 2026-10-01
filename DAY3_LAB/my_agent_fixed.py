"""Day 3: ReAct agent with three guards."""

import json
import sys
import os

# Reuse config.py from Day1_Lab
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day1_Lab")
    )
)

from config import client, MODEL, banner
from my_agent import SYSTEM_PROMPT
from my_tools import TOOLS, TOOL_FUNCTIONS


# Guard 2: maximum size of one tool observation
MAX_TOOL_CHARS = 1500

# Guard 3: maximum total characters sent to model
CHAR_BUDGET = 30000


def agent(question, max_steps=6, verbose=True):

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

    # Guard 1: detect repeated tool calls
    seen_calls = {}

    # Guard 3: track characters sent
    chars_sent = 0

    for step in range(1, max_steps + 1):

        # -----------------------------------------
        # Guard 3: Character budget
        # -----------------------------------------

        chars_sent += sum(
            len(str(m.get("content", "")))
            for m in messages
        )

        if chars_sent > CHAR_BUDGET:
            return (
                f"Stopped: character budget exceeded "
                f"({chars_sent} sent)."
            )

        # Ask the model
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # No tool call = final answer
        if not message.tool_calls:
            return message.content.strip()

        # Record assistant tool call
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        # -----------------------------------------
        # Execute tools
        # -----------------------------------------

        for call in message.tool_calls:

            name = call.function.name
            arguments = {}

            try:

                arguments = json.loads(
                    call.function.arguments or "{}"
                )

                function = TOOL_FUNCTIONS.get(name)

                if function is None:

                    result = (
                        f"Unknown tool: {name}. "
                        f"Available: {list(TOOL_FUNCTIONS)}"
                    )

                else:

                    result = function(**arguments)

            except json.JSONDecodeError as error:

                result = (
                    f"Argument error: {error}. "
                    f"Send valid JSON."
                )

            except TypeError as error:

                result = f"Argument error: {error}"

            result = str(result)

            # -----------------------------------------
            # Guard 1: Repeat detection
            # -----------------------------------------

            signature = (
                name,
                json.dumps(
                    arguments,
                    sort_keys=True
                )
            )

            seen_calls[signature] = (
                seen_calls.get(signature, 0) + 1
            )

            if seen_calls[signature] >= 3:

                return (
                    f"Stopped: the tool {name} was called "
                    f"3 times with the same arguments and "
                    f"no progress was made. Last result: "
                    f"{result[:200]}"
                )

            # -----------------------------------------
            # Guard 2: Observation limit
            # -----------------------------------------

            if len(result) > MAX_TOOL_CHARS:

                result = (
                    result[:MAX_TOOL_CHARS]
                    + " ... [observation truncated]"
                )

            # Display tool execution
            if verbose:

                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> "
                    f"{result[:120]}"
                )

            # Add result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "Stopped: maximum steps reached without a final answer."


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    banner("MY AGENT (guards on)")

    for question in [
        "Read notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.",

        "Read fees.html and tell me the fee for CS101.",

        "Read big.html and tell me how many students are listed.",
    ]:

        print("\nQ:", question)

        print("A:", agent(question))