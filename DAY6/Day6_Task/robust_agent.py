
"""Guarded agent using the OpenAI-compatible Chat Completions API."""

import json
import os
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, FUNCTIONS
from validator import validate_arguments


# Load the .env file from Day1_Task
env_path = (
    Path(__file__).resolve().parent.parent
    / "Day1_Task"
    / ".env"
)

load_dotenv(env_path)


def make_client():
    provider = os.getenv("PROVIDER", "groq").strip().lower()
    model = os.getenv("MODEL", "openai/gpt-oss-120b").strip()

    if provider == "groq":
        key = os.getenv("GROQ_API_KEY")

        if not key:
            raise SystemExit(
                f"GROQ_API_KEY was not found. Checked: {env_path}"
            )

        client = OpenAI(
            api_key=key,
            base_url="https://api.groq.com/openai/v1"
        )

    elif provider == "huggingface":
        key = os.getenv("HF_TOKEN")

        if not key:
            raise SystemExit(
                f"HF_TOKEN was not found. Checked: {env_path}"
            )

        client = OpenAI(
            api_key=key,
            base_url="https://router.huggingface.co/v1"
        )

    elif provider == "ollama":
        client = OpenAI(
            api_key=os.getenv("API_KEY", "ollama"),
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434/v1"
            )
        )

    else:
        raise SystemExit(
            "PROVIDER must be groq, huggingface, or ollama."
        )

    return client, model, provider


SYSTEM = """
You are a college campus assistant.

Use get_cafe_price for cafeteria prices.
Use get_campus_hours for campus building hours.
Never invent prices or opening hours.

For requests needing both tools, you may call both tools.

Allowed menu items: coffee, tea, sandwich, juice.
Allowed buildings: library, gym, computer_lab.
Allowed day types: weekday, saturday, sunday.

If a request is unsupported, explain the available choices.
"""


def handle_tool_call(tool_name, raw_arguments):
    # Stage 1: Parse JSON arguments
    try:
        if isinstance(raw_arguments, str):
            arguments = json.loads(raw_arguments)
        else:
            arguments = raw_arguments

    except (json.JSONDecodeError, TypeError):
        return (
            "ERROR: invalid JSON arguments. "
            "Send valid JSON object arguments."
        )

    # Ensure arguments are a JSON object
    if not isinstance(arguments, dict):
        return (
            "ERROR: Arguments must be a JSON object; "
            f"received {type(arguments).__name__}."
        )

    # Stage 2: Look up the tool
    function = FUNCTIONS.get(tool_name)

    if function is None:
        return (
            f"ERROR: unknown tool '{tool_name}'. "
            f"Available tools: {', '.join(FUNCTIONS)}."
        )

    # Stage 3: Validate arguments
    try:
        error = validate_arguments(tool_name, arguments)
    except Exception as exc:
        return (
            "ERROR: argument validation failed "
            f"({type(exc).__name__})."
        )

    if error:
        return "ERROR: " + error

    # Stage 4: Execute the tool safely
    try:
        result = function(**arguments)

        return json.dumps(
            {"ok": True, "result": result},
            ensure_ascii=False
        )

    except Exception as exc:
        return (
            "ERROR: tool execution failed "
            f"({type(exc).__name__}). Check arguments and try again."
        )


def run_question(
    client,
    model,
    question,
    max_steps=6,
    initial_max_tokens=500
):
    print(f"\nQUESTION: {question}")

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question}
    ]

    seen_calls = Counter()
    tool_names = []
    parallel = False
    length_seen = False
    max_tokens = initial_max_tokens

    for step in range(1, max_steps + 1):

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                parallel_tool_calls=True,
                max_tokens=max_tokens,
                temperature=0
            )

        except Exception as exc:
            print(
                f"API ERROR: {type(exc).__name__}: {exc}"
            )
            return

        choice = response.choices[0]
        message = choice.message
        finish_reason = choice.finish_reason

        print(f"step {step}: finish_reason={finish_reason}")

        # Retry if the response was truncated.
        # Do not add incomplete tool calls to the conversation.
        if finish_reason == "length":
            length_seen = True

            if max_tokens >= 4000:
                print(
                    "STOPPED: response was still truncated "
                    "at the maximum token limit."
                )
                return

            max_tokens = min(max_tokens * 2, 4000)

            messages.append({
                "role": "user",
                "content": (
                    "The previous response was truncated. "
                    "Please provide a complete response, including "
                    "complete tool arguments if tools are needed. "
                    f"The token limit is now {max_tokens}."
                )
            })

            print(
                "  Truncated reply: retrying with "
                f"max_tokens={max_tokens}"
            )
            continue

        # Save the completed assistant message
        assistant_message = {
            "role": "assistant",
            "content": message.content or ""
        }

        if message.tool_calls:
            assistant_message["tool_calls"] = [
                call.model_dump(exclude_none=True)
                for call in message.tool_calls
            ]

        messages.append(assistant_message)

        # Normal final answer
        if finish_reason == "stop" and not message.tool_calls:
            print("FINAL:", message.content or "(empty content)")
            print(
                f"SUMMARY: steps={step}, tools={tool_names}, "
                f"parallel={parallel}, length_seen={length_seen}"
            )
            return

        # Handle every tool call
        if finish_reason == "tool_calls" or message.tool_calls:
            calls = message.tool_calls or []

            if len(calls) > 1:
                parallel = True

            for call in calls:
                name = call.function.name
                raw_arguments = call.function.arguments

                tool_names.append(name)

                signature = (name, raw_arguments)
                seen_calls[signature] += 1

                print(
                    f"  tool call: {name} "
                    f"arguments={raw_arguments}"
                )

                # Stop repeated identical calls
                if seen_calls[signature] >= 3:
                    result = (
                        "ERROR: repeated identical tool call detected "
                        "three times. Stop retrying and answer using "
                        "available information."
                    )
                else:
                    result = handle_tool_call(
                        name,
                        raw_arguments
                    )

                # Send one result for every tool call ID
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                })

                print("  tool result:", result)

            continue

        # Handle unexpected response endings
        messages.append({
            "role": "user",
            "content": (
                f"The response ended with finish_reason={finish_reason}. "
                "Please provide a complete answer."
            )
        })

    print(f"STOPPED: maximum of {max_steps} steps reached.")
    print(
        f"SUMMARY: steps={max_steps}, tools={tool_names}, "
        f"parallel={parallel}, length_seen={length_seen}"
    )


def main():
    from validator import demo

    demo()

    client, model, provider = make_client()

    print(
        f"\n=== GUARDED CAMPUS AGENT | "
        f"provider={provider} | model={model} ==="
    )

    questions = [
        "What is the price of a sandwich?",

        "How much are coffee and tea together, "
        "and what are the library hours on a weekday?",

        "What is the price of pizza?",

        "Write a one-line welcome message for new students."
    ]

    for question in questions:
        run_question(client, model, question)


if __name__ == "__main__":
    main()
