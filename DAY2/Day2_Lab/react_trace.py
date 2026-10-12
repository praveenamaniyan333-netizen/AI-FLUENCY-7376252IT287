"""Day 2: Print the agent's real ReAct trace."""

import sys
import os
from dotenv import load_dotenv


# Path to Day1_Lab
DAY1_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "Day1_Lab"
    )
)

# Load the .env file from Day1_Lab
load_dotenv(os.path.join(DAY1_PATH, ".env"))

# Allow Python to import Day1_Lab files
sys.path.insert(0, DAY1_PATH)


from agent import agent


QUESTION = (
    "Which is cheaper: CS101 and AI202 with a 10% scholarship, "
    "or all three courses with a 25% scholarship? By how much?"
)


print("QUESTION:", QUESTION)
print()

print("--- the agent's actions and observations ---")

answer = agent(QUESTION, max_steps=8)

print()
print("FINAL ANSWER:", answer)