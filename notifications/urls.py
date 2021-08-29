from rest_framework.routers import SimpleRouter

from notifications.views import EmailView


app_name = 'notifications'

router = SimpleRouter(trailing_slash=True)
router.register('email', EmailView, basename='email')

urlpatterns = router.urls


