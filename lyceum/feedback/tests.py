from pathlib import Path
import shutil

from django.conf import settings
from django.core import validators
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse
from parameterized import parameterized

from feedback.forms import FeedbackAuthorForm, FeedbackFileForm, FeedbackForm
from feedback.models import Feedback


__all__ = []


MEDIA_TEST: Path = settings.BASE_DIR / "media_test"


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()
        cls.form_author = FeedbackAuthorForm()

    def test_mail_label(self):
        mail_label = FormTests.form_author.fields["mail"].label
        self.assertEqual(mail_label, "Почта")

    def test_text_label(self):
        text_label = FormTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст")

    def test_mail_help_text(self):
        mail_help_text = FormTests.form_author.fields["mail"].help_text
        self.assertEqual(
            mail_help_text,
            "почтовый адрес",
        )

    def test_text_help_text(self):
        text_help_text = FormTests.form.fields["text"].help_text
        self.assertEqual(text_help_text, "напишите текст сообщения")

    @parameterized.expand(
        [
            ("content", FeedbackForm),
            ("author", FeedbackAuthorForm),
            ("files", FeedbackFileForm),
        ],
    )
    def test_correct_context(
        self,
        form_name,
        form_type,
    ):
        with self.subTest(form_name=form_name, form_type=form_type):
            response = self.client.get(reverse("feedback:feedback"))
            self.assertIn("form", response.context)
            self.assertIn(form_name, response.context["form"].forms)
            form = response.context["form"][form_name]
            self.assertIsInstance(form, form_type)

    @parameterized.expand(
        [
            (
                {
                    "content-text": "some text",
                    "author-name": "",
                    "author-mail": "test@test.com",
                },
            ),
            (
                {
                    "content-text": "some text",
                    "author-name": "Vasya",
                    "author-mail": "test@test.com",
                },
            ),
        ],
    )
    def test_from(self, data):
        with self.subTest(data=data):
            feedback_count = Feedback.objects.count()
            response = self.client.post(
                reverse("feedback:feedback"),
                data=data,
                follow=True,
            )

            self.assertRedirects(response, reverse("feedback:feedback"))
            self.assertEqual(
                Feedback.objects.count(),
                feedback_count + 1,
                "Feedback not created",
            )
            self.assertTrue(
                Feedback.objects.filter(
                    author__mail=data["author-mail"],
                    author__name=data["author-name"] or None,
                    text=data["content-text"],
                ).exists(),
                "Uncorrect feedback created",
            )

    def test_form_errors(self):
        data = {"content-text": "some text", "author-mail": "wrong email"}
        feedback_count = Feedback.objects.count()
        response = self.client.post(
            reverse("feedback:feedback"),
            data=data,
            follow=True,
        )
        self.assertFormError(
            response,
            "form",
            "author-mail",
            validators.EmailValidator.message,
        )
        self.assertEqual(
            Feedback.objects.count(),
            feedback_count,
            "Feedback created while validation failed",
        )

    @override_settings(MEDIA_ROOT=MEDIA_TEST)
    def test_form_file_upload(self):
        content = "Test file content".encode()
        file_upload = SimpleUploadedFile(
            "file.txt",
            content,
            content_type="text/plain",
        )
        data = {
            "content-text": "some text",
            "author-mail": "test@test.com",
            "files-files": [file_upload],
        }
        feedback_count = Feedback.objects.count()
        response = self.client.post(
            reverse("feedback:feedback"),
            data=data,
            format="multipart",
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(
            Feedback.objects.count(),
            feedback_count + 1,
            "Feedback not created",
        )
        feedback = Feedback.objects.filter(
            author__mail=data["author-mail"],
            text=data["content-text"],
        ).get()
        files = list(feedback.files.all())
        self.assertEqual(len(files), 1, "Wrong count of files created")
        with (MEDIA_TEST / files[0].file.name).open("rb") as f:
            self.assertEqual(f.read(), content, "Wrong file content")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if Path.exists(MEDIA_TEST):
            shutil.rmtree(MEDIA_TEST)
