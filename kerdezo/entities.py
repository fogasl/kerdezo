"""
"""

import logging

import unidecode

logger = logging.getLogger(__name__)

class Question:
    title = ""
    dest = None
    default = None
    type = str
    value = None
    echo = True
    choices = []
    validators = []
    hooks = {
        "preValidate": [],
        "postValidate": []
    }

    def __init__(self, **kwargs):
        if "title" not in kwargs:
            raise ValueError("Question title is required")
        if "dest" not in kwargs:
            logger.debug("dest is not set")
            self.dest = Question._get_dest(kwargs["title"])
        else:
            if str(kwargs["dest"]).strip() == "":
                raise ValueError("dest cannot be empty")
        self.__dict__.update(**kwargs)

    @staticmethod
    def _get_dest(title):
        return unidecode.unidecode(title)

    def __str__(self):
        if self.choices:
            pass
        return self.title

    def __format__(self, spec):
        pass
