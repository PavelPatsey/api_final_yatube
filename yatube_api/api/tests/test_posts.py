from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Post, User


class PostViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testusername")
        cls.post = Post.objects.create(
            text="test text 1",
            author=cls.user,
        )
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_post_list(self):
        """Получение публикаций
        Удачное выполнение запроса без пагинации
        """
        url = "/api/v1/posts/"
        Post.objects.create(
            text="test text 2",
            author=self.user,
        )
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)
        self.assertEqual(len(response.json()), 2)

    def test_post_create(self):
        """Создание публикации.
        201 удачное выполнение запроса
        """
        url = "/api/v1/posts/"
        data = {"text": "test text"}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # def test_post_get_request(self):
    #     """Тестируем получение публикации по id."""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     response = self.authorized_client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_non_existent_post_get_request(self):
    #     """Тестируем попытку запроса несуществующего поста"""
    #     url = f"/api/v1/posts/{self.post.id + 1}/"
    #     response = self.authorized_client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_post_patch(self):
    #     """Частичное обновление публикации"""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     data = {"text": "patched test text 1"}
    #     response = self.authorized_client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.json()["text"], "patched test text 1")
    #     test_post = Post.objects.get(id=1)
    #     self.assertEqual(test_post.text, "patched test text 1")
    
    # asdd

    
    # def test_post_get_request_by_unauthorized_user(self):
    #     """Тестируем get запрос поста неавторизованным пользователем"""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     response = self.guest_client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    

    # def test_post_create_by_anonymous(self):
    #     """Анонимный пользователь не может создать пост"""
    #     url = "/api/v1/posts/"
    #     data = {"text": "test text"}
    #     response = self.guest_client.post(url, data, format="json")
    #     self.assertEqual(
    #         response.json(),
    #         {"detail": "Учетные данные не были предоставлены."},
    #     )

    # def test_post_delete(self):
    #     """Удаляем пост"""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     post_count = Post.objects.count()
    #     response = self.authorized_client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Post.objects.count(), post_count - 1)

    

    # def test_post_patch_by_not_author(self):
    #     """Редактирование поста не автором запрещена"""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     testuser_2 = User.objects.create_user(username="testusername_2")
    #     authorized_client_2 = APIClient()
    #     authorized_client_2.force_authenticate(user=testuser_2)
    #     data = {"text": "patched test text 1"}
    #     response = authorized_client_2.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_post_delete_by_not_author(self):
    #     """Удаление поста не автором запрещена"""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     testuser_2 = User.objects.create_user(username="testusername_2")
    #     authorized_client_2 = APIClient()
    #     authorized_client_2.force_authenticate(user=testuser_2)
    #     response = authorized_client_2.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_post_serializer(self):
    #     """Проверка работы post сериализатора."""
    #     url = f"/api/v1/posts/{self.post.id}/"
    #     response = self.authorized_client.patch(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.json()["text"], "test text 1")
    #     self.assertEqual(response.json()["author"], "testusername")
