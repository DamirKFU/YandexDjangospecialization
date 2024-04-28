from pathlib import Path
import re
import uuid

from django.core.exceptions import ValidationError
import django.db
from django.utils.safestring import mark_safe
from slugify import slugify
import sorl

__all__ = []


def normalize_str(value):
    words = re.findall("[0-9а-яёa-z]+", value.lower())
    return slugify("".join(words))


def get_path_image(instance, filename):
    ext = Path(filename).suffix
    return f"catalog/{uuid.uuid4()}{ext}"


class AbstractModel(django.db.models.Model):
    objects = django.db.models.Manager()
    name = django.db.models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="напишите название",
    )
    is_published = django.db.models.BooleanField(
        "опубликовано",
        default=True,
        help_text="поставьте галочку если он опубликован",
    )
    normalize_name = django.db.models.CharField(
        "нормализованное название",
        max_length=150,
        editable=False,
        help_text="этот field не редактируется и нормализует field(name)",
    )

    class Meta:
        verbose_name = "абстрактная модель"
        verbose_name_plural = "абстрактные модели"
        abstract = True

    def clean(self):
        normalize_name = normalize_str(self.name)
        found = self.__class__.objects.filter(
            ~django.db.models.Q(id=self.id),
            normalize_name=normalize_name,
        )
        if found:
            raise ValidationError(
                {self.__class__.name.field.name: "есть похожое название"},
            )

        self.normalize_name = normalize_name

    def __str__(self) -> str:
        return self.name


class BaseImage(django.db.models.Model):
    image = sorl.thumbnail.ImageField(
        "изображение",
        upload_to=get_path_image,
        help_text="загрузите изображение",
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def get_image_413x413(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "413x413",
            crop="center",
            quality=51,
        )

    def get_image_108x108(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "108x108",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            tag = f'<img src="{self.get_image_300x300().url}">'
            return mark_safe(tag)

        return "изображение отсутствует"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"

    class Meta:
        verbose_name = "абстрактная модель изображения"
        verbose_name_plural = "абстрактные модели изображений"
        abstract = True

    def __str__(self):
        return Path(self.image.path).stem
