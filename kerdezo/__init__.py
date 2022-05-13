"""
"""

import logging

from getpass import getpass

from .entities import Question
from .errors import InteractiveError

logger = logging.getLogger(__name__)

__version__ = "0.1.0"

class Kerdezo:
    startMessage = ""
    endMessage = ""
    errorMessage = ""
    failBehaviour = "retry" # or "continue" or "stop"
    abortHandler = None
    _questions = []
    _answers = {}

    def __init__(self, *args, **kwargs):
        self._questions= []
        if "failBehaviour" in kwargs:
            if kwargs["failBehaviour"] not in ["retry", "continue", "stop"]:
                raise ValueError("Invalid value for failBehaviour")
        self.__dict__.update(**kwargs)

    # TODO: param1 can be Question or str. Use *args and check type
    def addQuestion(self, question=None, **kwargs):
        if isinstance(question, Question):
            self._questions.append(question)
        else:
            quest = Question(**kwargs)
            self._questions.append(quest)
        return self

    def ask(self):
        if len(self._questions) == 0:
            raise InteractiveError("No questions to ask.")

        if self.startMessage is not None:
            print(self.startMessage)

        try:
            for question in self._questions:
                fn = input if question.echo else getpass
                # TODO handle GetPassWarning
                raw = fn(str(question) + ": ")

            if self.endMessage is not None:
                print(self.endMessage)

            return self._answers
        except KeyboardInterrupt:
            if callable(self.abortHandler):
                self.abortHandler(self)
