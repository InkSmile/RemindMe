from django.urls import path
from rest_framework.routers import SimpleRouter

from reminders import views
from reminders.views import RemindersViewSet

app_name = 'reminders'

router = SimpleRouter(trailing_slash=True)

# Pay attention on how SimpleRouter creates revers names for URLs.
# For list-like actions the url name is ``basename``-list;
# For detail-like ones this is ``basename``-detail with args <pk>
#
# So, for Premier endpoint it will be
# List: GET /v1/premiers/ - reverse('v1:premiers:premiers-list')
# Create: POST /v1/premiers/ - revers('v1:premiers:premiers-list')
router.register('', views.RemindersViewSet, basename='reminders')
router.register('', views.RemindersCategoryViewSet, basename='reminders_category')

urlpatterns = [

] + router.urls