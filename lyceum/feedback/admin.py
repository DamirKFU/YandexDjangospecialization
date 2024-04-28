from django.contrib import admin

import feedback.models

__all__ = []


class FeedbackAuthorInline(admin.TabularInline):
    model = feedback.models.FeedbackAuthor
    readonly_fields = ("name", "mail")
    can_delete = False


class FeedbackFileInline(admin.TabularInline):
    model = feedback.models.FeedbackFile
    readonly_fields = ("file",)


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.short_text.fget.field_name,
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.status.field.name,
    )

    fields = (
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.status.field.name,
    )

    readonly_fields = (
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.text.field.name,
    )

    inlines = [FeedbackAuthorInline, FeedbackFileInline]

    def save_model(self, request, obj, form, change):
        if "status" in form.changed_data:
            feedback.models.StatusLog(
                user=request.user,
                feedback=obj,
                from_status=form.initial["status"],
                to_status=form.cleaned_data["status"],
            ).save()

        super().save_model(request, obj, form, change)


@admin.register(feedback.models.StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to_status.field.name,
    )
    readonly_fields = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog.from_status.field.name,
        feedback.models.StatusLog.to_status.field.name,
        feedback.models.StatusLog.feedback.field.name,
    )
