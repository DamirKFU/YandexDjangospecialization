__all__ = []

from django.test import Client, override_settings, RequestFactory, TestCase
import django.urls

import catalog.models
import catalog.views
import statistic.views
import users.models


@override_settings(DEFAULT_USER_IS_ACTIVE=True, ALLOW_REVERSE=False)
class StatisticTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published-category",
        )
        cls.category.full_clean()
        cls.category.save()

        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый опубликованный тег",
            slug="published-tag",
        )
        cls.tag.full_clean()
        cls.tag.save()

        cls.item = catalog.models.Item.objects.create(
            is_published=True,
            name="Тестовый опубликованный предмет",
            text="превосходно",
            category=cls.category,
        )
        cls.item2 = catalog.models.Item.objects.create(
            is_published=True,
            name="Тестовый опубликованный предмет 2",
            text="превосходно 2",
            category=cls.category,
        )
        cls.item.full_clean()
        cls.item.save()
        cls.item2.full_clean()
        cls.item2.save()

        cls.item.tags.add(cls.tag)
        cls.item2.tags.add(cls.tag)

    def setUp(self):
        self.factory = RequestFactory()

        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        self.user1 = users.models.User.objects.create_user(**data)

    def test_statistic_by_user_context(self):
        request = self.factory.get(
            django.urls.reverse("statistic:by-user"),
        )
        request.user = self.user1
        response = statistic.views.StatisticByUserTemplateView.as_view()(
            request,
        )

        self.assertIn("query", response.context_data)
        self.assertIn("items", response.context_data)

    def test_statistic_graded_items_context(self):
        request = self.factory.get(
            django.urls.reverse("statistic:graded-items"),
        )
        request.user = self.user1
        response = statistic.views.StatisticGradedItemsListView.as_view()(
            request,
        )

        self.assertIn("grades", response.context_data)

    def test_statistic_by_items_context(self):
        request = self.factory.get(
            django.urls.reverse("statistic:by-items"),
        )
        request.user = self.user1
        response = statistic.views.StatisticByItemsListView.as_view()(request)

        self.assertIn("items", response.context_data)
