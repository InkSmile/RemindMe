from django.shortcuts import render
from reminders.serializers import RemindersSerializer, RemindersCategorySerializer
from reminders.models import Reminders, RemindersCategory

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

class RemindersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = RemindersSerializer

    def get_queryset(self):
        return Reminders.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RemindersCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = RemindersCategorySerializer

    def get_queryset(self):
        return RemindersCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# @api_view(['PUT'])
# def redminders_update(request, pk):
#     reminders = Reminders.objects.get(id=pk)
#     serializer = RemindersSerializer(instance=reminders, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
