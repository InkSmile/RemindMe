from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from authentication.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'created_at', 'last_login', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'last_login')

    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)
