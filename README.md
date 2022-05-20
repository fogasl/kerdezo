# Kerdezo

Ask questions interactively in console applications.

## Key features

- No dependencies
- Highly customizable (question formatting, input validation, fail behaviour etc.)

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

### Start and end messages

### Fail behaviour

When the user fails to give a formally adequate answer to a question, various
actions can take place. This program supports the following behaviours:

- `retry`: the program keeps asking the same question until it gets a formally
  correct answer. This is the default behaviour.
- `continue`: the occurring error is getting noted and the program continues
  with the next questions. At the end, all previous errors are listed. In this
  case, the returned object contains the appropriate answers only.
- `stop`: the program stops on the first occurring error.

### Error reporting
