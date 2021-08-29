from django_filters import rest_framework as filters
from reminders.models import Reminders, RemindersCategory


class RemindersFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category')
    ordering = filters.OrderingFilter(fields={
        'reminder': 'reminder',
        'created_at': 'create_date',
        'category': 'category'
    })

    class Meta:
        model = Reminders
        fields = ('category', 'reminder', 'ordering')


class RemindersCategoryFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category')

    ordering = filters.OrderingFilter(fields={'id': 'order_id'})

    class Meta:
        model = RemindersCategory
        fields = ('name', 'ordering')


