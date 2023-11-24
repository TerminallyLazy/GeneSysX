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
    required = []

    # get information about each param
    for name, param in inspect.signature(func).parameters.items():
        props[name] = {}

        if param.default is not param.empty:
            # add default value information
            props[name]["default"] = param.default
        else:
            # params without default values are considered "required"
            required.append(name)

        type_hint = param.annotation
        props[name]["type"] = to_json_type(typing._strip_annotations(type_hint))

        if is_annotated(type_hint):
            for metadata in type_hint.__metadata__:
                if isinstance(metadata, Doc):
                    props[name]["description"] = metadata.documentation

    schema = {
        "name": func.__name__,
        "parameters": {
            "type": "object",
            "properties": props,
        }
    }

    if (desc := inspect.getdoc(func)) is not None:
        schema["description"] = desc

    if len(required) > 0:
        schema["parameters"]["required"] = required

    return schema

def gen_tools_schema(mod: ModuleType) -> list[dict]:
    tools = []

    for name, fn in inspect.getmembers(mod):
        if (
            not name.startswith("_")
            and inspect.isfunction(fn)
            and fn.__module__ == mod.__name__
        ):
            tools.append({
                "type": "function",
                "function": gen_function_schema(fn)
            })

    return tools
