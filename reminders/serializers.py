from rest_framework import serializers
from reminders.models import Reminders, RemindersCategory


class RemindersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminders
        fields = ("id", "user", "name", "description", "created_at")
        read_only_field = ("id", "create_at")

class RemindersCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RemindersCategory
        fields = ("id", "user", "title", "body", "public_date")
        read_only_field = ("id", "public_date")