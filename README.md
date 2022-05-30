# Kerdezo

Ask questions interactively in console applications.

[![Python application](https://github.com/fogasl/kerdezo/actions/workflows/python-app.yml/badge.svg)](https://github.com/fogasl/kerdezo/actions/workflows/python-app.yml)

## Key features

- No dependencies
- Built-in validators for the most common use cases
- Highly customizable (input validation, fail behaviour etc.)
- Has unit tests and high code coverage

## In progress

- Load from / save to JSON
- Custom question formatting
- Multiline user input
- Recorders: classes that record information as the questionnaire progress

## Installation

    $ pip install kerdezo

## Example usage

```python
from kerdezo import Kerdezo

# Create interactive suite
suite = Kerdezo()

# Add questions
suite.addQuestion("How do you feel today?", dest="feel", default="happy")

# Start asking questions
suite.ask()

# Do something with the answers
print(f"You are feeling {suite.getAnswer('feel')}")
```

See the `kerdezo/examples` directory for more examples.

## Configuration

### Questions

A `kerdezo` suite consists of *Questions*.

Questions are asked in the order they were added to the `Kerdezo` suite.

Question can have a default value or possible values to choose from
(`choices`).

Answer on the question is stored in a dictionary, where the key field is
the one that defined in the question's `dist` property. If omitted, `dist`
become the question title itself.

`validators` contains a list of callables that validate the answer to the
question. Validators are run in the order they are defined in the list.

Validator functions must have three input args:

* `value` is the type-converted user input
* `question` is the question instance on what validation is happening
* `context` is the `Kerdezo` suite that originated the question.

Validator functions may raise `ValueError` if validation fails at some point.
Returning value is not required.

### Fail behaviour

When the user fails to give a formally adequate answer to a question, various
actions can take place. This program supports the following behaviours:

- `retry`: the program keeps asking the same question until it gets a formally
  correct answer. This is the default behaviour.
- `continue`: the occurring error is getting noted and the program continues
  with the next questions. At the end, all previous errors are listed. In this
  case, the returned object contains the appropriate answers only.
- `stop`: the program stops on the first occurring error.

## License

BSD-3-Clause.
