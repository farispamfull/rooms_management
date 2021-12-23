from django.contrib.auth import user_logged_out
from django.utils.timezone import now
from rest_framework.authtoken.models import Token


def login_user(request, user):
    token, _ = Token.objects.get_or_create(user=user)
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    user.last_login = now()
    user.save()
    return token
