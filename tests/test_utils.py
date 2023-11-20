import inspect
import math
from typing import Annotated

from typing_extensions import Doc

from genesys import utils

def f(x: float, y: float) -> float:
    """A simple function without documentation in annotated metadata."""
    return x + y

def pythagoras(
    a: Annotated[float, Doc("The length of side A.")],
    b: Annotated[float, Doc("The length of side B.")],
) -> Annotated[float, Doc("The length of side C.")]:
    """Calculate the length of the hypotenuse of a right triangle."""
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2))

def test_get_function_description():
    schema = utils.gen_function_schema(pythagoras)
    assert (
        schema.get("description")
        == "Calculate the length of the hypotenuse of a right triangle."
    )


def test_get_function_name():
    schema = utils.gen_function_schema(pythagoras)
    assert schema.get("name") == "pythagoras"

def test_annotated_param():
    sign = inspect.signature(pythagoras)
    assert utils.is_annotated(sign.parameters["a"].annotation)

def test_get_param_metadata():
    schema = utils.gen_function_schema(pythagoras)
    assert schema["parameters"]["properties"]["a"]["type"] == "number"
    assert schema["parameters"]["properties"]["b"]["type"] == "number"
    assert (
        schema["parameters"]["properties"]["a"]["description"]
        == "The length of side A."
    )
    assert (
        schema["parameters"]["properties"]["b"]["description"]
        == "The length of side B."
    )

def test_get_simple_function_schema():
    schema = utils.gen_function_schema(f)
    assert schema["name"] == "f"
    assert (
        schema["description"]
        == "A simple function without documentation in annotated metadata."
    )


def test_get_simple_param_annotations():
    schema = utils.gen_function_schema(f)
    assert schema["parameters"]["properties"]["x"]["type"] == "number"
    assert schema["parameters"]["properties"]["y"]["type"] == "number"
    assert schema["parameters"]["properties"]["x"].get("description") is None
    assert schema["parameters"]["properties"]["y"].get("description") is None

