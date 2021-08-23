from rest_framework import serializers
from authentication.validators import ValidatePathSerializerMixin, ValidateEmailSerializerMixin
from authentication.models import User
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from authentication.tokens import TokenGenerator

class SignUpSerializer(ValidatePathSerializerMixin, ValidateEmailSerializerMixin, serializers.ModelSerializer):

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

class ActivationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data['token']
        error = f"Provided activation token '{token}' is not valid"
        try:
            uid, token = token.split('.')
            uid = force_text(urlsafe_base64_decode(uid))
        except (TypeError, ValueError):
            raise ValidationError(error)
        try:
            user = User.objects.get(email=uid)
        except User.DoesNotExist:
            raise ValidationError(error)

        if not TokenGenerator.check_token(user, token):
            raise ValidationError(error)

        data['email'] = uid
        return data

    def activate_user(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.save()