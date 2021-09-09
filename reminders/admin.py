from django.contrib import admin

from reminders import models


@admin.register(models.Reminders)
class RemindersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reminder', 'created_at', 'remind_at','category', 'description')
    search_fields = ('reminder',)


@admin.register(models.RemindersCategory)
class RemindersCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
