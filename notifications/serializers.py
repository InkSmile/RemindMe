from rest_framework import serializers

from notifications.models import Email


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ('id', 'user', 'email')
        read_only_field = ('id', 'user',)