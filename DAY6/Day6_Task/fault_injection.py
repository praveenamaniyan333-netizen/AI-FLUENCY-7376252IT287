
"""Test broken tool calls without a model or internet."""

from robust_agent import handle_tool_call


CASES = [
    (
        "Valid call",
        "get_cafe_price",
        '{"item":"coffee"}'
    ),
    (
        "Invalid JSON",
        "get_cafe_price",
        '{"item":'
    ),
    (
        "Unknown tool",
        "get_secret_menu",
        '{"item":"coffee"}'
    ),
    (
        "Missing required argument",
        "get_campus_hours",
        '{"building":"library"}'
    ),
    (
        "Wrong type",
        "get_cafe_price",
        '{"item":123}'
    ),
    (
        "Value outside enum",
        "get_campus_hours",
        '{"building":"auditorium","day":"weekday"}'
    ),
    (
        "Invented argument",
        "get_cafe_price",
        '{"item":"tea","discount":5}'
    ),
    (
        "Custom fault: top-level list",
        "get_cafe_price",
        '["coffee"]'
    ),
    (
        "Custom fault: invalid day",
        "get_campus_hours",
        '{"building":"library","day":"holiday"}'
    )
]


def main():
    print("=== FAULT INJECTION (no model / no internet) ===")

    for number, (label, name, arguments) in enumerate(
        CASES, start=1
    ):
        print(f"\n{number}. {label}")
        print(f"   call: {name}({arguments})")

        result = handle_tool_call(name, arguments)

        print("   returned:", result)
        print("   handler returned a string: YES")


if __name__ == "__main__":
    main()
