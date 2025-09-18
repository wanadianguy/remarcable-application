from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from api.models.category import Category

class CategoriesControllerTests(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Electronics", description="Devices")
        self.category2 = Category.objects.create(name="Books", description="Reading materials")
        self.url = reverse("categories")

    @patch("api.controllers.category.get_all_categories")
    def test_get_categories(self, mock_service):
        mock_service.return_value = [self.category1, self.category2]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch("api.controllers.category.create_categories")
    def test_post_categories_success(self, mock_service):
        mock_service.return_value = ([{"name": "Clothing", "description": "Apparel"}], [])
        data = {"categories": [{"name": "Clothing", "description": "Apparel"}]}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)

    def test_post_categories_invalid_format(self):
        data = {"wrong_key": []}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("api.controllers.category.delete_categories")
    def test_delete_categories_success(self, mock_service):
        data = {"names": ["Electronics"]}
        response = self.client.delete(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_service.assert_called_once_with(["Electronics"])

    def test_delete_categories_no_names(self):
        data = {}
        response = self.client.delete(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
