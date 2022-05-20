"""This file contains validators for most common use cases.
"""

import re

class StringValidators:
    @staticmethod
    def minimumLength(length, message="Minimum length is {length}"):
        def _validator(value, context):
            if len(value) < length:
                raise ValueError(message.format(value=value, length=length))
        return _validator

    @staticmethod
    def maximumLength(length, message="Maximum length is: {length}"):
        def _validator(value, context):
            if len(value) > length:
                raise ValueError(message.format(value=value, length=length))
        return _validator

    @staticmethod
    def notEmptyOrWhitespace(message="Empty string is not allowed"):
        def _validator(value, context):
            if value.strip() == "":
                raise ValueError(message.format(value=value))
        return _validator

    @staticmethod
    def emailAddress(message="Invalid e-mail address"):
        def _validator(value, context):
            m = re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", value)
            if not m:
                raise ValueError(message.format(value=value))
        return _validator


class IntegerValidators:
    @staticmethod
    def greater(min, message="Must be greater than {min}"):
        def _validator(value, context):
            if not (value > min):
                raise ValueError(message.format(min=min, value=value))
        return _validator

    @staticmethod
    def greaterEqual(min, message="Must be greater or equal than {min}"):
        def _validator(value, context):
            if not (value >= min):
                raise ValueError(message.format(min=min, value=value))
        return _validator

    @staticmethod
    def less(max, message="Must be less than {max}"):
        def _validator(value, context):
            if not (value < max):
                raise ValueError(message.format(max=max, value=value))
        return _validator

    @staticmethod
    def lessEqual(max, message="Must be less or equal than {max}"):
        def _validator(value, context):
            if not (value <= max):
                raise ValueError(message.format(max=max, value=value))
        return _validator
