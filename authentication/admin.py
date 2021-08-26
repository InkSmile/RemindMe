from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from authentication.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'created_at', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'last_login')

    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)
