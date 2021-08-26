from django.test import TestCase
from user_profile.tests import BaseAPITest
from django.utils import timezone
from reminders.models import Reminders
from rest_framework import status
from rest_framework.reverse import reverse




class TestRemindersViewSet(BaseAPITest):

    def setUp(self):
        self.password = '1234'
        self.user = self.create_and_login(password=self.password)
        self.data = {"email": "hello@gmail.com"}
        self.user.save()

    def test_list_reminders(self):
        response = self.client.get(reverse('v1:reminders:reminders-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_reminders(self):
        pass

    def test_create_reminders(self):
        pass

    def test_create_validation_error(self):
        pass

    def test_update(self):
        pass

    def test_update_validation_error(self):
        pass

    def test_update_reminders_different_user(self):
        pass

    def test_destroy(self):
        pass

    def test_destroy_reminders_different_user(self):
        pass

    def test_unauthorized(self):
        pass
