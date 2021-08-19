from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User

class TestObtainTokenPair(APITestCase):

    def setUp(self):
        self.email = 'test@test.com'
        self.username = 'test'
        self.password = 'Secure123'
        self.user = User.objects.create_user(self.email, self.username, self.password)

    def test_auth(self):
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(reverse('v1:authentication:obtain'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_auth_wrong_pass(self):
        data = {'email': self.email, 'password': 'wrong_password'}
        response = self.client.post(reverse('v1:authentication:obtain'), data=data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_wrong_email(self):
        data = {'email': 'wrong_email', 'password': self.password}
        response = self.client.post(reverse('v1:authentication:obtain'), data=data)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

