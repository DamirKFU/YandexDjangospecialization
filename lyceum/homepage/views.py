from http import HTTPStatus

from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
import django.views.generic

import catalog.models
import homepage.forms

__all__ = []


class HomeView(django.views.generic.ListView):
    template_name = "homepage/index.html"
    context_object_name = "items"
    queryset = catalog.models.Item.objects.on_main()


class CoffeeView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile = request.user.profile
            user_profile.coffee_count += 1
            user_profile.save()

        return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


class EchoFormView(django.views.generic.FormView):
    http_method_names = ["get", "post"]
    template_name = "homepage/echo.html"
    form_class = homepage.forms.EchoForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if request.path == reverse("homepage:echo_submit") and form.is_valid():
            return HttpResponse(form.cleaned_data["text"])

        return HttpResponseNotAllowed(permitted_methods=["POST"])

    def get(self, request, *args, **kwargs):
        if request.path == reverse("homepage:echo"):
            return super().get(request, *args, **kwargs)

        return HttpResponseNotAllowed(permitted_methods=["GET"])

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(permitted_methods=["GET"])
