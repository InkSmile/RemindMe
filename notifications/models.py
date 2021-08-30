from django.db import models


class Email(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='user')
    email = models.CharField(max_length=50)

    class Meta:
        db_table = 'email_list'
