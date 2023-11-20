import inspect
from typing import Callable, Any

def _lenient_issubclass(cls: Any, class_or_tuple: Any) -> bool:
    """
    Adapted from pydantic._internal._utils.lenient_issubclass().
    """
    try:
        return isinstance(cls, type) and issubclass(cls, class_or_tuple)
    except TypeError:
        if isinstance(cls, (typing._GenericAlias, types.GenericAlias, types.UnionType)):
            return False
        else:
            raise

def is_annotated(ann_type: Any) -> bool:
    """
    Adapted from pydantic._internal._typing_extras.is_annotated().
    """
    origin = typing.get_origin(ann_type)
    return origin is not None and _lenient_issubclass(origin, Annotated)


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
