import datetime
import unittest.mock

import django.core.mail
import django.test
import django.urls
import django.utils
import parameterized

import users.models

__all__ = []


class TestUserViews(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = django.test.Client()
        cls.user_model = users.models.USER_MODEL

    @classmethod
    def tearDownClass(cls):
        cls.user_model.objects.all().delete()
        super().tearDownClass()

    def test_signup(self):
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            django.urls.reverse("users:login"),
        )

        self.assertTrue(
            self.user_model.objects.filter(username="testinguser").exists(),
        )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="testinguser",
        )

        self.assertTrue(
            user.is_authenticated,
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_login(self):
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
        response1 = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["username"],
                "password": data["password1"],
            },
        )
        self.assertRedirects(
            response1,
            django.urls.reverse("homepage:main"),
        )
        response2 = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["email"],
                "password": data["password1"],
            },
        )
        self.assertRedirects(
            response2,
            django.urls.reverse("homepage:main"),
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_positive(self):
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="test_username",
        )
        self.assertFalse(user.is_active)
        self.client.get(
            django.urls.reverse("users:activate", args=["test_username"]),
        )
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="test_username",
        )
        self.assertTrue(user.is_active)

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_negative(self):
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username2",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        expired_dt = django.utils.timezone.now() + datetime.timedelta(hours=13)
        with unittest.mock.patch(
            "django.utils.timezone.now",
        ) as mocked_timezone:
            mocked_timezone.return_value = expired_dt
            self.client.get(
                django.urls.reverse("users:activate", args=["test_username2"]),
            )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="test_username2",
        )

        self.assertFalse(user.is_active)

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_userproxy_isinstance(self):
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username2",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.client.post(
            django.urls.reverse("users:login"),
            data={
                "username": "test_username2",
                "password": "testpassword",
            },
        )
        response = self.client.get(django.urls.reverse("homepage:main"))
        self.assertIn("user", response.context)
        self.assertIsInstance(response.context["user"], users.models.User)

    @parameterized.parameterized.expand(
        [
            ("test@dev.com", "test@dev.com"),
            ("test@yandex.ru", "test@ya.ru"),
            ("tEsT@Yandex.rU", "test@ya.ru"),
            ("test+tag@dev.com", "test@dev.com"),
            ("test+some_words@dev.com", "test@dev.com"),
            ("T-e-s-t@yandex.ru", "t-e-s-t@ya.ru"),
            ("T-e-s-t@yandex.ru", "t-e-s-t@ya.ru"),
            ("t.e.s.t@gmail.com", "test@gmail.com"),
            ("T.e.S.t@gmail.com", "test@gmail.com"),
        ],
    )
    @django.test.override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_email_normalization(self, email: str, norm_email: str) -> None:
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "email": email,
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        user = users.models.User.objects.get(username="test_username")
        self.assertIsNotNone(user)
        if not user:
            return

        self.assertEqual(user.email, norm_email)

    @parameterized.parameterized.expand(
        [
            (datetime.timedelta(hours=1), True),
            (datetime.timedelta(days=1), True),
            (datetime.timedelta(days=4), True),
            (datetime.timedelta(days=6), True),
            (datetime.timedelta(days=7, minutes=1), False),
            (datetime.timedelta(days=10), False),
        ],
    )
    @django.test.override_settings(
        DEFAULT_USER_IS_ACTIVE=True,
        MAX_AUTH_ATTEMPTS=3,
    )
    def test_reset_link_expiration(self, timedelta, is_active):
        self.assertFalse(self.user_model.objects.exists())
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertTrue(self.user_model.objects.first().is_active)
        for _ in range(3):
            self.client.login(
                username="test_username",
                password="wrong_pass",
            )

        self.assertFalse(self.user_model.objects.first().is_active)

        future_date = django.utils.timezone.now() + timedelta
        with unittest.mock.patch("django.utils.timezone.now") as mocked_now:
            mocked_now.return_value = future_date
            self.client.get(
                django.urls.reverse("users:activate", args=["test_username"]),
            )

        self.assertEqual(
            users.models.User.objects.first().is_active,
            is_active,
        )


class TestContextProcessor(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = django.test.Client()
        cls.user_model = users.models.USER_MODEL

    @parameterized.parameterized.expand(
        [
            ["homepage", "main"],
            ["catalog", "main"],
            ["about", "main"],
        ],
    )
    def test_processor_in_context(self, namespace, name):
        response = self.client.get(
            django.urls.reverse(f"{namespace}:{name}"),
        )

        self.assertIn("birthdays", response.context)

    @parameterized.parameterized.expand(
        [
            [datetime.timedelta(days=0), 1],
            [datetime.timedelta(days=1), 0],
        ],
    )
    def test_correct_context(self, timedelta, count):
        user1 = self.user_model.objects.create(username="user1", password=123)
        user1_profile = users.models.Profile.objects.create(
            birthday=django.utils.timezone.now().date() - timedelta,
            user=user1,
        )
        user1.full_clean()
        user1.save()
        user1_profile.full_clean()
        user1_profile.save()

        response = self.client.get(
            django.urls.reverse("homepage:main"),
        )
        self.assertEqual(
            len(response.context["birthdays"]),
            count,
            f"Timedelta is: {timedelta}",
        )
