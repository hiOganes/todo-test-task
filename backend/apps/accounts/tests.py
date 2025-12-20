from rest_framework.test import (
    APIRequestFactory, APITestCase
)
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.accounts import views
from apps.common.data_tests import (
    test_user_register,
    test_user_login,
    test_user_login_ivalid_data,
)


class TestRegisterAPIView(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:register')
        self.view = views.RegisterAPIView.as_view()
        self.factory = APIRequestFactory()

    def test_register(self):
        users_before = get_user_model().objects.count()
        request = self.factory.post(self.url, test_user_register)
        response = self.view(request)
        users_after = get_user_model().objects.count()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(users_before < users_after)

    def test_register_invalid_email(self):
        test_user_register['email'] = 'invalid.inv'
        request = self.factory.post(self.url, test_user_register)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_password(self):
        test_user_register['password'] = '12345'
        request = self.factory.post(self.url, test_user_register)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_data(self):
        request = self.factory.post(self.url, {})
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCustomTokenObtainPairView(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:login')
        self.view = views.CustomTokenObtainPairView.as_view()
        self.factory = APIRequestFactory()
        get_user_model().objects.create_user(**test_user_register)

    def test_get_tokens(self):
        request = self.factory.post(self.url, test_user_login)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_tokens_invalid_user(self):
        request = self.factory.post(self.url, test_user_login_ivalid_data)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tokens_empty_user(self):
        request = self.factory.post(self.url, {})
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCustomTokenRefreshView(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:refresh')
        self.view = views.CustomTokenRefreshView.as_view()
        self.factory = APIRequestFactory()
        self.tokens = views.RegisterAPIView.as_view()(
            self.factory.post(reverse('accounts:register'), test_user_register)
        ).data

    def test_get_refresh_token(self):
        request = self.factory.post(
            self.url, {'refresh': self.tokens['refresh']}
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_refresh_token_invalid_data(self):
        request = self.factory.post(
            self.url, {'refresh': 'invalid_token'}
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_refresh_token_empty_data(self):
        request = self.factory.post(
            self.url, {}
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCustomTokenVerifyView(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:verify')
        self.view = views.CustomTokenRefreshView.as_view()
        self.factory = APIRequestFactory()
        self.tokens = views.RegisterAPIView.as_view()(
            self.factory.post(reverse('accounts:register'), test_user_register)
        ).data

    def test_get_verify_token(self):
        request = self.factory.post(
            self.url, {'refresh': self.tokens['refresh']}
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_verify_token_invalid_data(self):
        request = self.factory.post(
            self.url, {'refresh': 'invalid_token'}
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_verify_token_empty_data(self):
        request = self.factory.post(
            self.url, {}
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
