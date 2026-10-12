
"""Compare unconstrained text, JSON mode, and schema mode."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load the .env file from Day1_Task
env_path = (
    Path(__file__).resolve().parent.parent
    / "Day1_Task"
    / ".env"
)

load_dotenv(env_path)


TEXT = (
    'Extract from this request: "Maya wants a sandwich and coffee, '
    'and plans to visit the library on Saturday." '
    "Return student, items, building, and day."
)


SCHEMA = {
    "type": "object",
    "properties": {
        "student": {
            "type": "string"
        },
        "items": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["coffee", "tea", "sandwich", "juice"]
            }
        },
        "building": {
            "type": "string",
            "enum": ["library", "gym", "computer_lab"]
        },
        "day": {
            "type": "string",
            "enum": ["weekday", "saturday", "sunday"]
        }
    },
    "required": ["student", "items", "building", "day"],
    "additionalProperties": False
}


def make_client():
    provider = os.getenv("PROVIDER", "groq").strip().lower()
    model = os.getenv("MODEL", "openai/gpt-oss-20b").strip()

    if provider == "groq":
        key = os.getenv("GROQ_API_KEY")

        if not key:
            raise SystemExit(
                f"GROQ_API_KEY not found. Checked: {env_path}"
            )

        client = OpenAI(
            api_key=key,
            base_url="https://api.groq.com/openai/v1"
        )

    elif provider == "huggingface":
        key = os.getenv("HF_TOKEN")

        if not key:
            raise SystemExit(
                f"HF_TOKEN not found. Checked: {env_path}"
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
            "Unknown PROVIDER. Use groq, huggingface, or ollama."
        )

    return client, model, provider


def validate_schema_result(data):
    """Check the extracted data against our expected schema."""

    if not isinstance(data, dict):
        return False

    required = set(SCHEMA["required"])

    # Check missing or unexpected fields
    if set(data.keys()) != required:
        return False

    # Check student
    if not isinstance(data["student"], str):
        return False

    # Check items
    allowed_items = SCHEMA["properties"]["items"]["items"]["enum"]

    if not isinstance(data["items"], list):
        return False

    if not all(
        isinstance(item, str) and item in allowed_items
        for item in data["items"]
    ):
        return False

    # Check building
    allowed_buildings = SCHEMA["properties"]["building"]["enum"]

    if data["building"] not in allowed_buildings:
        return False

    # Check day
    allowed_days = SCHEMA["properties"]["day"]["enum"]

    if data["day"] not in allowed_days:
        return False

    return True


def run_case(client, model, label, options):
    print(f"\n=== {label} ===")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract the requested fields faithfully. "
                        "The student is Maya. Include the requested "
                        "items, building, and day. "
                        "Use lowercase enum values. "
                        "For JSON/schema cases, return the object only."
                    )
                },
                {
                    "role": "user",
                    "content": TEXT
                }
            ],
            temperature=0,
            max_tokens=500,
            **options
        )

        raw = response.choices[0].message.content or ""

        print("RAW REPLY:\n", raw)

        try:
            parsed = json.loads(raw)

            print(
                "PARSED RESULT:\n",
                json.dumps(
                    parsed,
                    indent=2,
                    ensure_ascii=False
                )
            )

            if label == "SCHEMA MODE":
                is_valid = validate_schema_result(parsed)

                print(
                    "SCHEMA VALIDATION:",
                    "PASS" if is_valid else "FAIL"
                )

        except json.JSONDecodeError:
            print("JSON PARSING: FAIL — reply is not valid JSON.")

    except Exception as exc:
        print(
            "ERROR:",
            f"{type(exc).__name__}: {exc}"
        )


def main():
    client, model, provider = make_client()

    print(
        f"=== STRUCTURED OUTPUTS | "
        f"provider={provider} | model={model} ==="
    )

    # Case 1: No response-format constraint
    run_case(
        client,
        model,
        "NO CONSTRAINT",
        {}
    )

    # Case 2: JSON mode
    run_case(
        client,
        model,
        "JSON MODE",
        {
            "response_format": {
                "type": "json_object"
            }
        }
    )

    # Case 3: JSON Schema mode
    run_case(
        client,
        model,
        "SCHEMA MODE",
        {
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "campus_request",
                    "strict": True,
                    "schema": SCHEMA
                }
            }
        }
    )


if __name__ == "__main__":
    main()
