from django.urls import path, include
from rest_framework.routers import SimpleRouter

from reminders import views


app_name = 'reminders'

router = SimpleRouter(trailing_slash=True)

router.register('category', views.RemindersCategoryViewSet, basename='reminders_category')
router.register('', views.RemindersViewSet, basename='reminders')

urlpatterns = router.urls