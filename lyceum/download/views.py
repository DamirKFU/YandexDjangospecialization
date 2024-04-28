from pathlib import Path

from django.conf import settings
from django.http import FileResponse
import django.views.generic


__all__ = []


class DownloadView(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        return FileResponse(
            open(settings.MEDIA_ROOT / Path(kwargs.get("path")), "rb"),
            as_attachment=True,
        )
