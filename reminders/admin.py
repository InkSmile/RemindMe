from django.contrib import admin

from reminders import models

@admin.register(models.Reminders)
class RemindersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'created_at', 'description')
    #list_filter = ('',)
    search_fields = ('name',)

@admin.register(models.RemindersCategory)
class RemindersCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'public_date', 'user', 'id')
    search_fields = ('title',)
