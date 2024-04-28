from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class StaticURLTests(TestCase):
    def test_catalog_items_endpoint(self):
        status_code = Client().get(reverse("catalog:main")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_friday_endpoint(self):
        status_code = Client().get(reverse("catalog:friday")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_new_endpoint(self):
        status_code = Client().get(reverse("catalog:new")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_catalog_unverified_endpoint(self):
        status_code = Client().get(reverse("catalog:unverified")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)
