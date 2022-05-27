"""This file contains validators for most common use cases.
"""

import re

class StringValidators:
    @staticmethod
    def equal(value, message="Must equal to {expected}"):
        def _validator(expected, question=None, context=None):
            if value != expected:
                raise ValueError(message.format(value=value, expected=expected))
        return _validator

    @staticmethod
    def notEqual(value, message="Must not equal to {notExpected}"):
        def _validator(notExpected, question=None, context=None):
            if value == notExpected:
                raise ValueError(message.format(value=value, notExpected=notExpected))
        return _validator

    @staticmethod
    def minimumLength(length, message="Minimum length is {length}"):
        def _validator(value, question=None, context=None):
            if len(value) < length:
                raise ValueError(message.format(value=value, length=length))
        return _validator

    @staticmethod
    def maximumLength(length, message="Maximum length is: {length}"):
        def _validator(value, question=None, context=None):
            if len(value) > length:
                raise ValueError(message.format(value=value, length=length))
        return _validator

    @staticmethod
    def notEmptyOrWhitespace(message="Empty string is not allowed"):
        def _validator(value, question=None, context=None):
            if value.strip() == "":
                raise ValueError(message.format(value=value))
        return _validator

    @staticmethod
    def emailAddress(message="Invalid e-mail address: {value}"):
        def _validator(value, question=None, context=None):
            m = re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,9})+$", value)
            if not m:
                raise ValueError(message.format(value=value))
        return _validator


class IntegerValidators:
    @staticmethod
    def equal(value, message="Must equal to {expected}"):
        def _validator(expected, question=None, context=None):
            if value != expected:
                raise ValueError(message.format(value=value, expected=expected))
        return _validator

    @staticmethod
    def notEqual(value, message="Must not equal to {notExpected}"):
        def _validator(notExpected, question=None, context=None):
            if value == notExpected:
                raise ValueError(message.format(value=value, notExpected=notExpected))
        return _validator

    @staticmethod
    def greater(min, message="Must be greater than {min}"):
        def _validator(value, question=None, context=None):
            if not (value > min):
                raise ValueError(message.format(value=value, min=min))
        return _validator

    @staticmethod
    def greaterEqual(min, message="Must be greater or equal than {min}"):
        def _validator(value, question=None, context=None):
            if not (value >= min):
                raise ValueError(message.format(value=value, min=min))
        return _validator

    @staticmethod
    def less(max, message="Must be less than {max}"):
        def _validator(value, question=None, context=None):
            if not (value < max):
                raise ValueError(message.format(value=value, max=max))
        return _validator

    @staticmethod
    def lessEqual(max, message="Must be less or equal than {max}"):
        def _validator(value, question=None, context=None):
            if not (value <= max):
                raise ValueError(message.format(max=max, value=value))
        return _validator
