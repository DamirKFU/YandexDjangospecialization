import django.views.generic

__all__ = []


class DescriptionTemplateView(django.views.generic.TemplateView):
    template_name = "about/description.html"
