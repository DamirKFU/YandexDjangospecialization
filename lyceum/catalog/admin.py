from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

import catalog.models

__all__ = []


class ItemMainImageInline(AdminImageMixin, admin.TabularInline):
    fields = ["image"]
    model = catalog.models.ItemMainImage


class ItemSecondaryImageInline(AdminImageMixin, admin.TabularInline):
    fields = ["image"]
    model = catalog.models.ItemSecondaryImage


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.field.name,)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (catalog.models.Category.name.field.name,)


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )
    list_editable = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )
    readonly_fields = (
        catalog.models.Item.created.field.name,
        catalog.models.Item.updated.field.name,
    )
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)

    inlines = [
        ItemMainImageInline,
        ItemSecondaryImageInline,
    ]
