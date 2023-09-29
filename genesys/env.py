from dotenv import load_dotenv as _load_dotenv

def load_dotenv():
    """This will load environment variables from `.env`.

    By default, it will not override any existing environment variables.

    After calling this function, you can reference the values in the `.env`
    file using `os.environ` and `os.getenv` as if they came from the actual
    environment. 

    References:
    - https://github.com/gventuri/pandas-ai/blob/main/pandasai/helpers/env.py
    """
    try:
        _load_dotenv()
    except ValueError:
        pass

def values()
    """TODO: Get a dictionary with environment variables.

    Using the `dotenv_values` function from `dotenv` will return a dictionary
    with values parsed from the `.env` file without affecting the environment.

    I have seen this pattern in Node projects, but I don't know if it is
    discouraged in Python.

    References (shameless plug):
    - https://github.com/sanman1k98/www/blob/main/src/schemas/env.ts
    - https://github.com/sanman1k98/www/blob/main/src/utils/index.ts

    Returns:
        A dictionary containing values parsed and validated from the `.env`
        file and from the environment.
    """
    pass
