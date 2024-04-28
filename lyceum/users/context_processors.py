from django.utils import timezone

from users.models import Profile, User

__all__ = []


def users_birthday(request):
    today = timezone.now().date()
    return {
        "birthdays": User.objects.active()
        .filter(
            profile__birthday__day=today.day,
            profile__birthday__month=today.month,
        )
        .only(
            User.username.field.name,
            User.email.field.name,
            f"{User.profile.related.name}__{Profile.id.field.name}",
        ),
    }
