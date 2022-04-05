from django.test import TestCase
from posts.models import Post, User
from rest_framework import status
from rest_framework.test import APIClient

POST_AMOUNT_TO_CREATE = 10


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

    def test_post_create_400(self):
        """Создание публикации.
        400 Отсутствует обязательное поле в теле запроса
        """
        url = "/api/v1/posts/"
        data = {}
        response = self.authorized_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"text": ["Обязательное поле."]})

    def test_post_create_401(self):
        """Создание публикации.
        401 Запрос от имени анонимного пользователя.
        """
        url = "/api/v1/posts/"
        data = {"text": "test text"}
        response = self.guest_client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"detail": "Учетные данные не были предоставлены."},
        )

    def test_post_get_200(self):
        """Получение публикации
        200 Удачное выполнение запроса
        """
        url = f"/api/v1/posts/{self.post.id}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), dict)

    def test_post_get_non_existent_post(self):
        """Попытка запроса несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_post_get_request_by_unauthorized_user(self):
        """Тестируем get запрос поста неавторизованным пользователем"""
        url = f"/api/v1/posts/{self.post.id}/"
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_put_200(self):
        """Обновление публикации. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/"
        data = {
            "text": "patched test text 1",
        }
        response = self.authorized_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["text"], "patched test text 1")
        test_post = Post.objects.get(id=1)
        self.assertEqual(test_post.text, "patched test text 1")

    def test_post_put_400(self):
        """Обновление публикации. 400 Отсутствует обязательное поле в теле
        запроса"""
        url = f"/api/v1/posts/{self.post.id}/"
        data = {}
        response = self.authorized_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"text": ["Обязательное поле."]})

    def test_post_put_401(self):
        """Обновление публикации. 401 Учетные данные не были предоставлены."""
        url = f"/api/v1/posts/{self.post.id}/"
        data = {"text": "patched test text 1"}
        response = self.guest_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"detail": "Учетные данные не были предоставлены."},
        )

    def test_post_put_403(self):
        """Обновление публикации. 403 У вас недостаточно прав для выполнения
        данного действия."""
        url = f"/api/v1/posts/{self.post.id}/"
        user_2 = User.objects.create_user(username="testusername_2")
        authorized_client_2 = APIClient()
        authorized_client_2.force_authenticate(user_2)
        data = {
            "text": "patched test text 1",
        }
        response = authorized_client_2.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        detail = "У вас недостаточно прав для выполнения данного действия."
        self.assertEqual(response.json(), {"detail": detail})

    def test_post_put_404(self):
        """Обновление публикации. 404 Попытка изменения несуществующей
        публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/"
        data = {"text": "patched test text 1"}
        response = self.authorized_client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_post_patch_200(self):
        """Частичное обновление публикации. 200 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/"
        data = {"text": "patched test text 1"}
        response = self.authorized_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["text"], "patched test text 1")
        test_post = Post.objects.get(id=1)
        self.assertEqual(test_post.text, "patched test text 1")

    def test_post_patch_401(self):
        """Частичное обновление публикации. 401 Запрос от имени анонимного
        пользователя"""
        url = f"/api/v1/posts/{self.post.id}/"
        data = {"text": "patched test text 1"}
        response = self.guest_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"detail": "Учетные данные не были предоставлены."},
        )

    def test_post_patch_403(self):
        """Частичное обновление публикации. 403 Попытка изменения чужого
        контента"""
        url = f"/api/v1/posts/{self.post.id}/"
        testuser_2 = User.objects.create_user(username="testusername_2")
        authorized_client_2 = APIClient()
        authorized_client_2.force_authenticate(user=testuser_2)
        data = {"text": "patched test text 1"}
        response = authorized_client_2.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        detail = "У вас недостаточно прав для выполнения данного действия."
        self.assertEqual(response.json(), {"detail": detail})

    def test_post_patch_404(self):
        """Частичное обновление публикации. 404 Попытка изменения
        несуществующей публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/"
        data = {"text": "patched test text 1"}
        response = self.authorized_client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_post_delete_204(self):
        """Удаление публикации. 204 Удачное выполнение запроса"""
        url = f"/api/v1/posts/{self.post.id}/"
        post_count = Post.objects.count()
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), post_count - 1)

    def test_post_delete_401(self):
        """Удаление публикации. 401 Запрос от имени анонимного пользователя"""
        url = f"/api/v1/posts/{self.post.id}/"
        response = self.guest_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {"detail": "Учетные данные не были предоставлены."},
        )

    def test_post_delete_403(self):
        """Удаление публикации. 403 У вас недостаточно прав для выполнения
        данного действия."""
        url = f"/api/v1/posts/{self.post.id}/"
        testuser_2 = User.objects.create_user(username="testusername_2")
        authorized_client_2 = APIClient()
        authorized_client_2.force_authenticate(user=testuser_2)
        response = authorized_client_2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        detail = "У вас недостаточно прав для выполнения данного действия."
        self.assertEqual(response.json(), {"detail": detail})

    def test_post_delete_404(self):
        """Удаление публикации. 404 Попытка удаления несуществующей
        публикации"""
        url = f"/api/v1/posts/{self.post.id + 1}/"
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "Страница не найдена."})

    def test_post_serializer(self):
        """Проверка работы PostSerializer."""
        url = f"/api/v1/posts/{self.post.id}/"
        response = self.authorized_client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["text"], "test text 1")
        self.assertEqual(response.json()["author"], "testusername")

    def test_post_pagination_get_200(self):
        """Получение публикации c пагинацией. 200 Удачное выполнение запроса"""
        for i in range(POST_AMOUNT_TO_CREATE):
            Post.objects.create(
                text=f"test text {i + 2}",
                author=self.user,
            )
        limit = 2
        offset = 2
        url = f"/api/v1/posts/?limit={limit}&offset={offset}"
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), dict)
        self.assertTrue("results" in response.json())
        self.assertEqual(len(response.json().get("results")), limit)
        self.assertEqual(
            response.json().get("results")[0].get("text"), "test text 3"
        )
