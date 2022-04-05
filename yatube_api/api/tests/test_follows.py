from django.test import TestCase
from posts.models import Follow, User
from rest_framework import status
from rest_framework.test import APIClient


class FollowViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testusername")
        cls.author = User.objects.create_user(username="testauthorname")
        cls.follow = Follow.objects.create(
            user=cls.user,
            following=cls.author,
        )
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_follow_list_200(self):
        """Возвращает все подписки пользователя, сделавшего запрос."""
        url = "/api/v1/follow/"
        Follow.objects.create(
            user=self.author,
            following=self.user,
        )
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["user"], "testusername")
        self.assertEqual(response.json()[0]["following"], "testauthorname")

    def test_get_follow_list_401(self):
        """Подписки. 401 Запрос от имени анонимного пользователя."""
        url = "/api/v1/follow/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = "Учетные данные не были предоставлены."
        self.assertEqual(response.json(), {"detail": detail})

    def test_post_follow_list_201(self):
        """Подписка. 201 Удачное выполнение запроса."""
        url = "/api/v1/follow/"
        author_2 = User.objects.create_user(username="testauthorname2")
        data = {"following": author_2.username}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.json()), list)
        self.assertEqual(len(response.json()), 2)
