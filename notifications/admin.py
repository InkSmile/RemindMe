from django.contrib import admin

from notifications.models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email')
    search_fields = ('email',)
