import re

from django.core.exceptions import ValidationError
import django.utils.deconstruct

__all__ = []


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self.words = words
        self.pattern = "|".join(f"\\b{word}\\b" for word in words)

    def __call__(self, value):
        if re.findall(self.pattern, value, re.IGNORECASE):
            return

        str_words = " ".join(self.words)
        raise ValidationError(
            f"должно содержаться одно из слов: {str_words}",
        )
