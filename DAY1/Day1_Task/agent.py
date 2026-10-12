import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college library AI agent. "
    "Use get_book_details for library data. "
    "Use safe_calculate for calculations. "
    "Never guess private data. "
    "Give short final answers."
)


def agent(question, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=100
        )

        message = response.choices[0].message

        # If the agent wants to use a tool
        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                result = TOOL_FUNCTIONS[tool_name](**arguments)

                # Short tool output for screenshot
                short_result = str(result).replace("\n", " | ")
                print(f"[Tool: {tool_name}] -> {short_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        # Final answer
        else:
            answer = message.content

            if answer and answer.strip():
                return answer.strip()

            # Safety fallback if model returns empty text
            return "Answer generated from the tool result."

    return "Agent stopped."


def main():
    banner("AI AGENT")

    for question in QUESTIONS:
        print("\nQ:", question)
        print("A:", agent(question))


if __name__ == "__main__":
    main()