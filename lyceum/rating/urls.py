from django.urls import path

from rating import views

app_name = "rating"

urlpatterns = [
    path(
        "delete/<int:pk>/",
        views.DeleteRedirectView.as_view(),
        name="delete",
    ),
]
