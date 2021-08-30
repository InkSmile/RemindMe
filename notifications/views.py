from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from notifications.serializers import EmailSerializer
from notifications.models import Email
from authentication.models import User


class EmailView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = EmailSerializer

    def get_queryset(self):
        return Email.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = self.request.data['email']
        if User.objects.filter(email=email).exists():
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

