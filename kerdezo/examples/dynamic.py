"""This test demonstrates how to add questions dynamically and how to create
dynamic bindings to check values with validators.
"""

import random
import sys

from kerdezo import Kerdezo
from kerdezo.validators import IntegerValidators


class RandomInt:
    def __init__(self, min=1, max=100):
        self.val = random.randint(min, max)

    def __str__(self):
        unit = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine"
        ]
        teen = [
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen"
        ]
        ten = [
            "-",
            "-",
            "twenty",
            "thirty",
            "forty",
            "fifty",
            "sixty",
            "seventy",
            "eighty",
            "ninety"
        ]

        res = ""

        if 0 < self.val < 10:
            res = unit[self.val]
        elif 10 <= self.val < 20:
            res = teen[self.val - 10]
        elif 20 <= self.val < 100:
            intpart = int(self.val / 10)
            remainder = self.val - intpart * 10
            suffix = f"-{unit[remainder]}" if remainder > 0 else ""
            res = f"{ten[intpart]}{suffix}"
        else:
            res = "one hundred"
        return res

    def __int__(self):
        return self.val

    def __eq__(self, value):
        if type(value) is str:
            return value.lower().strip() == str(self)
        elif type(value) is int:
            return value == int(self)
        return False


class Operator:
    def __init__(self, op):
        self.op = op

    @classmethod
    def random(self):
        num = random.random()
        if num > 0.5:
            return self("+")
        else:
            return self("-")

    def __str__(self):
        return self.op

    def __format__(self, fmt):
        if fmt == "text":
            if self.op == "+":
                return "plus"
            elif self.op == "-":
                return "minus"
            else:
                return ""

    def __eq__(self, op):
        return self.op == op


def getHelp(num1, op, num2):
    return f"{int(num1)} {str(op)} {int(num2)}"


def checkAnswer(num1, op, num2):
    def _validator(value, question, context):
        if op == "+":
            res = int(num1) + int(num2)
        elif op == "-":
            res = int(num1) - int(num2)
        else:
            raise ValueError(f"Unknown operator: {op}")

        if res != value:
            raise ValueError(
                f"{question.title} not equals to {value}, try again"
            )
    return _validator


def failHandler(err, context):
    print(f"Fail: {err}", file=sys.stderr)


if __name__ == "__main__":
    suite = Kerdezo(
        startMessage="""Let's see how do you do with numbers.
Give you answers as numbers.""",
        endMessage="Good job!",
        failHandler=failHandler
    )

    # Add questions dynamically
    for i in range(5):
        random.seed()

        # Generate random numbers and random operator
        num1 = RandomInt()
        op = Operator.random()
        num2 = RandomInt()

        suite.addQuestion(
            f"{num1} {op:text} {num2}",
            type=int,
            help=getHelp(num1, op, num2),
            validators=[
                IntegerValidators.greaterEqual(-100),
                IntegerValidators.lessEqual(200),
                checkAnswer(num1, op, num2)
            ]
        )

    suite.ask()
