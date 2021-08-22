from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from user_profile import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated



class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user



    @swagger_auto_schema(request_body=serializers.UserProfilePasswordChangeSerializer)
    @action(methods=['POST'], detail=False)
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = serializers.UserProfilePasswordChangeSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            if not user.check_password(serializer.data.get('old password')):
                return Response({'old password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('password'))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def change_password(self, *args, **kwargs):
    #     user = self.get_object()
    #     serializer = serializers.UserProfilePasswordChangeSerializer(data=self.request.data, context={'request': self.request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


    @swagger_auto_schema(request_body=serializers.UserEmailSerializer)
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