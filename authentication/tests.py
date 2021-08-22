from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User

from django.utils import timezone
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from unittest.mock import patch


# --------------------------------------------
class BaseAPITest(APITestCase):

    def create(self, email='test@mail.com', password='test_password'):  # nosec
        user = User.objects.create_user(email=email, password=password)
        user.last_login = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_and_login(self, email='test@mail.com', password='test_password'):  # nosec
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
# --------------------------------------------


# Authentication
class TestObtainTokenPair(APITestCase):
    def setUp(self):
        self.email = 'test@test.com'
        self.password = 'Secure123'
        self.user = User.objects.create_user(self.email, self.password)

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


class TestObtainJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "test@mail.com"
        self.password = "test_password"
        self.user = self.create(email=self.email, password=self.password)

    def test_get_token_pair(self):
        resp = self.client.post(reverse('v1:authentication:obtain'), data={'email': self.email, 'password': self.password})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('refresh', resp.data)
        self.assertIn('access', resp.data)

    def test_get_token_authentication_error(self):
        resp = self.client.post(reverse('v1:authentication:obtain'), data={'email': 'fake_data', 'password': 'fake_data'})
        self.assertEqual(resp.status_code, 401)


class TestVerifyJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "test@mail.com"
        self.password = "test_password"
        self.user = self.create(email=self.email, password=self.password)
        self.access_token = str(AccessToken.for_user(self.user))

    def test_token_is_valid(self):
        resp = self.client.post(reverse('v1:authentication:verify'), data={'token': self.access_token})
        self.assertEqual(resp.status_code, 200)

    def test_get_token_validation_error(self):
        resp = self.client.post(reverse('v1:authentication:verify'), data={'token': 'fake_data'})
        self.assertEqual(resp.status_code, 401)


class TestRefreshJSONWebTokenView(BaseAPITest):

    def setUp(self):
        self.email = "test@mail.com"
        self.password = "test_password"
        self.user = self.create(email=self.email, password=self.password)
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_get_access_token(self):
        resp = self.client.post(reverse('v1:authentication:refresh'), data={'refresh': self.refresh_token})
        self.assertIn('access', resp.data)

    def test_get_token_refresh_error(self):
        resp = self.client.post(reverse('v1:authentication:refresh'), data={'refresh': 'fake_data'})
        self.assertEqual(resp.status_code, 401)


# SignUp
class TestSignUpView(BaseAPITest):

    def setUp(self):
        self.data = {
            "email": "test@test.com",
            "password": "testpassword123",
            "path": "/activate/",
        }


    @patch('notifications.tasks.send_email.delay')
    def test_sign_up(self, email_delay):
        resp = self.client.post(reverse('v1:authentication:sign-up'), data=self.data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(email=self.data['email']).exists())
        email_delay.assert_called_once()


    @patch('notifications.tasks.send_email.delay')
    def test_sign_up_email_to_lower_case(self, email_delay):
        self.data['email'] = 'CAPs@mail.com'
        resp = self.client.post(reverse('v1:authentication:sign-up'), data=self.data)

        self.assertEqual(resp.status_code, 201)
        self.assertTrue(User.objects.filter(email=self.data['email'].lower(),).exists())
        email_delay.assert_called_once()

    def test_sign_up_user_exists(self):
        email = 'test@test.com'
        self.create(email=email)
        self.data['email'] = email
        resp = self.client.post(reverse('v1:authentication:sign-up'), data=self.data)
        self.assertEqual(resp.status_code, 400)