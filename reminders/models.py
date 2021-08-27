from django.db import models


class RemindersCategory(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='reminders_category')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'reminders_category'


class Reminders(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='reminders')
    reminder = models.CharField(max_length=255)
    category = models.ForeignKey(RemindersCategory, on_delete=models.CASCADE, related_name='reminders')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reminders'
