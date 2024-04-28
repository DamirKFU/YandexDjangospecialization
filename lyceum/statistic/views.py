from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView, TemplateView

from catalog.models import Item
import rating.models


__all__ = []


GRADE_NAME = rating.models.Grade.grade.field.name
GRADE_ID_NAME = rating.models.Grade.id.field.name


class StatisticByUserTemplateView(
    LoginRequiredMixin,
    TemplateView,
):
    model = rating.models.Grade
    template_name = "statistic/statistic_by_user.html"
    context_object_name = "grades"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = rating.models.Grade.objects.user_love_hate_item()
        user_quey = query.get(pk=self.request.user.id)
        context["query"] = user_quey
        field_name = f"{Item.grades.field.related_query_name()}__{GRADE_NAME}"
        items = (
            Item.objects.published()
            .filter(
                Q(pk=user_quey.love) | Q(pk=user_quey.hate),
            )
            .order_by(f"-{field_name}")
        )

        context["items"] = list(items)

        return context


class StatisticGradedItemsListView(LoginRequiredMixin, ListView):
    template_name = "statistic/statistic_graded_items.html"
    context_object_name = "grades"

    def get(self, request, *args, **kwargs):
        self.queryset = rating.models.Grade.objects.get_graded_items(
            user=request.user,
        ).order_by(f"-{GRADE_NAME}")

        return super().get(request, *args, **kwargs)


class StatisticByItemsListView(
    LoginRequiredMixin,
    ListView,
):
    template_name = "statistic/statistic_by_items.html"
    context_object_name = "items"

    def get(self, request, *args, **kwargs):
        query = rating.models.Grade.objects.item_love_hate_user()
        self.queryset = query

        return super().get(request, *args, **kwargs)
