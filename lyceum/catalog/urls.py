from django.urls import path, re_path, register_converter

from catalog import converters, views


register_converter(converters.PositiveIntegerConverter, "pint")
app_name = "catalog"

urlpatterns = [
    path(
        "",
        views.ItemListView.as_view(),
        name="main",
    ),
    path(
        "<int:pk>/",
        views.ItemDetailView.as_view(),
        name="item_detail",
    ),
    re_path(
        r"^re/(?P<pk>[1-9]\d*)/",
        views.ItemDetailView.as_view(),
        name="re",
    ),
    path(
        "converter/<pint:pk>/",
        views.ItemDetailView.as_view(),
        name="converter",
    ),
    path(
        "new/",
        views.ItemNewListView.as_view(),
        name="new",
    ),
    path(
        "friday/",
        views.ItemFridayListView.as_view(),
        name="friday",
    ),
    path(
        "unverified/",
        views.ItemUnverifiedListView.as_view(),
        name="unverified",
    ),
]
