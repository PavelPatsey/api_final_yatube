from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Comment, Post, User


class CommentViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testusername")
        cls.post = Post.objects.create(
            text="test text 1",
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            author=cls.user,
            post=cls.post,
            text="test comment text",
        )
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_comments_get_200(self):
        """Получение комментариев. 200 Получение комментариев"""
        url = f"/api/v1/posts/{self.post.id}/comments/"
        Comment.objects.create(
            author=self.user,
            post=self.post,
            text="test comment text 2",
        )
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)
        self.assertEqual(len(response.json()), 2)

    def test_comments_get_404(self):
        """Получение комментариев. 404 Получение списка комментариев к
        несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/comments/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_comments_post_200_1(self):
        """Добавление комментария. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/"
        comment_count = Comment.objects.count()
        data = {"text": "test comment text"}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(Comment.objects.count(), comment_count + 1)

    def test_comments_post_200_2(self):
        """Добавление комментария. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/"
        comment_count = Comment.objects.count()
        data = {"text": "test comment text", "post": self.post.id}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(Comment.objects.count(), comment_count + 1)

    def test_comment_post_200_3(self):
        """Добавление комментария. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/"
        comment_count = Comment.objects.count()
        data = {
            "author": self.user.id,
            "text": "test comment text",
            "post": self.post.id,
        }
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.json()), dict)
        self.assertEqual(Comment.objects.count(), comment_count + 1)

    def test_comment_post_400(self):
        """Добавление комментария. 400 Отсутствует обязательное поле в теле
        запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/"
        data = {}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"text": ["Обязательное поле."]})

    def test_comments_post_401(self):
        """Добавление комментария. 401 Запрос от имени анонимного
        пользователя"""
        url = f"/api/v1/posts/{self.post.id}/comments/"
        data = {"text": "test comment text"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = "Учетные данные не были предоставлены."
        self.assertEqual(response.json(), {"detail": detail})

    def test_comments_post_404(self):
        """Добавление комментария. 404 Попытка добавить комментарий к
        несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/comments/"
        data = {"text": "test comment text"}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_comments_details_get_200(self):
        """Получение комментария. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("text"), "test comment text")

    def test_comments_details_get_404(self):
        """Получение комментария. 404 Попытка запросить несуществующий
        комментарий или к несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/comments/{self.comment.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comments_put_200(self):
        """Обновление комментария. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        response = self.authorized_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get("text"), "updated test comment text"
        )

    def test_comments_put_400(self):
        """Обновление комментария. 400 Отсутствует обязательное поле в теле
        запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        data = {}
        response = self.authorized_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"text": ["Обязательное поле."]})

    def test_comments_put_401(self):
        """Обновление комментария. 401 Запрос от имени анонимного
        пользователя"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        response = self.guest_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = "Учетные данные не были предоставлены."
        self.assertEqual(response.json(), {"detail": detail})

    def test_comments_put_403(self):
        """Обновление комментария. 403 Попытка изменения чужого контента"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        user_2 = User.objects.create_user(username="testusername_2")
        authorized_client_2 = APIClient()
        authorized_client_2.force_authenticate(user_2)
        response = authorized_client_2.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        detail = "У вас недостаточно прав для выполнения данного действия."
        self.assertEqual(response.json(), {"detail": detail})

    def test_comments_put_404(self):
        """Обновление комментария. 404 Попытка изменить несуществующий
        комментарий или к несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        response = self.authorized_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id + 1}/"
        response = self.authorized_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_comments_patch_200(self):
        """Частичное обновление комментария. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        response = self.authorized_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get("text"), "updated test comment text"
        )

    def test_comments_patch_401(self):
        """Частичное обновление комментария. 401 Запрос от имени анонимного
        пользователя"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        response = self.guest_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = "Учетные данные не были предоставлены."
        self.assertEqual(response.json(), {"detail": detail})

    def test_comments_patch_403(self):
        """Частичное обновление комментария. 403 Попытка изменения чужого
        контента"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        user_2 = User.objects.create_user(username="testusername_2")
        authorized_client_2 = APIClient()
        authorized_client_2.force_authenticate(user_2)
        response = authorized_client_2.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        detail = "У вас недостаточно прав для выполнения данного действия."
        self.assertEqual(response.json(), {"detail": detail})

    def test_comments_patch_404(self):
        """Частичное обновление комментария. 404 Попытка изменить несуществующий
        комментарий или к несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        response = self.authorized_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id + 1}/"
        response = self.authorized_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_comments_delete_200(self):
        """Удаление комментария. 204 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comments_delete_401(self):
        """Удаление комментария. 401 Запрос от имени анонимного
        пользователя"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = "Учетные данные не были предоставлены."
        self.assertEqual(response.json(), {"detail": detail})

    def test_comments_delete_403(self):
        """Удаление комментария. 403 Попытка изменения чужого контента"""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        testuser_2 = User.objects.create_user(username="testusername_2")
        authorized_client_2 = APIClient()
        authorized_client_2.force_authenticate(user=testuser_2)
        response = authorized_client_2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        detail = "У вас недостаточно прав для выполнения данного действия."
        self.assertEqual(response.json(), {"detail": detail})

    def test_comments_delete_404(self):
        """Удаление комментария. 403 Попытка удалить несуществующий
        комментарий или к несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/comments/{self.comment.id}/"
        data = {"text": "updated test comment text"}
        response = self.authorized_client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id + 1}/"
        data = {"text": "updated test comment text"}
        response = self.authorized_client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_comments_serializer(self):
        """Проверка работы CommentSerializer."""
        url = f"/api/v1/posts/{self.post.id}/comments/{self.comment.id}/"
        response = self.authorized_client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["text"], "test comment text")
        self.assertEqual(response.json()["author"], "testusername")
