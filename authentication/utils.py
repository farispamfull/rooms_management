from django.contrib.auth import user_logged_out, logout
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


def logout_user(request):
    request.user.auth_token.delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    logout(request)
