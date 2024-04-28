from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import django.views.generic

from feedback.forms import (
    FeedbackMultiForm,
)
from feedback.models import FeedbackFile

__all__ = []


class FeedbackCreateView(django.views.generic.CreateView):
    template_name = "feedback/feedback.html"
    form_class = FeedbackMultiForm
    success_url = reverse_lazy("feedback:feedback")

    def form_valid(self, form):
        author_form = form["author"]
        content_form = form["content"]
        files_form = form["files"]

        feedback_instance = content_form.save(commit=True)
        author_form.instance.feedback = feedback_instance
        author_form.save(commit=True)

        files = files_form.cleaned_data["files"]
        for file in files:
            FeedbackFile(file=file, feedback=feedback_instance).save()

        send_mail(
            subject="Feedback",
            message=content_form.cleaned_data["text"],
            from_email=settings.EMAIL_HOST,
            recipient_list=[author_form.cleaned_data["mail"]],
        )
        messages.success(self.request, _("message_form_success"))
        return redirect(self.success_url)
