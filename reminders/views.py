from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from reminders.serializers import RemindersSerializer, RemindersCategorySerializer
from reminders.models import Reminders, RemindersCategory
from reminders.filters import RemindersFilter, RemindersCategoryFilter


class RemindersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = RemindersSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = RemindersFilter
    search_fields = ['reminder', 'description']

    def get_queryset(self):
        return Reminders.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RemindersCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = RemindersCategorySerializer
    filterset_class = RemindersCategoryFilter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['name']

    def get_queryset(self):
        return RemindersCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

