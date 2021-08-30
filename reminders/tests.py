from Reminder.tests import BaseAPITest
from reminders.models import Reminders, RemindersCategory
from authentication.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from mixer.backend.django import mixer
from django.urls import reverse
from unittest.mock import patch
from django.utils import timezone


class TestRemindersViewSet(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.reminder_category = mixer.blend(RemindersCategory, user=self.user)
        self.reminder = mixer.blend(Reminders, user=self.user, category=self.reminder_category)

    def test_list_reminders(self):
        response = self.client.get(reverse('v1:reminders:reminders-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.reminder.id)

    def test_create_reminders(self):
        data = {
            'reminder': 'something',
            'description': 'test',
            'category': self.reminder_category.id,
            "remind_at": timezone.now()

        }
        response = self.client.post(reverse('v1:reminders:reminders-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reminders.objects.count(), 2)
        self.assertTrue(Reminders.objects.filter(pk=response.data['id']).exists())

    def test_create_validation_error(self):
        data = {
            'reminder': None,
            'description': 'sometug',
            'category': 'vbjnjnkj',
            "remind_at": timezone.now()
        }
        response = self.client.post(reverse('v1:reminders:reminders-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        data = {
            'reminder': 'tetssomer',
            'description': 'test description',
            'category': self.reminder_category.id,
            "remind_at": timezone.now()
        }
        response = self.client.put(reverse('v1:reminders:reminders-detail', args=(self.reminder.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_validation_error(self):
        data = {
            'reminder': None,
            'description': 'testudpdate',
            'category': self.reminder_category.id,
            "remind_at": timezone.now()
        }
        resp = self.client.put(reverse('v1:reminders:reminders-detail', args=(self.reminder.id,)), data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_reminders_different_user(self):
        user = mixer.blend(User)
        self.reminder.user = user
        self.reminder.save()
        resp = self.client.put(reverse('v1:reminders:reminders-detail', args=(self.reminder.id,)))
        self.assertEqual(resp.status_code, 404)

    def test_delete(self):
        response = self.client.delete(reverse('v1:reminders:reminders-detail', args=(self.reminder.id,)))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Reminders.objects.count(), 0)

    def test_delete_reminders_different_user(self):
        user = mixer.blend(User)
        self.reminder.user = user
        self.reminder.save()
        resp = self.client.delete(reverse('v1:reminders:reminders-detail', args=(self.reminder.id,)))
        self.assertEqual(resp.status_code, 404)

    def test_unauthorized(self):
        self.logout()
        data = {
            'reminder': 'test'
        }
        response = self.client.post(reverse('v1:reminders:reminders-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_reminders_category(self):
        response = self.client.get(reverse('v1:reminders:reminders_category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.reminder_category.id)

    def test_create_reminders_category(self):
        data = {
            'name': 'test'
        }
        response = self.client.post(reverse('v1:reminders:reminders_category-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RemindersCategory.objects.count(), 2)
        self.assertTrue(RemindersCategory.objects.filter(pk=response.data['id']).exists())

    def test_create_category_validation_error(self):
        data = {
            'reminder': None
        }
        response = self.client.post(reverse('v1:reminders:reminders_category-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_update(self):
        data = {
            'name': 'update_test'
        }
        response = self.client.put(reverse('v1:reminders:reminders_category-detail', args=(self.reminder_category.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_validation_error(self):
        data = {
            'name': None
        }
        resp = self.client.put(reverse('v1:reminders:reminders_category-detail', args=(self.reminder_category.id,)), data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_reminders_category_different_user(self):
        user = mixer.blend(User)
        self.reminder_category.user = user
        self.reminder_category.save()
        resp = self.client.put(reverse('v1:reminders:reminders_category-detail', args=(self.reminder_category.id,)))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_delete(self):
        response = self.client.delete(reverse('v1:reminders:reminders_category-detail', args=(self.reminder_category.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RemindersCategory.objects.count(), 0)

    def test_delete_reminders_category_different_user(self):
        user = mixer.blend(User)
        self.reminder_category.user = user
        self.reminder_category.save()
        resp = self.client.delete(reverse('v1:reminders:reminders_category-detail', args=(self.reminder_category.id,)))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_category_unauthorized(self):
        self.logout()
        data = {
            'name': 'test'
        }
        response = self.client.post(reverse('v1:reminders:reminders_category-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('notifications.tasks.send_email.apply_async')
    def test_send_reminder_email(self, email_apply_async):
        data = {
            "reminder": "Hi Jack!",
            "category": self.reminder_category.id,
            "description": "Hi!",
            "remind_at": timezone.now()
        }
        response = self.client.post(reverse("v1:reminders:reminders-list"), data=data)
        self.assertTrue(Reminders.objects.filter(id=response.data['id']).exists())
        self.assertEqual(response.status_code, 201)
        email_apply_async.assert_called_once()