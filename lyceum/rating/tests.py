from django.core.exceptions import ValidationError
from django.test import Client, override_settings, TestCase
import django.urls

import catalog.models
import rating.models
import users.models


__all__ = []


@override_settings(DEFAULT_USER_IS_ACTIVE=True)
class GreadeTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user_model = users.models.USER_MODEL
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
        cls.item.full_clean()
        cls.item.save()

        cls.item.tags.add(cls.tag)

    @classmethod
    def tearDownClass(cls):
        rating.models.Grade.objects.all().delete()
        super().tearDownClass()

    def test_add_grade(self):
        count_grades = rating.models.Grade.objects.count()
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )
        self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["username"],
                "password": data["password1"],
            },
        )
        item = self.item
        response = self.client.post(
            django.urls.reverse("catalog:item_detail", args=[item.id]),
            {
                "grade": 1,
            },
        )
        self.assertRedirects(
            response,
            django.urls.reverse("catalog:item_detail", args=[item.id]),
        )
        grade = item.grades.first()
        self.assertEqual(grade.grade, 1)
        response = self.client.post(
            django.urls.reverse("catalog:item_detail", args=[item.id]),
            {
                "grade": 2,
            },
        )
        self.assertEqual(
            rating.models.Grade.objects.count(),
            count_grades + 1,
        )
        self.assertRedirects(
            response,
            django.urls.reverse("catalog:item_detail", args=[item.id]),
        )
        grade = item.grades.get(pk=grade.id)
        self.assertEqual(grade.grade, 2)

    def test_delete_grade(self):
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )
        self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["username"],
                "password": data["password1"],
            },
        )
        item = self.item
        self.client.post(
            django.urls.reverse("catalog:item_detail", args=[item.id]),
            {
                "grade": 1,
            },
        )
        count_grades = rating.models.Grade.objects.count()
        response = self.client.get(
            django.urls.reverse("rating:delete", args=[item.id]),
        )
        self.assertRedirects(
            response,
            django.urls.reverse("catalog:item_detail", args=[item.id]),
        )
        self.assertEqual(
            rating.models.Grade.objects.count(),
            count_grades - 1,
        )

    def test_add_novalidate_grade(self):
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )
        self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["username"],
                "password": data["password1"],
            },
        )
        user = users.models.USER_MODEL.objects.first()
        grade = rating.models.Grade(
            user=user,
            grade=1,
            item=self.item,
        )
        grade.full_clean()
        grade.save()
        with self.assertRaises(ValidationError):
            no_valid_grade = rating.models.Grade(
                user=user,
                grade=1,
                item=self.item,
            )
            no_valid_grade.full_clean()
            no_valid_grade.save()

    def test_rating_correct_context(self):
        grade_grades = [1, 1, 3, 1, 4, 5, 1]
        for i in range(1, len(grade_grades)):
            with self.subTest(i=i):
                user = self.user_model.objects.create(
                    username=f"user{i}",
                    password="0612",
                )
                item = self.item
                grade = rating.models.Grade(
                    user=user,
                    grade=grade_grades[i - 1],
                    item=self.item,
                )
                grade.save()
                responce = self.client.get(
                    django.urls.reverse("catalog:item_detail", args=[item.id]),
                )
                context = responce.context
                self.assertIn("item", context)
                item_ctx = context["item"]
                avg = round(sum(grade_grades[:i]) / i, 2)
                self.assertEqual(item_ctx.count_grade, i)
                self.assertEqual(item_ctx.rating, avg)
