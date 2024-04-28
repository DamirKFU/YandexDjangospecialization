from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

import users.models


__all__ = []


User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = users.models.Profile
    fields = (
        model.birthday.field.name,
        model.image.field.name,
        model.coffee_count.field.name,
    )
    readonly_fields = (model.coffee_count.field.name,)
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
