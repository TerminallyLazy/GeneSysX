from typing import Annotated
from typing_extensions import Doc
from genesys import utils

def pythagoras(
    a: Annotated[float, "The length of one of the two sides of the triangle"],
    b: Annotated[float, "THe length of the other one of the two sides of the triangle"],
) -> Annotated[float, "The length of the hypotenuse of the triangle"]:
    """Calculate the length of the hypotenuse of a triangle."""
    pass

def test_get_function_description():
    schema = utils.gen_function_schema(pythagoras)
    assert schema.get("description") == "Calculate the length of the hypotenuse of a triangle."

def test_get_function_name():
    schema = utils.gen_function_schema(pythagoras)
    assert schema.get("name") == "pythagoras"
