from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.urls
from django.urls import include, path


urlpatterns = [
    path(
        "",
        include(("homepage.urls")),
        name="homepage",
    ),
    path(
        "about/",
        include(("about.urls")),
        name="about",
    ),
    path(
        "catalog/",
        include(("catalog.urls")),
        name="catalog",
    ),
    path(
        "feedback/",
        include(("feedback.urls")),
        name="feedback",
    ),
    path(
        "auth/",
        include(("users.urls")),
        name="users",
    ),
    path(
        "download/",
        include(("download.urls")),
        name="download",
    ),
    path(
        "statistic/",
        include(("statistic.urls")),
        name="statistic",
    ),
    path(
        "rating/",
        include(("rating.urls")),
        name="rating",
    ),
    path(
        "admin/",
        admin.site.urls,
        name="admin",
    ),
    path(
        "tinymce/",
        include("tinymce.urls"),
    ),
    path(
        "i18n/",
        include("django.conf.urls.i18n"),
    ),
    path(
        "auth/",
        django.urls.include(django.contrib.auth.urls),
    ),
]

if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    if settings.MEDIA_ROOT:
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
