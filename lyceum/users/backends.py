from django.conf import settings
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


import users.models


__all__ = []


class EmailUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = users.models.User.objects.get_by_natural_key(
                username=username,
            )
        except users.models.User.DoesNotExist:
            try:
                user = users.models.User.objects.by_mail(username)
            except users.models.User.DoesNotExist:
                return None

        try:
            user.profile
        except users.models.User.profile.RelatedObjectDoesNotExist:
            user.profile = users.models.Profile.objects.create(user=user)

        if user.check_password(password):
            user.profile.attempts_count = 0
            user.profile.save()

            return user

        user.profile.attempts_count += 1
        if user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
            user.is_active = False
            user.save()
            context = {
                "username": user.username,
            }
            send_mail(
                subject="Activate your account",
                message=render_to_string(
                    "users/signup_email.html",
                    context,
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            user.profile.deactivation_date = timezone.now()
            if request:
                messages.error(request, _("message_acount_closed"))

        user.profile.save()
        return None
