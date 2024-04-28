from django.urls import path

from homepage import views

app_name = "homepage"
urlpatterns = [
    path(
        "",
        views.HomeView.as_view(),
        name="main",
    ),
    path(
        "coffee/",
        views.CoffeeView.as_view(),
        name="coffee",
    ),
    path(
        "echo/",
        views.EchoFormView.as_view(),
        name="echo",
    ),
    path(
        "echo/submit/",
        views.EchoFormView.as_view(),
        name="echo_submit",
    ),
]
