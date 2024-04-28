import django.core.validators
import django.db
from django.utils import timezone
from slugify import slugify
import tinymce.models

from catalog.validators import ValidateMustContain
from core.models import AbstractModel, BaseImage


__all__ = []


class Round(django.db.models.Func):
    function = "ROUND"
    arity = 2


class Tag(AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        blank=True,
        help_text="строка идентификатор"
        "(заполните чтобы изменить автоматический слаг)",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        blank=True,
        help_text="строка идентификатор"
        "(заполните чтобы изменить автоматический слаг)",
    )
    weight = django.db.models.IntegerField(
        "вес",
        default=100,
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
        help_text="ну какой вес то",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class ItemManager(django.db.models.Manager):
    def published(self):
        queryset = (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
        )
        return queryset.only(
            Item.name.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            Item.text.field.name,
            f"{Item.tags.field.name}__{Tag.name.field.name}",
            f"{Item.main_image.related.name}__"
            f"{ItemMainImage.image.field.name}",
        ).order_by(f"{Item.category.field.name}__{Category.name.field.name}")

    def on_main(self):

        return (
            self.published()
            .filter(is_on_main=True)
            .order_by(Item.name.field.name)
        )

    def get_item(self):
        queryset = (
            self.published()
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.images.field.related_query_name(),
                    queryset=ItemSecondaryImage.objects.all(),
                ),
            )
            .annotate(
                rating=django.db.models.ExpressionWrapper(
                    Round(
                        django.db.models.Avg(
                            f"{Item.grades.field.related_query_name()}__"
                            f"{Item.grades.field.model.grade.field.name}",
                        ),
                        2,
                    ),
                    output_field=django.db.models.FloatField(),
                ),
                count_grade=django.db.models.Count(
                    Item.grades.field.related_query_name(),
                ),
            )
        )

        return queryset.only(
            Item.name.field.name,
            f"{Item.category.field.name}__{Category.name.field.name}",
            Item.text.field.name,
            f"{Item.tags.field.name}__{Tag.name.field.name}",
            f"{Item.main_image.related.name}__"
            f"{ItemMainImage.image.field.name}",
            f"{Item.images.field._related_name}__"
            f"{ItemSecondaryImage.image.field.name}",
        )


class Item(AbstractModel):
    objects = ItemManager()
    is_on_main = django.db.models.BooleanField(
        "в главном",
        default=False,
        help_text="находится на домашней странице",
    )
    text = tinymce.models.HTMLField(
        "текст",
        validators=[
            ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="опишите",
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        related_name="items",
        related_query_name="items",
        help_text="выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="теги",
        related_name="items",
        related_query_name="items",
        help_text="выберите теги",
    )
    created = django.db.models.DateTimeField(
        "создано",
        help_text="дата и время создания",
        auto_now_add=True,
        null=True,
    )
    updated = django.db.models.DateTimeField(
        "обновлено",
        help_text="дата и время обновления",
        editable=False,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.updated:
            self.updated = self.created
        else:
            self.updated = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ItemMainImage(BaseImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        verbose_name="товар",
        help_text="товар изображения",
        related_name="main_image",
        related_query_name="main_image",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class ItemSecondaryImage(BaseImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        verbose_name="товар",
        help_text="товар изображения",
        related_name="images",
        related_query_name="images",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "дополнительные изображения"
