"""*Kerdezo*: ask questions interactively in console applications.
"""

import logging

from getpass import getpass
import sys

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


class InteractiveError(Exception):
    pass


class Question:
    """Entity that represents a particular question in the interactive suite
    that must be answered.
    Question can have a default value or possible values to choose from
    (`choices`).
    `validators` contains a list of callables that validate the answer to the
    question. Validators are run in the order they are defined in the list.
    Validator functions must have two input args:
    * `value` is the type-converted user input
    * `context` is the `Kerdezo` suite that originated the question.
    Validator functions may raise `ValueError` if validation fails on some
    point. Returning value is not required.
    """

    # Title of the question
    title = ""
    # Key name in the result array in which the answer is stored for this question
    dest = None
    # Default answer for the question
    default = None
    # Expected type of the answer
    type = str
    # Whether the answer should echo or not. Disable on password prompt or sensitive data
    echo = True
    # Possible answers for the question
    choices = []
    # Functions that validate the answer
    validators = []
    # Help message for the question
    help = ""

    def __init__(self, title="", **kwargs):
        """Initialize a new instance of the `Question` class.

        Args:
            title (str, optional): Title of the question. Defaults to "".

        Raises:
            ValueError: `title` is invalid
            ValueError: `dest` cannot be empty string
            ValueError: Trying to add the same choice multiple times
            ValueError: Default value not included in choices
            ValueError: Invalid type of default value
            ValueError: Invalid type of choice
        """
        # Check title
        if len(title) == 0 or title.isspace():
            raise ValueError("'title' is invalid")

        dest = kwargs.get("dest", title)

        if dest is not None and (len(dest) == 0 or dest.isspace()):
            raise ValueError("'dest' cannot be empty string")
        else:
            self.dest = dest

        # Check choice types
        typ = kwargs.get("type", str)
        choices = kwargs.get("choices", [])

        # Find duplicate choices
        if len({i: choices.count(i) for i in choices}.values()) != len(choices):
            raise ValueError("Trying to add the same choice multiple times")

        # If choices and default value is provided, choices should include default
        defaultValue = kwargs.get("default", None)
        if defaultValue is not None and len(choices) > 0 and defaultValue not in choices:
            raise ValueError("Default value not included in 'choices'")

        if defaultValue is not None and type(defaultValue) != typ:
            raise ValueError(
                f"Invalid type of 'default' (expected: {typ.__name__})"
            )

        for choice in choices:
            if not isinstance(choice, typ):
                raise ValueError(
                    f"Invalid type of choice: {choice} (expected: {typ.__name__})"
                )

        self.title = title
        self.type = typ
        self.__dict__.update(**kwargs)

    def getChoices(self):
        """Returns the possible values ('choices') of the question as a
        comma-separated string.

        Returns:
            str: 'choices' as string
        """
        return ", ".join([str(item) for item in self.choices])

    def getHelp(self, missing="(No help provided)"):
        """Returns the help of a question, or `missing` if help is not defined.

        Args:
            missing (str, optional): Substitute text if help is not defined.
            Defaults to "(No help provided)".

        Returns:
            str: help message
        """
        return self.help if self.help != "" else missing

    def __str__(self):
        """Returns a string that represents the current object.

        Returns:
            str: question as a string
        """
        if self.choices:
            choices = " {" + self.getChoices() + "}"
        else:
            choices = ""

        if self.default:
            suggested = " [" + str(self.default) + "]"
        else:
            suggested = ""

        return f"{self.title}{choices}{suggested}"

    def __repr__(self):
        """Returns printable representation of the current object.

        Returns:
            str: string representation of the question
        """
        return f"<Question: {self.title}>"


