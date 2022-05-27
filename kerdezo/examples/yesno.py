from kerdezo import Kerdezo, Question

class YesNoQuestion(Question):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.validators.insert(0, self.validator)

    @staticmethod
    def validator(value, question, context):
        pass

if __name__ == "__main__":
    suite = Kerdezo()

    suite.addQuestion(
        "Do you have a driving license?",
        choices=["yes", "no"],
        default="yes",
        validators=[]
    )

    suite.ask()

    if suite.getAnswer("Do you have a driving license?") is True:
        print("Congrats! Safe driving!")
