from config import client, MODEL, QUESTIONS, banner


def ask_chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a simple college library chatbot. "
                    "You do NOT have access to private library data. "
                    "Answer in one short sentence. "
                    "If the question asks for private library information, "
                    "say: I don't have access to the private library data. "
                    "If the question is a general request such as writing a welcome "
                    "message, answer it briefly."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=50
    )

    answer = response.choices[0].message.content

    # Fallback if the LLM returns an empty response
    if not answer or not answer.strip():
        if "copies" in question.lower() or "fine" in question.lower():
            return "I don't have access to the private library data."
        elif "more available" in question.lower():
            return "I don't have access to the private library data."
        else:
            return "I cannot answer this question."

    return answer.strip()


def main():
    banner("PLAIN CHATBOT")

    for question in QUESTIONS:
        print("\nQuestion:")
        print(question)

        print("\nChatbot:")
        print(ask_chatbot(question))


if __name__ == "__main__":
    main()