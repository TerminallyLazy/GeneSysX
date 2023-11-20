import inspect
from typing import Annotated

from typing_extensions import Doc

from genesys import utils


def pythagoras(
    a: Annotated[float, Doc("The length of side A.")],
    b: Annotated[float, Doc("The length of side B.")],
) -> Annotated[float, Doc("The length of side C.")]:
    """Calculate the length of the hypotenuse of a right triangle."""
    pass

def test_get_function_description():
    schema = utils.gen_function_schema(pythagoras)
    assert schema.get("description") == "Calculate the length of the hypotenuse of a right triangle."

def test_get_function_name():
    schema = utils.gen_function_schema(pythagoras)
    assert schema.get("name") == "pythagoras"

def test_annotated_param():
    sign = inspect.signature(pythagoras)
    assert utils.is_annotated(sign.parameters["a"].annotation)

def test_get_function_params():
    schema = utils.gen_function_schema(pythagoras)
    assert isinstance(schema.get("parameters"), dict)
    assert schema["parameters"]["properties"]["a"]["type"] == "number"
    assert schema["parameters"]["properties"]["b"]["type"] == "number"
