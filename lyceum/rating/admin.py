from django.contrib import admin

import rating.models

__all__ = []


@admin.register(rating.models.Grade)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        rating.models.Grade.user.field.name,
        rating.models.Grade.item.field.name,
        rating.models.Grade.grade.field.name,
    )
    readonly_fields = (
        rating.models.Grade.user.field.name,
        rating.models.Grade.item.field.name,
        rating.models.Grade.grade.field.name,
    )
