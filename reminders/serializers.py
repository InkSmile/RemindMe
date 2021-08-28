from rest_framework import serializers
from reminders.models import Reminders, RemindersCategory


class RemindersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminders
        fields = ("id", "reminder", "description", "category", "created_at")
        read_only_field = ("id", )


class RemindersCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RemindersCategory
        fields = ("id", "name",)
        read_only_field = ("id", )