from rest_framework import serializers
from authentication.validators import ValidatePathSerializerMixin, ValidateEmailSerializerMixin
from authentication.models import User

class SignUpSerializer(ValidatePathSerializerMixin, ValidateEmailSerializerMixin, serializers.ModelSerializer):
    """Create new user when sign up.
    Note! Password should always be write only!
    You may be interested what is the ``path`` field.
    Usually, we use it when we need to send an email to user
    and we include this path/ to FE endpoint to handle
    further user's activation.
    """
    password = serializers.CharField(write_only=True)
    path = serializers.RegexField(regex=r'[a-zA-Z0-9_\-\/]+', required=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "path",)
        read_only_fields = ("id",)
        write_only_fields = ("password", "path",)

    def create(self, validated_data):
        exclude = {'path', 'captcha'}
        vd = {k: v for k, v in validated_data.items() if k not in exclude}  # ???
        return User.objects.create_user(**vd)