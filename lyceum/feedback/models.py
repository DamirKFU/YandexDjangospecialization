from django.conf import settings
import django.db
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext_lazy as _


__all__ = []


class Status(django.db.models.TextChoices):
    NEW = "NW", _("new_status")
    PENDING = "PD", _("pending_status")
    COMPLETE = "CP", _("complete_status")


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        "текст",
        max_length=4000,
        help_text="напишите текст сообщения",
    )
    created_on = django.db.models.DateTimeField(
        "создано",
        help_text="дата и время создания",
        auto_now_add=True,
        null=True,
    )
    status = django.db.models.CharField(
        "статус",
        choices=Status.choices,
        help_text="статус обратной связи",
        default=Status.NEW,
        max_length=2,
    )

    @property
    def short_text(self):
        return truncatechars(self.text, 100)

    short_text.fget.field_name = "short_text"
    short_text.fget.short_description = "короткий текст"

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратные связи"

    def __str__(self) -> str:
        return f"обратная связь ({self.id})"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text="пользователь который изменил статус обратной связи",
        verbose_name="пользователь",
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    feedback = django.db.models.ForeignKey(
        Feedback,
        verbose_name="обратная связь",
        help_text="обратная связь лога",
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    timestamp = django.db.models.DateTimeField(
        "создано",
        help_text="дата и время создания",
        auto_now_add=True,
        null=True,
    )
    from_status = django.db.models.CharField(
        "с",
        choices=Status.choices,
        help_text="изменение статуса с",
        db_column="from",
        max_length=2,
    )
    to_status = django.db.models.CharField(
        "на",
        help_text="изменение статуса на",
        choices=Status.choices,
        db_column="to",
        max_length=2,
    )

    class Meta:
        verbose_name = "журнал состояния"
        verbose_name_plural = "журнал состояний"

    def __str__(self) -> str:
        return f"состояние ({self.id})"


class FeedbackFile(django.db.models.Model):
    def upload_to(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        verbose_name="обратная связь",
        related_name="files",
        related_query_name="files",
        help_text="обратная связь файла",
    )
    file = django.db.models.FileField(
        "файл",
        upload_to=upload_to,
        help_text="загрузите файл",
    )

    class Meta:
        verbose_name = "файлы обратной связи"
        verbose_name_plural = "файлы обратных связей"


class FeedbackAuthor(django.db.models.Model):
    name = django.db.models.CharField(
        "имя",
        max_length=150,
        help_text="напишите имя",
        null=True,
        blank=True,
    )
    mail = django.db.models.EmailField(
        "почта",
        help_text="почтовый адрес",
    )
    feedback = django.db.models.OneToOneField(
        Feedback,
        on_delete=django.db.models.CASCADE,
        help_text="обратная связь автора",
        verbose_name="обратная связь",
        related_name="author",
        related_query_name="author",
    )

    class Meta:
        verbose_name = "данные автора"
        verbose_name_plural = "данные авторов"
