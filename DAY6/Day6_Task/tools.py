
"""Tools and schemas for a college campus assistant."""

SCHEMAS = {
    "get_cafe_price": {
        "type": "object",
        "properties": {
            "item": {
                "type": "string",
                "enum": ["coffee", "tea", "sandwich", "juice"],
                "description": "Cafeteria menu item"
            }
        },
        "required": ["item"],
        "additionalProperties": False
    },

    "get_campus_hours": {
        "type": "object",
        "properties": {
            "building": {
                "type": "string",
                "enum": ["library", "gym", "computer_lab"]
            },
            "day": {
                "type": "string",
                "enum": ["weekday", "saturday", "sunday"]
            }
        },
        "required": ["building", "day"],
        "additionalProperties": False
    }
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_cafe_price",
            "description": "Look up the price of a cafeteria menu item.",
            "parameters": SCHEMAS["get_cafe_price"],
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_campus_hours",
            "description": "Look up campus building hours for a day type.",
            "parameters": SCHEMAS["get_campus_hours"],
            "strict": True
        }
    }
]

# Demonstration data
PRICES = {
    "coffee": 25,
    "tea": 15,
    "sandwich": 60,
    "juice": 35
}

HOURS = {
    ("library", "weekday"): "08:00-20:00",
    ("library", "saturday"): "09:00-16:00",
    ("library", "sunday"): "Closed",

    ("gym", "weekday"): "06:00-20:00",
    ("gym", "saturday"): "07:00-12:00",
    ("gym", "sunday"): "Closed",

    ("computer_lab", "weekday"): "09:00-17:00",
    ("computer_lab", "saturday"): "09:00-13:00",
    ("computer_lab", "sunday"): "Closed"
}


def get_cafe_price(item):
    return {
        "item": item,
        "price_rupees": PRICES[item]
    }


def get_campus_hours(building, day):
    return {
        "building": building,
        "day": day,
        "hours": HOURS[(building, day)]
    }


FUNCTIONS = {
    "get_cafe_price": get_cafe_price,
    "get_campus_hours": get_campus_hours
}
