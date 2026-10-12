
"""
Day 5 Task: Ollama REST API testing

Demonstrates:
1. Non-streaming /api/generate
2. Streaming /api/generate
3. Three different prompts and a repeated prompt
4. TTFT, total time, and tokens per second
5. Model loading status using /api/ps
6. OpenAI-compatible endpoint with a different system prompt

Requirements:
    python -m pip install requests

Start Ollama before running this script.
"""

import json
import time
import requests


OLLAMA_URL = "http://localhost:11434"
CUSTOM_MODEL = "coding-helper"


def check_model_status():
    """Display models currently loaded in Ollama memory."""
    print("\n--- Models currently loaded (before tests) ---")

    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/ps",
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        models = data.get("models", [])

        if not models:
            print("No models are currently loaded.")
        else:
            for model in models:
                print(
                    f"Model: {model.get('name', 'Unknown')}, "
                    f"Size: {model.get('size', 'Unknown')}, "
                    f"VRAM: {model.get('size_vram', 'Unknown')}"
                )

    except requests.RequestException as error:
        print(f"Could not check model status: {error}")


def calculate_tokens_per_second(data):
    """Calculate generation speed from Ollama timing statistics."""
    token_count = data.get("eval_count", 0)
    duration_ns = data.get("eval_duration", 0)

    if token_count and duration_ns:
        return token_count / (duration_ns / 1_000_000_000)

    return None


def non_streaming_request(prompt):
    """Send a non-streaming request to /api/generate."""
    print("\n--- NON-STREAMING REQUEST ---")
    print(f"Prompt: {prompt}")

    payload = {
        "model": CUSTOM_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    start_time = time.perf_counter()

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=600,
        )
        response.raise_for_status()

        data = response.json()
        total_time = time.perf_counter() - start_time

        print("\nModel response:")
        print(data.get("response", ""))

        speed = calculate_tokens_per_second(data)

        print(f"\nTotal time: {total_time:.3f} seconds")

        if speed is not None:
            print(f"Tokens per second: {speed:.2f}")
        else:
            print("Tokens per second: unavailable")

        print(
            "TTFT: Not separately measured by this "
            "non-streaming request."
        )

        print(
            f"Prompt tokens: {data.get('prompt_eval_count', 'Unknown')}"
        )
        print(
            f"Generated tokens: {data.get('eval_count', 'Unknown')}"
        )

        return data

    except requests.RequestException as error:
        print(f"Non-streaming request failed: {error}")
        return None


def streaming_request(prompt):
    """Stream a response and measure TTFT and generation speed."""
    print("\n--- STREAMING REQUEST ---")
    print(f"Prompt: {prompt}")
    print("\nModel response:")

    payload = {
        "model": CUSTOM_MODEL,
        "prompt": prompt,
        "stream": True,
    }

    start_time = time.perf_counter()
    first_token_time = None
    final_data = {}
    response_parts = []

    try:
        with requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            stream=True,
            timeout=(10, 600),
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                data = json.loads(line)

                text = data.get("response", "")

                if text:
                    if first_token_time is None:
                        first_token_time = time.perf_counter()

                    response_parts.append(text)
                    print(text, end="", flush=True)

                if data.get("done"):
                    final_data = data

        end_time = time.perf_counter()
        total_time = end_time - start_time

        print()

        if first_token_time is not None:
            ttft = first_token_time - start_time
            print(f"TTFT: {ttft:.3f} seconds")
        else:
            print("TTFT: No generated text received.")

        speed = calculate_tokens_per_second(final_data)

        if speed is not None:
            print(f"Tokens per second: {speed:.2f}")
        else:
            print("Tokens per second: unavailable")

        print(f"Total time: {total_time:.3f} seconds")
        print(
            f"Generated tokens: "
            f"{final_data.get('eval_count', 'Unknown')}"
        )

        return {
            "response": "".join(response_parts),
            "ttft_seconds": (
                first_token_time - start_time
                if first_token_time is not None
                else None
            ),
            "total_time_seconds": total_time,
            "tokens_per_second": speed,
            "eval_count": final_data.get("eval_count"),
        }

    except (requests.RequestException, json.JSONDecodeError) as error:
        print(f"\nStreaming request failed: {error}")
        return None


def openai_compatible_request():
    """
    Call the OpenAI-compatible endpoint with a custom system prompt.
    This prompt is intentionally different from the Modelfile SYSTEM.
    """
    print("\n--- OPENAI-COMPATIBLE ENDPOINT TEST ---")

    custom_system_prompt = (
        "You are a concise study assistant. "
        "Answer in exactly three short bullet points. "
        "Do not use code blocks."
    )

    user_prompt = (
        "Explain what a Python function is."
    )

    payload = {
        "model": CUSTOM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": custom_system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "stream": False,
        "temperature": 0.2,
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/v1/chat/completions",
            json=payload,
            timeout=600,
        )
        response.raise_for_status()

        data = response.json()

        answer = data["choices"][0]["message"]["content"]

        print("Custom program system prompt:")
        print(custom_system_prompt)

        print("\nModel response:")
        print(answer)

        print(
            "\nCheck whether the response follows the "
            "three-bullet instruction."
        )

    except (requests.RequestException, KeyError, IndexError) as error:
        print(f"OpenAI-compatible request failed: {error}")


def main():
    print("DAY 5 TASK: OLLAMA API TEST")
    print(f"Custom model: {CUSTOM_MODEL}")

    # Check whether the model is already loaded.
    check_model_status()

    # Test a non-streaming request.
    non_streaming_request(
        "Explain a Python variable in simple English."
    )

    # Three different prompts for the observation section.
    prompts = [
        "Explain a Python variable in simple English.",
        "Explain a Python for loop with a short example.",
        "What is the capital of France? Follow your Modelfile rules.",
    ]

    for index, prompt in enumerate(prompts, start=1):
        print(f"\n========== PROMPT {index} ==========")
        streaming_request(prompt)

    # Repeat the first prompt to compare consecutive runs.
    print("\n========== REPEATED PROMPT 1 ==========")
    streaming_request(prompts[0])

    # Test whether the program's system prompt changes behavior.
    openai_compatible_request()

    # Check the loaded model after the tests.
    check_model_status()


if __name__ == "__main__":
    main()