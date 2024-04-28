from django.test import Client, override_settings, TestCase
from django.urls import reverse

from lyceum import settings

__all__ = []


class ReverseResponseMiddlewareTests(TestCase):
    def test_reverse_russian_words_defoult(self):
        contents = [
            Client().get(reverse("homepage:coffee")).content.decode()
            for _ in range(20)
        ]
        if settings.ALLOW_REVERSE:
            self.assertIn(
                "Я кинйач",
                contents,
                "'Я кинйач' not in twenty contents",
            )
            self.assertEqual(
                contents.count("Я кинйач"),
                2,
                "count 'Я кинйач' in twenty contents != 2",
            )
            content_first, content_second = list(
                filter(lambda content: content == "Я кинйач", contents),
            )
            index_first = contents.index(content_first)
            index_second_reverse = contents[-1::-1].index(content_second)
            index_second = 20 - index_second_reverse - 1
            self.assertEqual(
                index_second - index_first,
                10,
                "difference between index 'Я кинйач' != 10",
            )
        else:
            self.assertNotIn(
                "Я кинйач",
                contents,
                "'Я кинйач' in twenty contents",
            )

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = [
            Client().get(reverse("homepage:coffee")).content.decode()
            for _ in range(20)
        ]
        self.assertIn(
            "Я кинйач",
            contents,
            "'Я кинйач' not in twenty contents",
        )
        self.assertEqual(
            contents.count("Я кинйач"),
            2,
            "count 'Я кинйач' in twenty contents != 2",
        )
        content_first, content_second = list(
            filter(lambda content: content == "Я кинйач", contents),
        )
        index_first = contents.index(content_first)
        index_second_reverse = contents[-1::-1].index(content_second)
        index_second = 20 - index_second_reverse - 1
        self.assertEqual(
            index_second - index_first,
            10,
            "difference between index 'Я кинйач' != 10",
        )

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_desabled(self):
        contents = [
            Client().get(reverse("homepage:coffee")).content.decode()
            for _ in range(20)
        ]
        self.assertNotIn("Я кинйач", contents, "'Я кинйач' in twenty contents")
