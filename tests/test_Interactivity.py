from distutils.command.build_scripts import first_line_re
import os
import unittest

from kerdezo import (
    Kerdezo,
    Question,
    InteractiveError
)

class InteractiveTests(unittest.TestCase):
    @staticmethod
    def answerMachine():
        counter = -1
        answers = [
            "John Doe",
            "",
            "?",
            "nonesuch",
            "baz",
            "THISISTOOLONG",
            "x"
        ]

        def _input(prompt):
            nonlocal counter
            nonlocal answers
            counter += 1
            with open(os.devnull, "w") as devnull:
                print(prompt + f"(Counter: {counter})", end="", file=devnull)
            return answers[counter]

        return _input

    @staticmethod
    def answerMachineAborting():
        def _input(prompt):
            raise KeyboardInterrupt()
        return _input

    @staticmethod
    def validator(value, question, context):
        if len(value) > 3:
            raise ValueError("maximum length is 3 chars")

    @staticmethod
    def raisingFailHandler(err, context):
        raise err

    @staticmethod
    def abortHandler(context):
        pass

    def test_interactive_ask_no_questions(self):
        k = Kerdezo()

        with self.assertRaises(InteractiveError):
            k.ask()

    def test_interactive_ask_retry(self):
        k = Kerdezo(
            startMessage="Test #1",
            endMessage="Finished"
        )

        firstQuestion = Question("Your name")

        k.addQuestion(firstQuestion)
        k.addQuestion("Are you over 18?", choices=["yes", "no"], default="yes")
        k.addQuestion("There are choices", choices=["foo", "bar", "baz"])
        k.addQuestion("It is being validated", validators=[self.validator])

        with open(os.devnull, "w") as devnull:
            k.ask(inputFn=self.answerMachine(), outfile=devnull)

        self.assertEqual(k.getAnswer(firstQuestion), "John Doe")
        self.assertEqual(k.getAnswer("Are you over 18?"), "yes")
        self.assertEqual(k.getAnswer("There are choices"), "baz")
        self.assertEqual(k.getAnswer("It is being validated"), "x")

        with self.assertRaises(TypeError):
            k.getAnswer(98230324)

    def test_interactive_ask_stop(self):
        k = Kerdezo(failBehaviour="stop", failHandler=self.raisingFailHandler)

        k.addQuestion("Your age", type=int)

        with self.assertRaises(InteractiveError):
            k.ask(inputFn=self.answerMachine())

    def test_interactive_ask_continue(self):
        k = Kerdezo(failBehaviour="continue", errorMessage="There were errors")

        q = Question("Maybe float input here", type=float)

        k.addQuestion(q)

        with open(os.devnull, "w") as devnull:
            k.ask(inputFn=self.answerMachine(), outfile=devnull)

        self.assertEqual(len(k.getErrors("Maybe float input here")), 1)
        self.assertEqual(len(k.getErrors(q)), 1)

        with self.assertRaises(TypeError):
            k.getErrors(987)

    def test_interactive_ask_interrupt(self):
        k = Kerdezo(abortHandler=self.abortHandler)

        k.addQuestion("No matter what it is, should never be answered")

        k.ask(inputFn=self.answerMachineAborting())


if __name__ == "__main__":
    unittest.main()
