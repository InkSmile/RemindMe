import datetime
import csv

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from reminders.serializers import RemindersSerializer, RemindersCategorySerializer
from reminders.models import Reminders, RemindersCategory
from reminders.filters import RemindersFilter, RemindersCategoryFilter

from django.http import HttpResponse


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

    @action(methods=['GET'], url_path='export-csv', detail=False)
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Reminders'+str(datetime.datetime.now())+'csv'

        writer = csv.writer(response)
        writer.writerow(['reminder', 'description', 'category'])

        reminders = Reminders.objects.filter(user=self.request.user)

        for reminder in reminders:
            writer.writerow([reminder.reminder, reminder.description, reminder.category])

        return response


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

