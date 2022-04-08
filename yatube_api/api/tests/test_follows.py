from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Follow, User


class FollowViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testusername")
        cls.following = User.objects.create_user(username="testfollowing")
        Follow.objects.create(
            user=cls.user,
            following=cls.following,
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
        following_2 = User.objects.create_user(username="testfollowingname_2")
        Follow.objects.create(
            user=self.user,
            following=following_2,
        )
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["user"], "testusername")
        self.assertEqual(response.json()[0]["following"], "testfollowing")
        self.assertEqual(response.json()[1]["user"], "testusername")
        self.assertEqual(
            response.json()[1]["following"], "testfollowingname_2"
        )

    def test_get_follow_list_401(self):
        """Подписки. 401 Запрос от имени анонимного пользователя."""
        url = "/api/v1/follow/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = "Учетные данные не были предоставлены."
        self.assertEqual(response.json(), {"detail": detail})

    def test_post_follow_201(self):
        """Подписка. 201 Удачное выполнение подписки."""
        url = "/api/v1/follow/"
        follow_count = Follow.objects.count()
        User.objects.create_user(username="testauthorname2")
        data = {"following": "testauthorname2"}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(
            response.json(),
            {"user": "testusername", "following": "testauthorname2"},
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)

    def test_post_follow_400(self):
        """Подписка. 400 Отсутствует обязательное поле в теле запроса или оно
        не соответствует требованиям"""
        url = "/api/v1/follow/"
        data = {}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(response.json()["following"], ["Обязательное поле."])

    def test_post_follow_401(self):
        """Подписка. 401 Запрос от имени анонимного пользователя"""
        url = "/api/v1/follow/"
        User.objects.create_user(username="testauthorname2")
        data = {"following": "testauthorname2"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = "Учетные данные не были предоставлены."
        self.assertEqual(response.json(), {"detail": detail})

    def test_post_follow_400_unable_to_re_follow_author(self):
        """Подписка. 400 Нельзя повторно подписаться на автора"""
        url = "/api/v1/follow/"
        follow_count = Follow.objects.count()
        data = {"following": "testfollowing"}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(follow_count, Follow.objects.count())
        test_json = {
            "non_field_errors": [
                "Поля user, following должны производить массив с "
                + "уникальными значениями."
            ]
        }
        self.assertEqual(response.json(), test_json)

    def test_post_follow_400_cant_subscribe_to_yourself(self):
        """Подписка. 400 Нельзя подписаться на самого себя."""
        url = "/api/v1/follow/"
        data = {"following": "testusername"}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_json = {"non_field_errors": ["You can't subscribe to yourself"]}
        self.assertEqual(response.json(), test_json)

    def test_follow_search_filter(self):
        """Проверка GET запроса с параметром `search`."""
        url = f"/api/v1/follow/?search={self.following.username}"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [{"user": "testusername", "following": "testfollowing"}],
        )
