from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserChangeForm
from .models import User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    search_fields = ('email', 'username')


admin.site.register(User, MyUserAdmin)
