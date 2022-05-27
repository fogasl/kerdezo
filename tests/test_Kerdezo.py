import unittest

from kerdezo import (
    Kerdezo,
    Question,
    InteractiveError
)


class KerdezoTests(unittest.TestCase):

    def test_kerdezo_ctor_ok(self):
        k = Kerdezo()
        self.assertIsNotNone(k)

    def test_kerdezo_ctor_invalid_failBehaviour(self):
        with self.assertRaises(ValueError):
            Kerdezo(failBehaviour="keep-going")

    def test_kerdezo_add_question_str_ok(self):
        k = Kerdezo()

        k.addQuestion("What's your flava?")

    def test_kerdezo_add_question_instance_ok(self):
        k = Kerdezo()
        q = Question("Do you want to believe?")
        k.addQuestion(q)

    def test_kerdezo_add_question_invalid_type(self):
        k = Kerdezo()

        with self.assertRaises(TypeError):
            k.addQuestion(333)

    def test_kerdezo_add_questions_same_dest(self):
        k = Kerdezo()

        with self.assertRaises(InteractiveError):
            k.addQuestion("Number one", dest="one")
            k.addQuestion("Number two", dest="one")

    def test_kerdezo_add_question_default_conflict_helpInvoker(self):
        k = Kerdezo()

        with self.assertRaises(InteractiveError):
            k.addQuestion("Invalid one", default="?")

    def test_kerdezo_add_question_choice_conflict_helpInvoker(self):
        k = Kerdezo()

        with self.assertRaises(InteractiveError):
            k.addQuestion("Another invalid one", choices=["!", ".", "?"])

    def test_kerdezo_getQuestion_ok(self):
        k = Kerdezo()

        k.addQuestion("How much is the fish", dest="fish")

        questionFish = k.getQuestion("fish")

        self.assertIsInstance(questionFish, Question)
        self.assertEqual(questionFish.dest, "fish")

        q = Question("What does the fox say")

        k.addQuestion(q)

        questionFox = k.getQuestion(q)

        self.assertIsInstance(questionFox, Question)
        self.assertEqual(questionFox.dest, "What does the fox say")

    def test_kerdezo_getQuestion_nok(self):
        k = Kerdezo()

        k.addQuestion("It should NOT be answered")

        with self.assertRaises(ValueError):
            k.getQuestion("foobar")

        with self.assertRaises(TypeError):
            k.getQuestion(3.14)


if __name__ == "__main__":
    unittest.main()
