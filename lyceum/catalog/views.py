import datetime
import random

from django.contrib.auth.decorators import login_required
import django.contrib.messages
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
import django.views.generic

import catalog.models
import rating.forms
import rating.models

__all__ = []


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.published()


class ItemDetailView(
    django.views.generic.edit.FormMixin,
    django.views.generic.DetailView,
):
    template = "catalog/item_detail.html"
    context_object_name = "item"
    queryset = catalog.models.Item.objects.get_item()
    model = rating.models.Grade
    form_class = rating.forms.GradeForm

    def get_success_url(self):
        django.contrib.messages.success(
            self.request,
            _("message_grade_save_success"),
            fail_silently=True,
        )
        return reverse("catalog:item_detail", kwargs={"pk": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("item_list_title")
        return context

    def get_form_kwargs(self):
        kwargs = super(ItemDetailView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            grade = self.object.grades.filter(
                user=self.request.user,
            ).first()
            kwargs.update(
                instance=grade,
            )

        return kwargs

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        grade = form.save(commit=False)
        grade.user = self.request.user
        grade.item = self.object
        grade.save()
        return super().form_valid(form)


class ItemNewListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        qs = self.model.objects.published()
        items = list(
            qs.filter(
                created__gt=timezone.now() - datetime.timedelta(hours=24 * 7),
            ).all(),
        )
        ln_items = len(items)
        return sorted(
            random.sample(items, 5 if ln_items >= 5 else ln_items),
            key=lambda item: item.category.name,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("new")
        return context


class ItemFridayListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        qs = self.model.objects.published()
        item_category = catalog.models.Item.category.field.name
        category_name = catalog.models.Category.name.field.name
        return reversed(
            qs.filter(updated__week_day=6).order_by(
                f"-{item_category}__{category_name}",
            )[:5],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("friday")
        return context


class ItemUnverifiedListView(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    model = catalog.models.Item

    def get_queryset(self):
        qs = self.model.objects.published()
        return qs.filter(updated=F("created"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter"] = _("unverified")
        return context
