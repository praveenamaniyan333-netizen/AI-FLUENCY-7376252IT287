
"""Validate tool arguments using the schemas in tools.py."""

from tools import SCHEMAS


def validate_arguments(tool_name, arguments):

    # Check whether the tool exists
    if tool_name not in SCHEMAS:
        return (
            f"Unknown tool '{tool_name}'. "
            f"Expected one of: {', '.join(SCHEMAS)}."
        )

    # Arguments must be a dictionary
    if not isinstance(arguments, dict):
        return (
            "Arguments must be a JSON object; "
            f"received {type(arguments).__name__}."
        )

    schema = SCHEMAS[tool_name]
    properties = schema["properties"]
    required = schema.get("required", [])

    # Check missing required arguments
    missing = [key for key in required if key not in arguments]

    if missing:
        return (
            f"Missing required argument(s): {', '.join(missing)}. "
            f"Required: {', '.join(required)}."
        )

    # Reject extra arguments
    if schema.get("additionalProperties") is False:
        extra = [key for key in arguments if key not in properties]

        if extra:
            return (
                f"Unexpected argument(s): {', '.join(extra)}. "
                f"Allowed: {', '.join(properties)}."
            )

    # Check argument types and enum values
    for key, value in arguments.items():

        if key not in properties:
            continue

        expected_type = properties[key].get("type")

        if expected_type == "string":
            valid_type = isinstance(value, str)
        elif expected_type == "integer":
            valid_type = isinstance(value, int) and not isinstance(value, bool)
        elif expected_type == "number":
            valid_type = (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
            )
        elif expected_type == "boolean":
            valid_type = isinstance(value, bool)
        elif expected_type == "object":
            valid_type = isinstance(value, dict)
        elif expected_type == "array":
            valid_type = isinstance(value, list)
        else:
            valid_type = True

        if not valid_type:
            return (
                f"Wrong type for '{key}': expected {expected_type}, "
                f"received {type(value).__name__}."
            )

        allowed_values = properties[key].get("enum")

        if allowed_values is not None and value not in allowed_values:
            return (
                f"Invalid value for '{key}': {value!r}. "
                f"Allowed values: {', '.join(map(str, allowed_values))}."
            )

    # None means the arguments are valid
    return None


def demo():
    samples = [
        (
            "get_cafe_price",
            {"item": "coffee"},
            "valid"
        ),
        (
            "get_campus_hours",
            {"building": "library"},
            "missing required argument"
        ),
        (
            "get_cafe_price",
            {"item": "tea", "discount": 5},
            "invented argument"
        ),
        (
            "get_cafe_price",
            {"item": 123},
            "wrong type"
        ),
        (
            "get_campus_hours",
            {"building": "auditorium", "day": "weekday"},
            "value outside enum"
        )
    ]

    print("=== VALIDATOR DEMO ===")

    for tool_name, arguments, label in samples:
        error = validate_arguments(tool_name, arguments)

        print(f"\n{label}: {tool_name}({arguments})")

        if error is None:
            print("  result: VALID")
        else:
            print("  result:", error)


if __name__ == "__main__":
    demo()
