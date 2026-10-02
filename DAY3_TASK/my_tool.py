"""Day 3: Single external tool for library lookup."""

LIBRARY = {
    "PY101": {
        "title": "Python Programming",
        "copies": 4,
        "available": True
    },
    "AI202": {
        "title": "Artificial Intelligence",
        "copies": 2,
        "available": True
    },
    "DB303": {
        "title": "Database Systems",
        "copies": 5,
        "available": True
    }
}


def lookup_book(book_code):
    """Look up the current library stock for a book."""

    book_code = book_code.upper()

    if book_code not in LIBRARY:
        return f"Book code {book_code} was not found in the library."

    book = LIBRARY[book_code]

    return (
        f"Book: {book['title']}\n"
        f"Code: {book_code}\n"
        f"Copies available: {book['copies']}\n"
        f"Available: {'Yes' if book['available'] else 'No'}"
    )


TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "lookup_book",
        "description": (
            "Look up the current number of available copies "
            "of a library book using its book code."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "book_code": {
                    "type": "string",
                    "description": "The library book code, such as PY101 or AI202."
                }
            },
            "required": ["book_code"]
        }
    }
}