from django.contrib.auth import views
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.urls import path, reverse_lazy

import users.forms
import users.views

__all__ = []


app_name = "users"

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=users.forms.custom_auth_form(
                AuthenticationForm,
            ),
        ),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=users.forms.custom_auth_form(
                PasswordChangeForm,
            ),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            form_class=users.forms.custom_auth_form(
                PasswordResetForm,
            ),
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            form_class=users.forms.custom_auth_form(
                SetPasswordForm,
            ),
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path(
        "signup/",
        users.views.SignupFormView.as_view(),
        name="signup",
    ),
    path(
        "activate/<username>/",
        users.views.ActivateRedirectView.as_view(),
        name="activate",
    ),
    path(
        "user_list/",
        users.views.UserListView.as_view(),
        name="user_list",
    ),
    path(
        "<int:pk>/",
        users.views.UserDetailView.as_view(),
        name="user_detail",
    ),
    path(
        "profile/",
        users.views.ProfileUpdateView.as_view(),
        name="profile",
    ),
]
