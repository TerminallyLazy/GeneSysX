import inspect
import typing
from types import GenericAlias, ModuleType, UnionType
from typing import Annotated, Any, Callable

from typing_extensions import Doc


def _lenient_issubclass(cls: Any, class_or_tuple: Any) -> bool:
    """
    Adapted from pydantic._internal._utils.lenient_issubclass().
    """
    try:
        return isinstance(cls, type) and issubclass(cls, class_or_tuple)
    except TypeError:
        if isinstance(cls, (typing._GenericAlias, GenericAlias, UnionType)):
            return False
        else:
            raise

def is_annotated(ann_type: Any) -> bool:
    """
    Adapted from pydantic._internal._typing_extras.is_annotated().
    """
    origin = typing.get_origin(ann_type)
    return origin is not None and _lenient_issubclass(origin, Annotated)

def to_json_type(tp: type) -> str:
    if tp == bool:
        return 'boolean'
    elif tp == float or tp == int:
        return 'number'
    elif tp == str:
        return 'string'
    elif tp == list:
        return 'array'
    elif tp == dict:
        return 'object'
    else:
        return 'null'

def gen_function_schema(func: Callable[..., Any]) -> dict[str, Any]:
    props = {}

    for name, param in inspect.signature(func).parameters.items():
        type_hint = param.annotation
        props[name] = { "type": to_json_type(typing._strip_annotations(type_hint)) }
        if is_annotated(type_hint):
            for metadata in type_hint.__metadata__:
                if isinstance(metadata, Doc):
                    props[name]["description"] = metadata.documentation

    schema = {
        "name": func.__name__,
        "description": inspect.getdoc(func),
        "parameters": {
            "type": "object",
            "properties": props,
        }
    }

    return schema
