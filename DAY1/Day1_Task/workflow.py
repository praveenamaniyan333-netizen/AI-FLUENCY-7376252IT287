import re

from config import BOOKS, QUESTIONS, banner


def find_book_code(question):
    question = question.upper()

    for code in BOOKS:
        if code in question:
            return code

    return None


def calculate_fine(question, book_code):
    match = re.search(r"(\d+)\s*days?", question.lower())

    if match:
        days = int(match.group(1))
        fine = days * BOOKS[book_code]["fine_per_day"]
        return fine

    return None


def workflow(question):

    question_lower = question.lower()

    # Question about availability
    if "available" in question_lower or "copies" in question_lower:

        codes = []

        for code in BOOKS:
            if code.lower() in question_lower:
                codes.append(code)

        # Compare two books
        if len(codes) >= 2:

            first = codes[0]
            second = codes[1]

            difference = (
                BOOKS[first]["copies"]
                - BOOKS[second]["copies"]
            )

            if difference > 0:
                return (
                    f"{first} has {difference} more copies "
                    f"than {second}."
                )

            elif difference < 0:
                return (
                    f"{second} has {-difference} more copies "
                    f"than {first}."
                )

            else:
                return "Both books have the same number of copies."

        # Single book
        book_code = find_book_code(question)

        if book_code:
            return (
                f"{BOOKS[book_code]['name']} ({book_code}) "
                f"has {BOOKS[book_code]['copies']} copies available."
            )

    # Question about fine
    if "fine" in question_lower:

        book_code = find_book_code(question)

        if book_code:

            fine = calculate_fine(question, book_code)

            if fine is not None:
                return (
                    f"The fine for {book_code} for the given period "
                    f"is ₹{fine}."
                )

    # Welcome message
    if "welcome" in question_lower:

        return (
            "Welcome to our college library! "
            "We are happy to have you as a new member. "
            "Please take care of the books and return them on time."
        )

    return "Sorry, I cannot handle this question."


if __name__ == "__main__":

    banner("RULE-BASED WORKFLOW")

    for question in QUESTIONS:

        print("\nQuestion:")
        print(question)

        answer = workflow(question)

        print("\nWorkflow:")
        print(answer)