"""
"""

import logging

from getpass import getpass

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


class InteractiveError(Exception):
    pass


class Question:
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
        # Check title
        if title.isspace():
            raise ValueError("title is invalid")

        if "dest" not in kwargs:
            logger.debug("dest is not set")
            self.dest = title
        else:
            if str(kwargs["dest"]).isspace():
                raise ValueError("dest cannot be empty string")

        # Check choice types
        typ = kwargs.get("type", str)
        for choice in kwargs.get("choices", []):
            if not isinstance(choice, typ):
                raise ValueError(
                    f"Invalid choice: {choice} (expected type: {typ.__name__})"
                )

        # Ignore title from kwargs
        if "title" in kwargs:
            del kwargs["title"]

        self.title = title
        self.__dict__.update(**kwargs)

    def getChoices(self):
        return ", ".join(self.choices)

    def getHelp(self, missing="(No help provided)"):
        return self.help if self.help != "" else missing

    def __str__(self):
        if self.choices:
            choices = " {" + self.getChoices() + "}"
        else:
            choices = ""

        if self.default:
            suggested = " [" + str(self.default) + "]"
        else:
            suggested = ""

        return f"{self.title}{choices}{suggested}"


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

    # Internals
    _questions = []
    _answers = {}
    _errors = {}

    def __init__(self, **kwargs):
        """Initialize interactive suite.

        Raises:
            ValueError: Invalid value passwd for failBehaviour
        """
        if "failBehaviour" in kwargs:
            if kwargs["failBehaviour"] not in ["retry", "continue", "stop"]:
                raise ValueError("Invalid value for failBehaviour")

        self.__dict__.update(**kwargs)

    def _addQuestion(self, question):
        # look for the same dest
        res = [q for q in self._questions if q.dest == question.dest]
        if len(res) > 0:
            raise InteractiveError(
                f"Trying to add question with the same dest twice: {question.dest}"
            )
        else:
            self._questions.append(question)

    def addQuestion(self, question, **kwargs):
        if isinstance(question, Question):
            self._addQuestion(question)
        elif isinstance(question, str):
            quest = Question(question, **kwargs)
            self._addQuestion(quest)
        else:
            raise ValueError("Invalid value passed as question")
        return self

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

    def ask(self, reset=True, inputFn=input, silentInputFn=getpass):
        if reset:
            self._answers = {}

        if len(self._questions) == 0:
            raise InteractiveError("No questions to ask.")

        if self.startMessage is not None:
            print(self.startMessage)

        try:
            for question in self._questions:
                ok = False
                while not ok:
                    try:
                        fn = inputFn if question.echo else silentInputFn
                        # TODO handle GetPassWarning
                        raw = fn(str(question) + ": ")

                        # Handle help invocation
                        if (self.helpInvoker is not None and raw == self.helpInvoker):
                            print(question.getHelp())
                            continue

                        # Check and store if question has default answer
                        if raw == "" and question.default is not None:
                            ok = self._answer(question, question.default)
                            break

                        # Convert to the appropriate type
                        if question.type is not None:
                            raw = question.type(raw)

                        # Run through validators
                        if len(question.validators) > 0:
                            for validator in question.validators:
                                validator(raw, self)
                            ok = self._answer(question, raw)
                        elif len(question.choices) > 0:
                            if raw not in question.choices:
                                raise InteractiveError(
                                    f"Choose one from the following: {question.getChoices()}"
                                )
                            else:
                                ok = self._answer(question, raw)
                        else:
                            ok = self._answer(question, raw)
                    except Exception as ex:
                        if self.failBehaviour == "stop" or self.failBehaviour == "retry":
                            if self.failBehaviour == "stop":
                                raise InteractiveError(ex)
                            else:
                                ok = self._handleFail(ex, question)

                        elif self.failBehaviour == "continue":
                            if question not in self._errors:
                                self._errors[question] = []
                            self._errors[question].append(ex)
                            ok = True

            if len(self._errors) > 0:
                if self.errorMessage is not None:
                    print(self.errorMessage)
            else:
                if self.endMessage is not None:
                    print(self.endMessage)

            return self._answers
        except (ValueError, InteractiveError) as ex:
            self._handleFail(ex, question)
        except KeyboardInterrupt:
            if callable(self.abortHandler):
                self.abortHandler(self)

    def getAnswer(self, dest):
        return self._answers[dest]

    def getError(self, question):
        if isinstance(question, Question):
            return self._errors[question] if question in self._errors else None
        elif isinstance(question, str):
            # FIXME
            pass
        else:
            # FIXME
            pass
