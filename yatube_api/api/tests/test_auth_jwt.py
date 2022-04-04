from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import User


class AuthJWTTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testusername", password="testpassword"
        )
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_jwt_token(self):
        """Тест: Получить JWT-токен"""
        url = "/api/v1/jwt/create/"
        data = {"username": "testusername", "password": "testpassword"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(len(response.json()), 2)
        self.assertTrue("refresh" in response.json())
        self.assertTrue("access" in response.json())

    def test_update_jwt_token(self):
        """Тест: Обновить JWT-токен"""
        url_create = "/api/v1/jwt/create/"
        data = {"username": "testusername", "password": "testpassword"}
        response = self.guest_client.post(url_create, data)
        refresh_token = response.json().get("refresh")
        url_refresh = "/api/v1/jwt/refresh/"
        data = {"refresh": refresh_token}
        response = self.authorized_client.post(url_refresh, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(len(response.json()), 1)
        self.assertTrue("access" in response.json())

    def test_check_jwt_token(self):
        """Тест: Проверить JWT-токен"""
        url_create = "/api/v1/jwt/create/"
        data = {"username": "testusername", "password": "testpassword"}
        response = self.guest_client.post(url_create, data)
        access_token = response.json().get("refresh")
        url_check = "/api/v1/jwt/verify/"
        data = {"token": access_token}
        response = self.authorized_client.post(url_check, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(len(response.json()), 0)
        data = {}
        response = self.authorized_client.post(url_check, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"token": ["Обязательное поле."]})
        data = {"token": "invalid_token"}
        response = self.authorized_client.post(url_check, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid",
            },
        )
