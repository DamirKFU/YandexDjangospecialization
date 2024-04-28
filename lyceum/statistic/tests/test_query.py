__all__ = []

from django.db.models import Avg
from django.test import Client, override_settings, RequestFactory, TestCase
import django.urls

import catalog.models
import catalog.views
import rating.models
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

        data2 = {
            "username": "testinguser2",
            "email": "testuser2@example.com",
            "password": "testpassword2",
        }
        self.user2 = users.models.User.objects.create_user(**data2)

    def test_statistic_by_user(self):

        request = self.factory.post(
            django.urls.reverse(
                "catalog:item_detail",
                kwargs={"pk": self.item.id},
            ),
            {
                "grade": 1,
            },
        )
        request.user = self.user1
        catalog.views.ItemDetailView.as_view()(request, pk=self.item.id)

        request = self.factory.post(
            django.urls.reverse("catalog:item_detail", args=[self.item2.id]),
            {
                "grade": 5,
            },
        )
        request.user = self.user1
        catalog.views.ItemDetailView.as_view()(request, pk=self.item2.id)

        self.client.get(
            django.urls.reverse("users:logout"),
        )

        request = self.factory.post(
            django.urls.reverse(
                "catalog:item_detail",
                kwargs={"pk": self.item.id},
            ),
            {
                "grade": 5,
            },
        )
        request.user = self.user2
        catalog.views.ItemDetailView.as_view()(request, pk=self.item.id)

        request = self.factory.post(
            django.urls.reverse("catalog:item_detail", args=[self.item2.id]),
            {
                "grade": 2,
            },
        )
        request.user = self.user2
        catalog.views.ItemDetailView.as_view()(request, pk=self.item2.id)

        count_grade_by_user = rating.models.Grade.objects.filter(
            user=self.user1,
        ).count()
        average_grade_by_user = rating.models.Grade.objects.filter(
            user=self.user1,
        ).aggregate(average_grade=Avg("grade"))
        self.assertEqual(count_grade_by_user, 2)
        self.assertEqual(int(average_grade_by_user["average_grade"]), 3)

        qs = rating.models.Grade.objects.get_graded_items(user=self.user1)

        max_grade_item_by_user = qs.order_by(
            statistic.views.GRADE_NAME,
            statistic.views.GRADE_ID_NAME,
        ).last()
        self.assertEqual(max_grade_item_by_user.item.name, self.item2.name)
        self.assertEqual(max_grade_item_by_user.item.text, self.item2.text)

        min_grade_item_by_user = qs.order_by(
            statistic.views.GRADE_NAME,
            f"-{statistic.views.GRADE_ID_NAME}",
        ).first()
        self.assertEqual(min_grade_item_by_user.item.name, self.item.name)
        self.assertEqual(min_grade_item_by_user.item.text, self.item.text)

        count_grade_by_user2 = rating.models.Grade.objects.filter(
            user=self.user2,
        ).count()
        average_grade_by_user2 = rating.models.Grade.objects.filter(
            user=self.user2,
        ).aggregate(average_grade=Avg("grade"))
        self.assertEqual(count_grade_by_user2, 2)
        self.assertEqual(
            round(float(average_grade_by_user2["average_grade"]), 1),
            round(3.5, 1),
        )

        qs = rating.models.Grade.objects.get_graded_items(user=self.user2)

        max_grade_item_by_user2 = qs.order_by(
            statistic.views.GRADE_NAME,
            statistic.views.GRADE_ID_NAME,
        ).last()
        self.assertEqual(max_grade_item_by_user2.item.name, self.item.name)
        self.assertEqual(max_grade_item_by_user2.item.text, self.item.text)

        min_grade_item_by_user2 = qs.order_by(
            statistic.views.GRADE_NAME,
            f"-{statistic.views.GRADE_ID_NAME}",
        ).first()
        self.assertEqual(min_grade_item_by_user2.item.name, self.item2.name)
        self.assertEqual(min_grade_item_by_user2.item.text, self.item2.text)

    def test_statistic_by_items(self):

        request = self.factory.post(
            django.urls.reverse(
                "catalog:item_detail",
                kwargs={"pk": self.item.id},
            ),
            {
                "grade": 1,
            },
        )
        request.user = self.user1
        catalog.views.ItemDetailView.as_view()(request, pk=self.item.id)

        request = self.factory.post(
            django.urls.reverse("catalog:item_detail", args=[self.item2.id]),
            {
                "grade": 5,
            },
        )
        request.user = self.user1
        catalog.views.ItemDetailView.as_view()(request, pk=self.item2.id)

        self.client.get(
            django.urls.reverse("users:logout"),
        )

        request = self.factory.post(
            django.urls.reverse(
                "catalog:item_detail",
                kwargs={"pk": self.item.id},
            ),
            {
                "grade": 5,
            },
        )
        request.user = self.user2
        catalog.views.ItemDetailView.as_view()(request, pk=self.item.id)

        request = self.factory.post(
            django.urls.reverse("catalog:item_detail", args=[self.item2.id]),
            {
                "grade": 2,
            },
        )
        request.user = self.user2
        catalog.views.ItemDetailView.as_view()(request, pk=self.item2.id)

        count_grade_by_items = rating.models.Grade.objects.count()
        average_grade_by_items = rating.models.Grade.objects.aggregate(
            average_grade=Avg("grade"),
        )
        self.assertEqual(count_grade_by_items, 4)
        self.assertEqual(
            round(float(average_grade_by_items["average_grade"]), 2),
            round(3.25, 2),
        )
        qs = rating.models.Grade.objects.get_graded_items()

        max_grade_by_items = qs.order_by(
            statistic.views.GRADE_NAME,
            statistic.views.GRADE_ID_NAME,
        ).last()
        self.assertEqual(max_grade_by_items.user.username, self.user2.username)
        self.assertEqual(max_grade_by_items.user.email, self.user2.email)
        min_grade_by_items = qs.order_by(
            statistic.views.GRADE_NAME,
            f"-{statistic.views.GRADE_ID_NAME}",
        ).first()
        self.assertEqual(min_grade_by_items.user.username, self.user1.username)
        self.assertEqual(min_grade_by_items.user.email, self.user1.email)

    def test_statistic_graded_items(self):

        request = self.factory.post(
            django.urls.reverse(
                "catalog:item_detail",
                kwargs={"pk": self.item.id},
            ),
            {
                "grade": 1,
            },
        )
        request.user = self.user1
        catalog.views.ItemDetailView.as_view()(request, pk=self.item.id)

        request = self.factory.post(
            django.urls.reverse("catalog:item_detail", args=[self.item2.id]),
            {
                "grade": 5,
            },
        )
        request.user = self.user1
        catalog.views.ItemDetailView.as_view()(request, pk=self.item2.id)

        self.client.get(
            django.urls.reverse("users:logout"),
        )

        graded_items = rating.models.Grade.objects.get_graded_items(
            user=self.user1,
        ).order_by(f"-{statistic.views.GRADE_NAME}")

        self.assertEqual(graded_items.first().item.name, self.item2.name)
        self.assertEqual(graded_items.first().item.text, self.item2.text)

        self.assertEqual(graded_items.last().item.name, self.item.name)
        self.assertEqual(graded_items.last().item.text, self.item.text)
