import users.models

__all__ = []


class UserProxyRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            request.user = users.models.User.objects.get(
                pk=request.user.id,
            )

        return self.get_response(request)
