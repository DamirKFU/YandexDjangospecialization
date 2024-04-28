import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv


__all__ = []

load_dotenv()


def true_load(value: str, defoult: bool) -> bool:
    env_value = os.getenv(value, str(defoult)).lower()
    return env_value in ("", "true", "yes", "1", "y")


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "ABOBA")

DEBUG = true_load("DJANGO_DEBUG", False)

ALLOWED_HOSTS = list(
    map(str.strip, os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")),
)

DEFAULT_USER_IS_ACTIVE = os.getenv("DJANGO_DEFAULT_USER_IS_ACTIVE", DEBUG)

ALLOW_REVERSE = true_load("DJANGO_ALLOW_REVERSE", True)

MAX_AUTH_ATTEMPTS = int(os.getenv("MAX_AUTH_ATTEMPTS", 5))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "core.apps.CoreConfig",
    "rating.apps.RatingConfig",
    "users.apps.UsersConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
    "homepage.apps.HomepageConfig",
    "statistic.apps.StatisticConfig",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "tinymce",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "lyceum.middleware.ReverseResponseMiddleware",
    "users.middleware.UserProxyRequestMiddleware",
]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "users.context_processors.users_birthday",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib."
        "auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib."
        "auth.password_validation."
        "NumericPasswordValidator",
    },
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = os.getenv("DJANGO_INTERNAL_IPS", "127.0.0.1").split(",")

LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "ru")

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login/"
AUTHENTICATION_BACKENDS = ["users.backends.EmailUsernameBackend"]


LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]

LOCALE_PATHS = (BASE_DIR / "locale",)

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

STATIC_ROOT = BASE_DIR.parent / "static"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / "send_mail"

EMAIL_HOST = os.getenv("DJANGO_MAIL")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
