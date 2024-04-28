from pathlib import Path
import sys
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
import django.db

import users.validators


__all__ = []

USER_MODEL = get_user_model()

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    USER_MODEL._meta.get_field("email")._unique = True


def get_path_image(instance, filename):
    ext = Path(filename).suffix
    return f"users/{uuid.uuid4()}{ext}"


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="пользователь",
        help_text="укажите пользователя",
        related_name="profile",
        related_query_name="profile",
        on_delete=django.db.models.CASCADE,
    )
    birthday = django.db.models.DateField(
        "дата рождения",
        help_text="укажите дату рождения",
        validators=[users.validators.birthday_validator],
        null=True,
        blank=True,
    )
    image = django.db.models.ImageField(
        "аватарка",
        help_text="загрузите автарку",
        upload_to=get_path_image,
        null=True,
        blank=True,
    )
    coffee_count = django.db.models.PositiveIntegerField(
        "количество переходов по /coffee/",
        help_text="сколько раз пользователь пытался сварить кофе",
        default=0,
    )
    attempts_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="количество попыток входа",
    )
    deactivation_date = django.db.models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="дата деактивации аккаунта",
    )

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

    class Meta:
        verbose_name = "дополнительное поле пользователя"
        verbose_name_plural = "дополнительные поля пользователей"


class UserProxyManager(django.contrib.auth.models.UserManager):
    CONONICAL_DOMAINS = {
        "yandex.ru": "ya.ru",
    }
    DOTS = {
        "ya.ry": "-",
        "gmail.com": "",
    }

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain_part = email.rsplit("@", 1)
            email_name, *_ = email_name.split("+", 1)
            domain_part = cls.CONONICAL_DOMAINS.get(domain_part, domain_part)
            email_name = email_name.replace(
                ".",
                cls.DOTS.get(domain_part, "."),
            )
        except ValueError:
            pass
        else:
            email = f"{email_name}@{domain_part}"

        return email

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                USER_MODEL.profile.related.name,
            )
        )

    def active(self):
        return (
            self.get_queryset().filter(
                is_active=True,
            )
        ).only(
            USER_MODEL.username.field.name,
            USER_MODEL.is_superuser.field.name,
            USER_MODEL.first_name.field.name,
            USER_MODEL.last_name.field.name,
            USER_MODEL.email.field.name,
            f"{USER_MODEL.profile.related.name}__{Profile.image.field.name}",
            f"{USER_MODEL.profile.related.name}__"
            f"{Profile.birthday.field.name}",
            f"{USER_MODEL.profile.related.name}__"
            f"{Profile.coffee_count.field.name}",
        )

    def user_list(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_active=True,
            )
        ).only(
            USER_MODEL.username.field.name,
        )

    def by_mail(self, email):
        return self.get_queryset().get(email=self.normalize_email(email))


class User(get_user_model()):
    objects = UserProxyManager()

    class Meta:
        proxy = True
