from betterforms.multiform import MultiModelForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import django.forms

import users.models

__all__ = []


def custom_auth_form(form):
    class CustomForm(form):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            for field in self.visible_fields():
                field.field.widget.attrs["class"] = "form-control"

    return CustomForm


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        model = users.models.User
        fields = (
            model.username.field.name,
            model.email.field.name,
        )


class CustomUserChangeForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChangeForm.Meta):
        fields = (
            users.models.User.email.field.name,
            users.models.User.username.field.name,
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
        )


class ProfileForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_name = users.models.Profile.coffee_count.field.name
        self.fields[field_name].disabled = True
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = users.models.Profile
        fields = [
            model.birthday.field.name,
            model.image.field.name,
            model.coffee_count.field.name,
        ]


class UserProfileForm(MultiModelForm):
    form_classes = {
        "user": CustomUserChangeForm,
        "profile": ProfileForm,
    }
