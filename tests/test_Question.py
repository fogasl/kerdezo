import unittest

from kerdezo import Question

class QuestionTests(unittest.TestCase):

    def test_question_ctor_ok(self):
        q = Question("This is the question")
        self.assertIsInstance(q, Question)

    def test_question_ctor_other_than_str(self):
        with self.assertRaises(TypeError):
            Question(2313242)

    def test_question_ctor_empty_string(self):
        with self.assertRaises(ValueError):
            Question("")

    def test_question_ctor_dest_same_as_title(self):
        q = Question("My question")
        self.assertEqual(q.title, q.dest)

    def test_question_ctor_dest_empty_string(self):
        with self.assertRaises(ValueError):
            Question("My question", dest="")

    def test_question_ctor_dest_all_whitespace(self):
        with self.assertRaises(ValueError):
            Question("My question", dest="     ")

    def test_question_ctor_different_choices(self):
        choices = ["Answer 1", "Ans 2", "None of the above"]
        q = Question("My question", choices=choices)
        self.assertEqual(len(q.choices), len(choices))

    def test_question_ctor_same_choices_multiple_times(self):
        with self.assertRaises(ValueError):
            Question("My question", choices=["Yes", "Yes", "Yes"])

    def test_question_ctor_different_type_choices(self):
        with self.assertRaises(ValueError):
            Question("My question", type=int, choices=["one", 2, "three"])

    def test_question_no_choices_join(self):
        q = Question("What to do")
        chs = q.getChoices()
        self.assertEqual(chs, "")

    def test_question_choices_join(self):
        q = Question("What to eat", choices=["Peach", "Strawberry", "Melon"])
        chs = q.getChoices()
        self.assertEqual(chs, "Peach, Strawberry, Melon")

    def test_question_int_choices_join(self):
        q = Question("What's your number", type=int, choices=[3, 6, 9])
        chs = q.getChoices()
        self.assertEqual(chs, "3, 6, 9")

    def test_question_choices_invalid_default(self):
        with self.assertRaises(ValueError):
            Question("Bird is a", choices=["eagle", "duck", "goose"], default="word")

    def test_question_get_help_default(self):
        q = Question("Say my name")
        hlp = q.getHelp()
        self.assertEqual(hlp, "(No help provided)")

    def test_question_get_help_custom(self):
        q = Question("Say my name", help="As is on your ID")
        hlp = q.getHelp()
        self.assertEqual(hlp, "As is on your ID")

    def test_question_str_no_choices_no_default(self):
        q = Question("What's up")
        self.assertEqual(str(q), "What's up")

    def test_question_str_no_choices_default(self):
        q = Question("What's up", default="nothing")
        self.assertEqual(str(q), "What's up [nothing]")

    def test_question_str_no_choices_default_invalid_type(self):
        with self.assertRaises(ValueError):
            Question("What'y up", default=999)

    def test_question_str_choices_contains_default(self):
        q = Question("How do you feel", choices=["good", "mad", "sad", "happy"], default="happy")
        self.assertEqual(str(q), "How do you feel {good, mad, sad, happy} [happy]")

    def test_question_repr(self):
        q = Question("Do you want it to end?")
        self.assertEqual(repr(q), "<Question: Do you want it to end?>")


if __name__ == "__main__":
    unittest.main()
