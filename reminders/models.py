from django.db import models

class Reminders(models.Model):
    user = models.ForeignKey('authentication.User', models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reminders'


class RemindersCategory(models.Model):
    user = models.ForeignKey('authentication.User', models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    public_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reminders_category'
