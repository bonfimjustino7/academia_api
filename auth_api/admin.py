from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserCustom


@admin.register(UserCustom)
class UserAdmin(UserAdmin):
    pass


admin.site.site_header = 'Academia ADMIN'
admin.site.site_title = 'Academia ADMIN'
