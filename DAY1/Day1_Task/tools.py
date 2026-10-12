import ast
import operator as op

from config import BOOKS


# -----------------------------
# Tool 1: Get book information
# -----------------------------

def get_book_details(book_code):

    book_code = book_code.upper()

    if book_code not in BOOKS:
        return f"Book code {book_code} was not found."

    book = BOOKS[book_code]

    return (
        f"Book: {book['name']}\n"
        f"Code: {book_code}\n"
        f"Available copies: {book['copies']}\n"
        f"Fine per day: ₹{book['fine_per_day']}"
    )


# -----------------------------
# Tool 2: Safe calculator
# -----------------------------

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv
}


def safe_calculate(expression):

    try:

        tree = ast.parse(expression, mode="eval")

        def evaluate(node):

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

            if isinstance(node, ast.BinOp):

                left = evaluate(node.left)
                right = evaluate(node.right)

                operation = operators.get(type(node.op))

                if operation:
                    return operation(left, right)

            raise ValueError("Invalid expression")

        result = evaluate(tree)

        return str(result)

    except Exception:
        return "Invalid calculation."


# -----------------------------
# Tool schemas for the LLM
# -----------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_book_details",
            "description": "Get private library information for a book.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_code": {
                        "type": "string",
                        "description": "Book code such as AI202"
                    }
                },
                "required": ["book_code"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "safe_calculate",
            "description": "Perform a basic mathematical calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


TOOL_FUNCTIONS = {
    "get_book_details": get_book_details,
    "safe_calculate": safe_calculate
}


if __name__ == "__main__":

    print("Testing library tool:")
    print(get_book_details("AI202"))

    print("\nTesting calculator tool:")
    print(safe_calculate("5 * 10"))