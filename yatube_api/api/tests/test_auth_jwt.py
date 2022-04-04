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

    def test_post_get_request(self):
        """Тестируем Получить JWT-токен"""
        url = "/api/v1/jwt/create/"
        data = {"username": "testusername", "password": "testpassword"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), dict)
        self.assertTrue("refresh" in response.json())
        self.assertTrue("access" in response.json())

    # def test_post_get_request(self):
    #     """Тестируем get запрос поста"""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     response = self.authorized_client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
