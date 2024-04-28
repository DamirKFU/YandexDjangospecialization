from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
import django.views.generic

import catalog.models


__all__ = []


class DeleteRedirectView(
    LoginRequiredMixin,
    django.views.generic.RedirectView,
):
    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(
            catalog.models.Item.objects,
            pk=kwargs.get("pk"),
        )
        grade = get_object_or_404(item.grades, user=self.request.user)
        grade.delete()
        return reverse("catalog:item_detail", kwargs=kwargs)
