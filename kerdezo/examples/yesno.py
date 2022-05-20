from kerdezo import Kerdezo

if __name__ == "__main__":
    suite = Kerdezo()

    suite.addQuestion(
        "Do you have a driving license?",
        choices=["yes", "no"]
    )

    suite.ask()
