from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from api.models.tag import Tag

class TagsControllerTests(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Python", description="Language")
        self.tag2 = Tag.objects.create(name="Django", description="Framework")
        self.url = reverse("tags")

    @patch("api.controllers.tag.get_all_tags")
    def test_get_tags(self, mock_service):
        mock_service.return_value = [self.tag1, self.tag2]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch("api.controllers.tag.create_tags")
    def test_post_tags_success(self, mock_service):
        mock_service.return_value = ([{"name": "Flask", "description": "Microframework"}], [])
        data = {"tags": [{"name": "Flask", "description": "Microframework"}]}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

    def test_post_tags_invalid_format(self):
        data = {"wrong_key": []}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("api.controllers.tag.delete_tags")
    def test_delete_tags_success(self, mock_service):
        data = {"names": ["Python"]}
        response = self.client.delete(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_service.assert_called_once_with(["Python"])

    def test_delete_tags_no_names(self):
        data = {}
        response = self.client.delete(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
