import datetime

from django.conf import settings
import django.contrib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
import django.forms
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import django.views.generic

import users.forms
import users.models


__all__ = []


class SignupFormView(django.views.generic.FormView):
    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        user.profile = users.models.Profile.objects.create(user_id=user.id)
        context_email = {
            "username": user.username,
        }
        send_mail(
            subject="Activate your account",
            message=render_to_string("users/signup_email.html", context_email),
            from_email=settings.EMAIL_HOST,
            recipient_list=[user.email],
        )
        django.contrib.messages.success(
            self.request,
            _("message_signup_success"),
        )
        return super().form_valid(form)


class ActivateRedirectView(django.views.generic.RedirectView):
    url = reverse_lazy("homepage:main")

    def get_redirect_url(self, *args, **kwargs):
        user = get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username=kwargs.get("username"),
        )
        if user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
            time_limit = datetime.timedelta(days=7)
            start_date = user.profile.deactivation_date
        else:
            time_limit = datetime.timedelta(hours=12)
            start_date = user.date_joined

        if timezone.now() < start_date + time_limit:
            user.is_active = True
            user.save()
            user.profile.attempts_count = 0
            user.profile.save()
            django.contrib.messages.success(
                self.request,
                _("message_activate_success"),
            )
        else:
            django.contrib.messages.error(
                self.request,
                _("message_activate_error"),
            )

        return super().get_redirect_url(*args, **kwargs)


class UserListView(django.views.generic.ListView):
    template_name = "users/user_list.html"
    context_object_name = "users"
    queryset = users.models.User.objects.user_list()
    paginate_by = 100


class UserDetailView(django.views.generic.DetailView):
    template_name = "users/user_detail.html"
    context_object_name = "user_item"
    queryset = users.models.User.objects.active()


class ProfileUpdateView(LoginRequiredMixin, django.views.generic.UpdateView):
    template_name = "users/profile.html"
    form_class = users.forms.UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs.update(
            instance={
                "user": self.object,
                "profile": self.object.profile,
            },
        )
        return kwargs

    def get_form(self, form_class=None):
        this_year = datetime.date.today().year
        year_range = range(this_year - 100, this_year + 1)
        form = super(ProfileUpdateView, self).get_form(form_class)
        form.forms["profile"].fields["birthday"].widget = (
            django.forms.SelectDateWidget(
                years=year_range,
                attrs={"class": "form-control"},
            )
        )
        return form

    def get_success_url(self):
        django.contrib.messages.success(
            self.request,
            _("message_profile_save_success"),
        )
        return super().get_success_url()
