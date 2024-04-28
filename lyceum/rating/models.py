from django.conf import settings
import django.db.models

import catalog.models
import users.models

__all__ = []


CATALOG_ITEM_TAGS_NAME = catalog.models.Item.tags.field.name
CATALOG_ITEM_CATEGORY_NAME = catalog.models.Item.category.field.name
CATALOG_ITEM_MAIN_IMAGE_NAME = catalog.models.Item.main_image.related.name
CATALOG_CATEGORY_NAME_NAME = catalog.models.Category.name.field.name
CATALOG_MAIN_IMAGE_IMAGE_NAME = catalog.models.ItemMainImage.image.field.name
CATALOG_ITEM_NAME_NAME = catalog.models.Item.name.field.name
CATALOG_ITEM_TEXT_NAME = catalog.models.Item.text.field.name


class GradeManager(django.db.models.Manager):

    def get_graded_items(self, user=None):

        queryset = self.get_queryset()

        if user is not None:
            queryset = queryset.filter(user=user)

        queryset = queryset.filter(
            item__is_published=True,
            item__category__is_published=True,
        )

        queryset_select_related = queryset.select_related(
            f"{Grade.item.field.name}__" f"{CATALOG_ITEM_CATEGORY_NAME}",
            f"{Grade.item.field.name}__" f"{CATALOG_ITEM_MAIN_IMAGE_NAME}",
        )
        queryset_prefetch_related = queryset_select_related.prefetch_related(
            django.db.models.Prefetch(
                f"{Grade.item.field.name}__" f"{CATALOG_ITEM_TAGS_NAME}",
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only(
                    catalog.models.Tag.name.field.name,
                ),
            ),
        )
        return queryset_prefetch_related.only(
            f"{Grade.grade.field.name}",
            f"{Grade.item.field.name}__{CATALOG_ITEM_NAME_NAME}",
            f"{Grade.item.field.name}__"
            f"{CATALOG_ITEM_CATEGORY_NAME}__"
            f"{CATALOG_CATEGORY_NAME_NAME}",
            f"{Grade.item.field.name}__{CATALOG_ITEM_TEXT_NAME}",
            f"{Grade.item.field.name}__"
            f"{CATALOG_ITEM_MAIN_IMAGE_NAME}__"
            f"{CATALOG_MAIN_IMAGE_IMAGE_NAME}",
        )

    def user_love_hate_item(self):
        return users.models.USER_MODEL.objects.annotate(
            avg_grades=django.db.models.Avg(
                f"{catalog.models.Item.grades.field.related_query_name()}__"
                f"{Grade.grade.field.name}",
            ),
            count_grades=django.db.models.Count(
                catalog.models.Item.grades.field.related_query_name(),
            ),
            love=django.db.models.Subquery(
                catalog.models.Item.objects.filter(
                    pk=django.db.models.Subquery(
                        Grade.objects.filter(
                            user=django.db.models.OuterRef(
                                django.db.models.OuterRef(
                                    users.models.USER_MODEL.id.field.name,
                                ),
                            ),
                        )
                        .order_by(f"-{Grade.grade.field.name}")
                        .values(Grade.item.field.name)[:1],
                    ),
                ).values(Grade.id.field.name)[:1],
            ),
            hate=django.db.models.Subquery(
                catalog.models.Item.objects.filter(
                    pk=django.db.models.Subquery(
                        Grade.objects.filter(
                            user=django.db.models.OuterRef(
                                django.db.models.OuterRef(
                                    users.models.USER_MODEL.id.field.name,
                                ),
                            ),
                        )
                        .order_by(Grade.grade.field.name)
                        .values(Grade.item.field.name)[:1],
                    ),
                ).values(catalog.models.Item.id.field.name)[:1],
            ),
        ).only(Grade.id.field.name)

    def item_love_hate_user(self):
        return catalog.models.Item.objects.published().annotate(
            avg_grades=django.db.models.Avg(
                f"{catalog.models.Item.grades.field.related_query_name()}__"
                f"{Grade.grade.field.name}",
            ),
            count_grades=django.db.models.Count(
                catalog.models.Item.grades.field.related_query_name(),
            ),
            love=django.db.models.Subquery(
                users.models.USER_MODEL.objects.filter(
                    pk=django.db.models.Subquery(
                        Grade.objects.filter(
                            item=django.db.models.OuterRef(
                                django.db.models.OuterRef(
                                    catalog.models.Item.id.field.name,
                                ),
                            ),
                        )
                        .order_by(f"-{Grade.grade.field.name}")
                        .values(
                            f"{Grade.user.field.name}__"
                            f"{users.models.User.id.field.name}",
                        )[:1],
                    ),
                ).values(users.models.User.username.field.name)[:1],
            ),
            hate=django.db.models.Subquery(
                users.models.USER_MODEL.objects.filter(
                    pk=django.db.models.Subquery(
                        Grade.objects.filter(
                            item=django.db.models.OuterRef(
                                django.db.models.OuterRef(
                                    catalog.models.Item.id.field.name,
                                ),
                            ),
                        )
                        .order_by(f"{Grade.grade.field.name}")
                        .values(
                            f"{Grade.user.field.name}__"
                            f"{users.models.User.id.field.name}",
                        )[:1],
                    ),
                ).values(users.models.User.username.field.name)[:1],
            ),
        )


class Grade(django.db.models.Model):
    objects = GradeManager()

    GRADE_CHOICES = (
        (1, "Ненависть"),
        (2, "Неприязнь"),
        (3, "Нейтрально"),
        (4, "Обожание"),
        (5, "Любовь"),
    )
    user = django.db.models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text="пользователь который поставил оценку",
        related_name="grades",
        related_query_name="grades",
        verbose_name="пользователь",
        on_delete=django.db.models.CASCADE,
    )

    item = django.db.models.ForeignKey(
        catalog.models.Item,
        help_text="товар которому поставили оценку",
        related_name="grades",
        related_query_name="grades",
        verbose_name="товар",
        on_delete=django.db.models.CASCADE,
    )

    grade = django.db.models.IntegerField(
        choices=GRADE_CHOICES,
        verbose_name="оценка",
        help_text="поставьте оценку",
    )

    class Meta:
        unique_together = (
            "user",
            "item",
        )
        verbose_name = "оценка"
        verbose_name_plural = "оценки"

    def __str__(self):
        return f"Оценка({self.id})->{self.grade}\u2605"
