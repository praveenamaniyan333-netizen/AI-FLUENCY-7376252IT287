"""
Day 2:
Self-Consistency Experiment

Scenario:
College Library Book Rental

The same reasoning question is run 5 times
with a non-zero temperature.

The majority answer is identified and compared
with a temperature = 0 run.
"""

import re
import sys
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------
# Import config.py from Day1_Practice
# ---------------------------------------------------------

DAY1_PATH = (
    Path(__file__).resolve().parent.parent
    / "Day1_Practice"
)

sys.path.insert(0, str(DAY1_PATH))

from config import client, MODEL, banner


# ---------------------------------------------------------
# Library reasoning question
# ---------------------------------------------------------

QUESTION = (
    "AI202 costs Rs. 10 per day to borrow. "
    "If a student borrows it for 3 days, "
    "what is the total rental cost?"
)

CORRECT_ANSWER = 30


# ---------------------------------------------------------
# Ask model
# ---------------------------------------------------------

def ask_model(temperature):

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "Solve the arithmetic problem carefully. "
                    "Give a concise reasoning summary followed "
                    "by the final answer. "
                    "Do not reveal private hidden chain-of-thought."
                )
            },
            {
                "role": "user",
                "content": QUESTION
            }
        ],

        temperature=temperature
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# Extract final amount
# ---------------------------------------------------------

def extract_amount(text):

    # First look for Rs. / ₹ amounts

    matches = re.findall(
        r"(?:Rs\.?|₹)\s*([0-9,]+)",
        text,
        flags=re.IGNORECASE
    )

    if matches:

        return int(
            matches[-1].replace(",", "")
        )

    # Backup for a plain answer such as "30"

    plain_numbers = re.findall(
        r"\b\d{1,6}\b",
        text
    )

    if plain_numbers:

        return int(plain_numbers[-1])

    return None


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    banner("DAY 2: SELF-CONSISTENCY")

    print("SCENARIO: College Library Book Rental")

    print("\nQUESTION:")
    print(QUESTION)

    print("\nCorrect answer: Rs. 30")

    # -----------------------------------------------------
    # Five non-zero-temperature runs
    # -----------------------------------------------------

    TEMPERATURE = 0.7

    print("\n" + "=" * 70)

    print(
        "Running the question 5 times "
        f"with temperature = {TEMPERATURE}"
    )

    print("=" * 70)

    answers = []

    for run in range(1, 6):

        result = ask_model(TEMPERATURE)

        extracted = extract_amount(result)

        answers.append(extracted)

        print(f"\nRUN {run}")

        print(result)

        if extracted is not None:

            print(
                f"Extracted final amount: "
                f"Rs. {extracted:,}"
            )

        else:

            print(
                "Extracted final amount: "
                "Could not identify"
            )

    # -----------------------------------------------------
    # Majority answer
    # -----------------------------------------------------

    valid_answers = [
        answer
        for answer in answers
        if answer is not None
    ]

    print("\n" + "=" * 70)

    print("SELF-CONSISTENCY SUMMARY")

    print("=" * 70)

    print(
        "Recorded answers:",
        answers
    )

    if valid_answers:

        counts = Counter(valid_answers)

        majority_answer, frequency = (
            counts.most_common(1)[0]
        )

        print(
            f"Majority answer: "
            f"Rs. {majority_answer:,}"
        )

        print(
            "Majority frequency:",
            frequency
        )

        print(
            "Majority answer correct:",
            majority_answer == CORRECT_ANSWER
        )

    else:

        majority_answer = None

        print(
            "Majority answer: "
            "Could not determine"
        )

    # -----------------------------------------------------
    # Temperature = 0
    # -----------------------------------------------------

    print("\n" + "=" * 70)

    print("TEMPERATURE = 0")

    print("=" * 70)

    zero_result = ask_model(0)

    zero_answer = extract_amount(zero_result)

    print("\nResponse:")

    print(zero_result)

    if zero_answer is not None:

        print(
            f"\nExtracted final amount: "
            f"Rs. {zero_answer:,}"
        )

        print(
            "Temperature-0 answer correct:",
            zero_answer == CORRECT_ANSWER
        )

    else:

        print(
            "\nCould not extract final amount."
        )