# Developing

## [Google Python style guide](https://google.github.io/styleguide/pyguide.html)

A list of "dos and don'ts" for Python programs with explanations. Pretty solid advice imo.

## Package manager

To run this project, you need to use the [Poetry package manager](https://python-poetry.org/docs/).

> [!WARNING]
> Please install Poetry using one of the [recommended methods](https://python-poetry.org/docs/#installation). Running `brew install poetry` is easier but will inevitably lead to a myriad of problems with virtualenvs, Python versions, dependency resolution, and just add fuel to the dumpster fire that is Python package management.

### Installing dependencies

Run this command when you first clone the project.

```sh
poetry install
```

### Adding dependencies

If you need to add dependency, the following command will install the package and update the `tool.poetry.dependencies` section in the `pyproject.toml`.

```sh
poetry add <package-name>
```

### Poetry documentation

- [Basic usage](https://python-poetry.org/docs/basic-usage/)
- [Managing dependencies](https://python-poetry.org/docs/managing-dependencies/)
- [Commands](https://python-poetry.org/docs/cli/)
- [The `pyproject.toml` file](https://python-poetry.org/docs/pyproject/)

## Testing

This project uses pytest to test the code. To run the entire test suite, run the following command

```sh
poetry run pytest
```

### Specifying tests

Use the `--collect-only` or `--co` flag to list out all the tests that can be executed.

```sh
poetry run pytest --co
```

[Pytest supports multiple ways](https://docs.pytest.org/en/7.4.x/how-to/usage.html#specifying-which-tests-to-run) to specify which tests to run, here are a few examples.

```sh
# run tests in a module
poetry run pytest tests/test_toolkit.py
# run a specific test
poetry run pytest tests/test_toolkit.py::test_multiple_sequence_alignment
```

### Using `print()` statements in tests

By default, pytest will capture any output sent to `stdout` and `stderr` during test execution. But if a test fails, then its captured output will be shown along with its traceback.

To disable all capturing you can use the `-s` flag, which is a shortcut for `--capture=no`.

```sh
# run tests with print() output shown
poetry run pytest -s
```

### Pytest documentation

- [Get started](https://docs.pytest.org/en/7.4.x/getting-started.html#create-your-first-test)
- [How to invoke pytest](https://docs.pytest.org/en/7.4.x/how-to/usage.html)
- [About fixtures](https://docs.pytest.org/en/7.4.x/explanation/fixtures.html)
- [API reference](https://docs.pytest.org/en/7.4.x/reference/reference.html)

## Running locally

Create a `.env` file containing varibles required to run the application (e.g., your OpenAI API key).

TODO: point to the environment variable validation logic instead of enumerating the required variables here.

```sh
# ik it says run twice
poetry run streamlit run app.py
```
