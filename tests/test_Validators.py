import unittest

from kerdezo.validators import (
    StringValidators,
    IntegerValidators
)


class ValidatorTests(unittest.TestCase):
    def test_validator_string_equal_ok(self):
        fn = StringValidators.equal("fubar")

        fn("fubar")

    def test_validator_string_equal_nok(self):
        fn = StringValidators.equal("barbaz")

        with self.assertRaises(ValueError):
            fn("foobar")

    def test_validator_string_notEqual_ok(self):
        fn = StringValidators.notEqual("superman")

        fn("batman")

    def test_validator_string_notEqual_nok(self):
        fn = StringValidators.notEqual("batman")

        with self.assertRaises(ValueError):
            fn("batman")

    def test_validator_string_empty_whitespace_ok(self):
        fn = StringValidators.notEmptyOrWhitespace()
        with self.assertRaises(ValueError):
            fn("")

        with self.assertRaises(ValueError):
            fn("      ")

    def test_validator_string_not_empty_ok(self):
        fn = StringValidators.notEmptyOrWhitespace()
        fn("Foo bar")

    def test_validator_string_min_length_ok(self):
        fn = StringValidators.minimumLength(5)
        fn("Kerdezo")
        fn("Ez egy fa")

    def test_validator_string_min_length_nok(self):
        fn = StringValidators.minimumLength(5)
        with self.assertRaises(ValueError):
            fn("fo")

        with self.assertRaises(ValueError):
            fn("")

    def test_validator_string_max_length_ok(self):
        fn = StringValidators.maximumLength(5)
        fn("foo")
        fn("")

    def test_validator_string_max_length_nok(self):
        fn = StringValidators.maximumLength(5)
        with self.assertRaises(ValueError):
            fn("This is way too long for an aswer")

        with self.assertRaises(ValueError):
            fn("                     ")

    def test_validator_string_email_ok(self):
        fn = StringValidators.emailAddress()

        fn("somebody@example.com")
        fn("so.me.bo.dy@localhost.local")
        fn("w@example.co.uk")

    def test_validator_string_email_nok(self):
        fn = StringValidators.emailAddress()

        with self.assertRaises(ValueError):
            fn("")

        with self.assertRaises(ValueError):
            fn("   ")

        with self.assertRaises(ValueError):
            fn("myself@localhost")

        with self.assertRaises(ValueError):
            fn("myemailaddress.com")

    def test_validator_int_greater_ok(self):
        fn = IntegerValidators.greater(1)

        fn(6)
        fn(9)

    def test_validator_int_greater_nok(self):
        fn = IntegerValidators.greater(1)

        with self.assertRaises(ValueError):
            fn(-1)

        with self.assertRaises(ValueError):
            fn(1)

    def test_validator_int_greaterEqual_ok(self):
        fn = IntegerValidators.greaterEqual(3)

        fn(3)
        fn(4)
        fn(9999)

    def test_validator_int_greaterEqual_nok(self):
        fn = IntegerValidators.greaterEqual(3)

        with self.assertRaises(ValueError):
            fn(-87)

        with self.assertRaises(ValueError):
            fn(2)

    def test_validator_int_less_ok(self):
        fn = IntegerValidators.less(8)

        fn(3)
        fn(7)

    def test_validator_int_less_nok(self):
        fn = IntegerValidators.less(9)

        with self.assertRaises(ValueError):
            fn(19)

    def test_validator_int_lessEqual_ok(self):
        fn = IntegerValidators.lessEqual(9)

        fn(9)
        fn(1)
        fn(-9)

    def test_validator_int_lessEqual_nok(self):
        fn = IntegerValidators.lessEqual(3)

        with self.assertRaises(ValueError):
            fn(9)

    def test_validator_int_equal_ok(self):
        fn = IntegerValidators.equal(69)

        fn(69)

    def test_validator_int_equal_nok(self):
        fn = IntegerValidators.equal(135)

        with self.assertRaises(ValueError):
            fn(185)

    def test_validator_int_notEqual_ok(self):
        fn = IntegerValidators.notEqual(33)

        fn(23)
        fn(-33)

    def test_validator_int_notEqual_nok(self):
        fn = IntegerValidators.notEqual(99)

        with self.assertRaises(ValueError):
            fn(99)


if __name__ == "__main__":
    unittest.main()
