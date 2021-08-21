from rest_framework import  serializers
from rest_framework.exceptions import ValidationError
from authentication.models import User

class ValidateEmailSerializerMixin:
    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise ValidationError('User with this email address already exists.')
        return value

class ValidatePathSerializerMixin:
    def validate_path(self, path):
        return path.strip('/')

class UserProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email')
        read_only_fields = ('id', 'email')

    # def validate_email(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value

    # def validate_username(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})
    #     return value

class UserProfilePasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        field = ('old password', 'password')

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('Wrong password')
        return value

    def save(self):
        password = self.validated_data['password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class UserEmailSerializer(ValidateEmailSerializerMixin, ValidatePathSerializerMixin, serializers.ModelSerializer):
    path = serializers.RegexField(regex=r'[a-zA-Z0-9_\-\/]+', required=True, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'path')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        instance.is_active = False
        return super().update(instance, validated_data)

    # def update(self, instance, validated_data):
    #     instance.email = validated_data['email']
    #     instance.username = validated_data['username']
    #     instance.save()
    #     return instance




