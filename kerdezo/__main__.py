"""
"""

import sys

from .errors import InteractiveError
from . import Kerdezo

# Define methods for validation
def validateFoo(val):
    pass

def validatePasswords2(val, context):
    if val != context.answers.password:
        context.setProgressTo("password")
        raise ValueError("Passwords do not match")

# Initialize suite
qs = Kerdezo(
    startMessage="This message is printed before the test.",
    endMessage="Successfully filled, congratulations.",
    errorMessage="There were errors. Check the output for details."
)

# Add questions
qs.addQuestion(
    title="First name",
    dest="fn",  # If omitted, destination name comes from Title, unaccented and camelCase
    default="John"
)

qs.addQuestion(
    title="Birth Year",
    type=int
)

qs.addQuestion(
    title="Password",
    echo=False,
    validators=[validatePasswords2]
)

qs.addQuestion(
    title="Repeat password",
    echo=False
)

qs.addQuestion(
    title="You can type anything here or simply skip this question"
)

print(qs)

# Ask for answers
try:
    qs.ask()
except InteractiveError as err:
    print(f"Error: {err}", file=sys.stderr)
