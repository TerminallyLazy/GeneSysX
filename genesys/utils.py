import inspect
from typing import Callable, Any


def gen_function_schema(function: Callable[..., Any]) -> dict[str, Any]:
    schema = {
        "name": function.__name__,
        "description": inspect.getdoc(function),
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }
    return schema
