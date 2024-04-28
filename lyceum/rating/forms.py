import django.forms

import rating.models

__all__ = []


class GradeForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_name = rating.models.Grade.grade.field.name
        self.fields[field_name].widget.attrs["class"] = "form-select"

    class Meta:
        model = rating.models.Grade
        fields = [
            model.grade.field.name,
        ]
