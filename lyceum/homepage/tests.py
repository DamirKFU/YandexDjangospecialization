from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.urls import reverse

__all__ = []


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        status_code = Client().get(reverse("homepage:main")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        status_code = Client().get(reverse("homepage:coffee")).status_code
        self.assertEqual(status_code, HTTPStatus.IM_A_TEAPOT)

    @override_settings(ALLOW_REVERSE=False)
    def test_coffee_endpoint_content(self):
        response = Client().get(reverse("homepage:coffee"))
        self.assertEqual(response.content.decode(), "Я чайник")
