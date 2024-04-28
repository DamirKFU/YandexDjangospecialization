from django.test import TestCase
from django.urls import reverse

import catalog.models

__all__ = []


class CheckFieldsTest(TestCase):
    def check_content_value(
        self,
        item,
        exists,
        prefetched,
        not_loaded,
    ):
        check_dict = item.__dict__

        for value in exists:
            self.assertIn(value, check_dict)

        for value in prefetched:
            self.assertIn(value, check_dict["_prefetched_objects_cache"])

        for value in not_loaded:
            self.assertNotIn(value, check_dict)


class CatalogContentTest(CheckFieldsTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category_published = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published-category",
        )
        cls.category_published.full_clean()
        cls.category_published.save()

        cls.tag_published = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый опубликованный тег",
            slug="published-tag",
        )
        cls.tag_published.full_clean()
        cls.tag_published.save()

        cls.item_published = catalog.models.Item.objects.create(
            is_published=True,
            name="Тестовый опубликованный предмет",
            text="превосходно",
            category=cls.category_published,
        )
        cls.item_published.full_clean()
        cls.item_published.save()

        cls.item_on_main = catalog.models.Item.objects.create(
            is_published=True,
            is_on_main=True,
            name="Тестовый предмет на главной странице",
            text="превосходно",
            category=cls.category_published,
        )
        cls.item_on_main.full_clean()
        cls.item_on_main.save()

        cls.item_unpublished = catalog.models.Item.objects.create(
            is_published=False,
            name="Тестовый неопубликованный предмет",
            text="превосходно",
            category=cls.category_published,
        )

        cls.item_unpublished.full_clean()
        cls.item_unpublished.save()

        cls.item_published.tags.add(cls.tag_published)
        cls.item_on_main.tags.add(cls.tag_published)
        cls.item_published.tags.add(cls.tag_published)

    def test_home_page_correct_context(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertIn("items", response.context)

    def test_item_list_page_correct_context(self):
        response = self.client.get(reverse("catalog:main"))
        self.assertIn("items", response.context)

    def test_home_count_item(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(len(response.context["items"]), 1)

    def test_item_list_count_item(self):
        response = self.client.get(reverse("catalog:main"))
        self.assertEqual(len(response.context["items"]), 2)

    def test_item_type(self):
        response = self.client.get(reverse("catalog:main"))
        items = response.context["items"]
        self.assertIsInstance(items.first(), catalog.models.Item)

    def test_filds_homepage_main(self):
        response = self.client.get(reverse("homepage:main"))
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    "name",
                    "text",
                    "category_id",
                ),
                ("tags",),
                (
                    "is_on_main",
                    "image",
                    "images",
                    "is_published",
                ),
            )

    def test_filds_catalog_main(self):
        response = self.client.get(reverse("catalog:main"))
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    "name",
                    "text",
                    "category_id",
                ),
                ("tags",),
                (
                    "is_on_main",
                    "image",
                    "images",
                    "is_published",
                ),
            )

    def test_filds_catalog_item_detail(self):
        response = self.client.get(reverse("catalog:item_detail", args=[1]))
        item = response.context["item"]
        self.check_content_value(
            item,
            (
                "name",
                "text",
                "category_id",
                "rating",
                "count_grade",
            ),
            (
                "tags",
                "images",
            ),
            (
                "is_on_main",
                "image",
                "images",
                "is_published",
            ),
        )

    def test_filds_tags_main(self):
        correct_fields = [
            "_state",
            "id",
            "name",
        ]
        response = self.client.get(reverse("homepage:main"))
        item = response.context["items"].first()
        tag = item._prefetched_objects_cache["tags"].first()
        self.assertQuerySetEqual(
            tag.__dict__,
            correct_fields,
            msg="not correct use field in main item.tags query",
        )
