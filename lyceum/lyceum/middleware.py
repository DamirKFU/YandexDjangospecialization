import re

from django.conf import settings

__all__ = []


class ReverseResponseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def reverse_russian_words(content):
        pattern = re.compile(
            r"\b[а-яё]+\b",
            re.IGNORECASE,
        )
        text = content
        for m in re.finditer(string=text, pattern=pattern):
            s = m.start()
            e = m.end()
            text = text[:s] + text[s:e][::-1] + text[e:]

        return text

    def __call__(self, request):
        response = self.get_response(request)
        if ReverseResponseMiddleware.count == 9:
            if settings.ALLOW_REVERSE:
                content = response.content.decode("utf-8")
                response.content = self.reverse_russian_words(content).encode(
                    "utf-8",
                )

            ReverseResponseMiddleware.count = 0
            return response

        ReverseResponseMiddleware.count += 1
        return response