class Kerdezo:
    # Message to print before asking questions
    startMessage = None
    # Message to print after the last question has been answered
    endMessage = None
    # Message to print if errors occurred and failBehaviour is not "retry"
    errorMessage = None
    # What to do if an answer fails on type conversion or validation
    failBehaviour = "retry" # or "continue" or "stop"
    # Method to handle type conversion or validation errors
    failHandler = None
    # Method to handle test abortion (e.g. Ctrl+C on console)
    abortHandler = None
    # Special kind of answer that shows help message on a particular question
    helpInvoker = "?"

    def __init__(self, **kwargs):
        """Initialize the interactive suite.

        Raises:
            ValueError: Invalid value passed for failBehaviour
        """
        if "failBehaviour" in kwargs:
            if kwargs["failBehaviour"] not in ["retry", "continue", "stop"]:
                raise ValueError("Invalid value for 'failBehaviour'")

        self.__dict__.update(**kwargs)

        self._questions = []
        self._answers = {}
        self._errors = {}

    def _addQuestion(self, question):
        # look for the same dest
        res = [q for q in self._questions if q.dest == question.dest]
        if len(res) > 0:
            raise InteractiveError(
                f"Trying to add question with the same 'dest' twice: {question.dest}"
            )

        if self.helpInvoker is not None and (self.helpInvoker == \
            question.default or self.helpInvoker in question.choices):
            raise InteractiveError(
                f"'default' or 'choices' conflicts with 'helpInvoker'"
            )

        self._questions.append(question)

    def _answer(self, question, value):
        """Store answer on a particular question.

        Args:
            question (Question): Question instance
            value (any): Answer to the question

        Returns:
            bool: True
        """
        if question.dest is not None:
            self._answers[question.dest] = value
        return True

    def _handleFail(self, err, question):
        if callable(self.failHandler):
            self.failHandler(err, self)
        return False

    def addQuestion(self, question, **kwargs):
        if isinstance(question, Question):
            self._addQuestion(question)
        elif isinstance(question, str):
            quest = Question(question, **kwargs)
            self._addQuestion(quest)
        else:
            raise ValueError("Invalid value for 'question' (expected 'str' or 'Question')")
        return self

    def ask(self, **kwargs):
        reset = kwargs.get("reset", True)
        inputFn = kwargs.get("inputFn", input)
        silentInputFn = kwargs.get("silentInputFn", getpass)
        outfile = kwargs.get("outfile", sys.stdout)

        if reset:
            self._answers = {}

        if len(self._questions) == 0:
            raise InteractiveError("No questions to ask")

        if self.startMessage is not None:
            print(self.startMessage, file=outfile)

        try:
            for question in self._questions:
                ok = False
                while not ok:
                    try:
                        fn = inputFn if question.echo else silentInputFn
                        # TODO handle GetPassWarning
                        # TODO custom question formatting?
                        raw = fn(str(question) + ": ")

                        # Handle help invocation
                        if (self.helpInvoker is not None and raw == self.helpInvoker):
                            print(question.getHelp(), file=outfile)
                            continue

                        # Check and store if question has default answer
                        if raw == "" and question.default is not None:
                            ok = self._answer(question, question.default)
                            break

                        # Convert to the appropriate type
                        if question.type is not None:
                            raw = question.type(raw)

                        # Run through validators
                        if len(question.choices) > 0:
                            if raw not in question.choices:
                                raise InteractiveError(
                                    f"Choose one from the following: {question.getChoices()}"
                                )
                            else:
                                ok = self._answer(question, raw)

                        if len(question.validators) > 0:
                            for validator in question.validators:
                                validator(raw, question, self)
                            ok = self._answer(question, raw)
                        else:
                            ok = self._answer(question, raw)
                    except Exception as ex:
                        if self.failBehaviour == "stop":
                            raise InteractiveError(ex)
                        elif self.failBehaviour == "retry":
                            ok = self._handleFail(ex, question)
                        elif self.failBehaviour == "continue":
                            if question.dest not in self._errors:
                                self._errors[question.dest] = []
                            self._errors[question.dest].append(ex)
                            ok = True

            if len(self._errors) > 0:
                if self.errorMessage is not None:
                    print(self.errorMessage, file=outfile)
            else:
                if self.endMessage is not None:
                    print(self.endMessage, file=outfile)

            return self._answers
        except (ValueError, InteractiveError) as ex:
            self._handleFail(ex, question)
        except KeyboardInterrupt:
            if callable(self.abortHandler):
                self.abortHandler(self)

    def getQuestion(self, question):
        if isinstance(question, Question):
            filtered = [q for q in self._questions if q == question]
        elif isinstance(question, str):
            filtered = [q for q in self._questions if q.dest == question]
        else:
            raise TypeError(
                "Invalid type for 'question' (expected 'Question' or 'str')"
            )

        if len(filtered) != 1:
            raise ValueError(f"Question not found: {question}")

        return filtered[0]

    def getAnswer(self, question):
        res = None

        if isinstance(question, Question):
            res = self._answers[question.dest]
        elif isinstance(question, str):
            res = self._answers[question]
        else:
            raise TypeError(
                "Invalid type for 'question' (expected 'Question' or 'str')"
            )

        return res

    def getErrors(self, question):
        res = None

        if isinstance(question, Question):
            if question.dest in self._errors:
                res = self._errors[question.dest]
        elif isinstance(question, str):
            if question in self._errors:
                res = self._errors[question]
        else:
            raise TypeError(
                "Invalid type for 'question' (expected 'Question' or 'str')"
            )

        return res
