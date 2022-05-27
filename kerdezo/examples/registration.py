import sys

from datetime import datetime

from kerdezo import Kerdezo
from kerdezo.validators import StringValidators


def abortHandler(ctx):
    """Handle questionnaire abortion.

    Args:
        ctx (Kerdezo): Context
    """
    total = len(ctx._questions)
    answered = len(ctx._answers)
    print()
    print(
        f"Registration aborted. Total questions: {total}, answered: {answered}"
    )


def failHandler(ex, ctx):
    """Handle failed answers.

    Args:
        ex (Exception): Exception raised on failed answering
        ctx (Kerdezo): Context
    """
    print(f"Error: {ex}", file=sys.stderr)


# Define methods for validation
def validateBirthYear(value, question, context):
    """Validate the Birth Year question.
    Values lower than 1900 or greater that the current year treated as invalid.

    Args:
        value (int): Birth year input
        context (Kerdezo): Context

    Raises:
        ValueError: The given year is invalid as birth year.
    """
    lo = 1900
    hi = datetime.now().year
    if value < lo or value > hi:
        raise ValueError(
            f"Must enter something between {lo} and {hi}"
        )


def validateRepeatPassword(value, question, context):
    """Validate the 'Repeat password' question.
    This function checks equality with the answer for the 'Password' question.

    Args:
        value (str): Repeat password input
        context (Kerdezo): Context

    Raises:
        ValueError: Passwords does not match.
    """
    if value != context.getAnswer("Password"):
        raise ValueError(
            "Passwords do not match"
        )


def tosValidator(value, question, context):
    """Validate the 'Terms of Service' question.

    Args:
        value (str): Answer to the 'Terms of Service' question
        context (Kerdezo): Context

    Raises:
        ValueError: If the answer is not 'yes'
    """
    if value != "yes":
        raise ValueError(
            "You must accept the Terms of Service to finish registration"
        )


if __name__ == "__main__":
    suite = Kerdezo(
        startMessage="""This form mimicks a registration process.
Note that no data is collected nor stored anywhere, it is for demonstrational
purposes only.
To get help on a question, type '?' (without apostrophes)
""",
        endMessage="Registration completed.",
        abortHandler=abortHandler,
        failHandler=failHandler
    )


    # Add questions
    suite.addQuestion(
        "First name",
        help="Your first name as written on your ID",
        validators=[
            StringValidators.notEmptyOrWhitespace(
                "You must type your name"
            )
        ]
    )

    suite.addQuestion(
        "Last name",
        help="Your last name or names",
        validators=[
            StringValidators.notEmptyOrWhitespace()
        ]
    )

    suite.addQuestion(
        "Birth Year",
        type=int,
        validators=[validateBirthYear]
    )

    suite.addQuestion(
        "Sex",
        choices=["male", "female"]
    )

    suite.addQuestion(
        "E-mail address",
        validators=[
            StringValidators.emailAddress()
        ]
    )

    suite.addQuestion(
        "Password",
        help="Type your password. Minimum 3, maximum 10 characters.",
        validators=[
            StringValidators.minimumLength(
                3,
                "Password length must be greater than {length} characters"
            ),
            StringValidators.maximumLength(
                10,
                "This password is too long, choose another"
            )
        ],
        echo=False  # Do not show password when typing
    )

    suite.addQuestion(
        "Repeat password",
        echo=False,
        dest=None,  # Do not store in the output
        validators=[
            validateRepeatPassword # Validate against first typed password
        ]
    )

    suite.addQuestion(
        "Do you agree with our Terms of Service?",
        choices=["yes", "no"],
        validators=[tosValidator]
    )

    # Start asking questions
    suite.ask()

    # Print answers at the end (if any)
    if suite._answers:
        print()
        print("Your answers were the following:")
        for question, answer in suite._answers.items():
            # Hide password for security
            if question == "Password":
                answer = "(hidden)"
            print(f"{question}\t{answer}")
