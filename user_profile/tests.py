from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
from authentication.models import User


class BaseAPITest(APITestCase):

    def create(self, email='test@mail.com', password='testpassword'):
        user = User.objects.create_user(email=email, password=password)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_and_login(self, email='test@mail.com', password='testpassword'):
        user = self.create(email=email, password=password)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)

class TestProfileViewSet(BaseAPITest):

    def setUp(self):
        self.password = 'testpassword'
        self.user = self.create_and_login(password=self.password)
        self.data = {
            "email": "new@email.com",
        }

    def test_get_profile(self):
        response = self.client.get(reverse('v1:user_profile:profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_profile_unauthorized(self):
        self.logout()
        response = self.client.get(reverse('v1:user_profile:profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password(self):
        data = {
            "old_password": self.password,
            "password": "newpass123",
        }
        response = self.client.post(reverse('v1:user_profile:password-change'), data=data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(check_password(data['password'], self.user.password))

    def test_change_password_wrong_old_password(self):
        data = {
            "old_password": self.password + 'some_str',
            "password": "newpass123"
        }
        response = self.client.post(reverse('v1:user_profile:password-change'), data=data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(check_password(data['password'], self.user.password))

    def test_change_email(self):
        data = {
            "email": "test442@mail.com",
            "path": "change/email",
        }
        response = self.client.patch(reverse('v1:user_profile:email'), data=data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, data['email'])
        self.assertEqual(response.data['email'], data['email'])

    def test_email_already_exists(self):
        data = {
            "email": "test1@email.com",
        }
        #self.create(email=data['email'])
        response = self.client.patch(reverse('v1:user_profile:email'), data=data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.user.email, data['email'])

    def test_email_uppercase_already_exists(self):
        email = "test453211@mail.com"
        #self.create(email=email)
        response = self.client.patch(reverse('v1:user_profile:email'), data={"email": email.upper()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, email)

    def test_deactivate_user_profile(self):
        response = self.client.post(reverse('v1:user_profile:deactivate'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)