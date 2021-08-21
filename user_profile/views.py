from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from authentication.models import User
from user_profile import serializers
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated



class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user

    @action(methods=['POST'], detail=False)
    def change_password(self, *args, **kwargs):
        user = self.get_object()
        serializer = serializers.UserProfilePasswordChangeSerializer(instance=user, data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(methods=['PATCH'], detail=False)
    def change_email(self, *args, **kwargs):
        user = self.get_object()
        serializer = serializers.UserEmailSerializer(instance=user, data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def deactivate(self, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)