from rest_framework import serializers
from reminders.models import Reminders, RemindersCategory

from notifications.tasks import send_email


class RemindersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminders
        fields = ("id", "reminder", "description", "category", "created_at", "remind_at")
        read_only_field = ("id", "create_at")

    def create(self, validated_data):
        new_reminder = super().create(validated_data)

        user = self.context['request'].user
        reminder = new_reminder.reminder
        category = new_reminder.category
        description = new_reminder.description
        remind_at = new_reminder.remind_at
        context = {
            'email': user.email,
            'title': reminder,
            'category': {'name': category.name, 'id': category.id},
            'description': description
        }

        template = 'notifications/remind_user.html'
        send_email.apply_async(
            (
                'Your Reminder from RemindMe',
                template,
                [user.email],
                context
            ),
            eta=remind_at
        )

        return new_reminder


class RemindersCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RemindersCategory
        fields = ("id", "name",)
        read_only_field = ("id", )