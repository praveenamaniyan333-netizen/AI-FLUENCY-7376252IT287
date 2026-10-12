import sys
from config import client, MODEL, PROVIDER, banner


def check_setup():
    banner("DAY 1 - SETUP CHECK")

    print("Python version:")
    print(sys.version)

    print("\nProvider:")
    print(PROVIDER)

    print("\nModel:")
    print(MODEL)

    print("\nTesting LLM connection...")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with SETUP OK"
                }
            ]
        )

        print("\nLLM Response:")
        print(response.choices[0].message.content)

        print("\nSetup completed successfully.")

    except Exception as e:
        print("\nSetup failed.")
        print("Error:", e)


if __name__ == "__main__":
    check_setup()