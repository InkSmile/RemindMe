from django.test import TestCase
from user_profile.tests import BaseAPITest
from django.utils import timezone
from reminders.models import Reminders, RemindersCategory
from authentication.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from mixer.backend.django import mixer


class TestRemindersViewSet(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.reminder_category = mixer.blend(RemindersCategory)
        self.Reminders = mixer.blend(Reminders, user=self.user, category=self.reminder_category)

    def test_list_reminders(self):
        response = self.client.get(reverse('v1:reminders-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.reminder.id)

    def test_create_reminders(self):
        data = {
            'reminder': 'something',
            'description': 'test',
            'category': self.reminder_category.id
        }
        response = self.client.post(reverse('v1:reminders-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reminders.objects.count(), 2)
        self.assertTrue(Reminders.objects.filter(pk=response.data['id']).exists())

    def test_create_validation_error(self):
        data = {
            'reminder': None,
            'descriptino': 'sometug',
            'category': 'vbjnjnkj'
        }
        response = self.client.post(reverse('v1:reminders-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        data = {
            'reminder': 'test update',
            'description': 'testudpdate',
            'category': self.reminder_category.id
        }
        resp = self.client.delete(reverse('v1:notes-detail', args=(self.reminder.id,)))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


    def test_update_validation_error(self):
        data = {
            'reminder': 'test update',
            'description': 'testudpdate',
            'category': self.reminder_category.id
        }
        resp = self.client.delete(reverse('v1:notes-detail', args=(self.reminder.id,)))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_reminders_different_user(self):
        user = mixer.blend(User)
        self.reminder.user = user
        self.reminder.save()
        resp = self.client.delete(reverse('v1:notes-detail', args=(self.reminder.id,)))
        self.assertEqual(resp.status_code, 404)

    def test_delete(self):
        response = self.client.delete(reverse('v1:reminders-detail', args=(self.reminder.id,)))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Reminders.objects.count(), 0)

    def test_delete_reminders_different_user(self):
        user = mixer.blend(User)
        self.reminder.user = user
        self.reminder.save()
        resp = self.client.delete(reverse('v1:notes-detail', args=(self.reminder.id,)))
        self.assertEqual(resp.status_code, 404)

    def test_unauthorized(self):
        self.logout()
        data = {
            'reminder': 'test'
        }
        response = self.client.post(reverse('v1:notes-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
