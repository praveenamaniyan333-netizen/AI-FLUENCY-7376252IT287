"""
Day 2:
Direct Prompting vs Chain-of-Thought

Scenario:
College Library Book Rental

Direct Prompting and Chain-of-Thought do not have access
to external tools. ReAct will use the Day 1 tools.
"""

import sys
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
# Same Library scenario used by ReAct
# ---------------------------------------------------------

QUESTIONS = [

    (
        "REASONING QUESTION",
        "AI202 costs Rs. 10 per day to borrow. "
        "If a student borrows it for 3 days, "
        "what is the total rental cost?"
    ),

    (
        "EXTERNAL INFORMATION QUESTION",
        "How much does AI202 cost per day to borrow?"
    ),

    (
        "MULTI-STEP REASONING QUESTION",
        "AI202 costs Rs. 10 per day and PY101 costs Rs. 5 per day. "
        "If a student borrows AI202 for 3 days and PY101 for 2 days, "
        "what is the total rental cost?"
    )
]


# ---------------------------------------------------------
# Direct Prompting
# ---------------------------------------------------------

def direct_prompt(question):

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question directly. "
                    "You do not have access to external tools "
                    "or the college library database. "
                    "If information required to answer the question "
                    "is not provided, do not guess it. "
                    "State that the information is unavailable. "
                    "Give a concise answer."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],

        temperature=0
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# Chain-of-Thought style
# ---------------------------------------------------------

def chain_of_thought(question):

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "Solve the question carefully step by step. "
                    "You do not have access to external tools "
                    "or the college library database. "
                    "If required information is missing, "
                    "do not invent it. "
                    "Give a concise reasoning summary and "
                    "then the final answer. "
                    "Do not reveal private hidden chain-of-thought."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],

        temperature=0
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    banner(
        "DAY 2: DIRECT PROMPTING vs CHAIN-OF-THOUGHT"
    )

    print("SCENARIO: College Library Book Rental")

    print(
        "\nDirect Prompting and Chain-of-Thought "
        "do not have access to library tools."
    )

    print("\n" + "=" * 70)

    for number, (question_type, question) in enumerate(
        QUESTIONS,
        start=1
    ):

        print(
            f"\nQUESTION {number} - {question_type}"
        )

        print(question)

        print("\n--- DIRECT PROMPTING ---")

        direct_answer = direct_prompt(question)

        print(direct_answer)

        print("\n--- CHAIN-OF-THOUGHT ---")

        cot_answer = chain_of_thought(question)

        print(cot_answer)

        print("\n" + "-" * 70)