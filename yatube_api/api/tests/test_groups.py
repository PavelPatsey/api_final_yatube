from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Group, User


class GroupViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testusername")
        cls.group = Group.objects.create(
            title="test group title",
            slug="testgroupslug",
            description="test group description",
        )
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(cls.user)

    def test_cool_test(self):
        """cool test"""
        self.assertEqual(True, True)

    def test_get_group_list_200(self):
        """Список сообществ. 200 Удачное выполнение запроса без пагинации"""
        url = "/api/v1/groups/"
        Group.objects.create(
            title="test group title 2",
            slug="testgroupslug2",
            description="test group description 2",
        )
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)
        self.assertEqual(len(response.json()), 2)

    def test_get_group_creat(self):
        """Список сообществ. Нельзя создавать сообщесва"""
        url = "/api/v1/groups/"
        group_count = Group.objects.count()
        data = {
            "title": "test group title 2",
            "slug": "testgroupslug2",
            "description": "test group description 2",
        }
        response = self.authorized_client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(len(response.json()), group_count)
