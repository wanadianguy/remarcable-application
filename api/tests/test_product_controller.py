from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from api.models.product import Product
from api.models.category import Category

class ProductsControllerTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Devices")
        self.product1 = Product.objects.create(
            name="Laptop", description="Portable computer", price=1000, category=self.category
        )
        self.product2 = Product.objects.create(
            name="Phone", description="Smartphone", price=500, category=self.category
        )
        self.url = reverse("products")

    @patch("api.controllers.product.get_filtered_products")
    def test_get_products(self, mock_service):
        mock_service.return_value = [self.product1, self.product2]
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch("api.controllers.product.create_products")
    def test_post_products_success(self, mock_service):
        from api.models.product import Product
        from api.models.category import Category

        category = Category.objects.create(name="Other", description="Devices")
        product = Product(name="Tablet", description="Device", price=300, category=category)

        mock_service.return_value = ([product], [])

        data = {"products": [{"name": "Tablet", "description": "Device", "price": 300, "category": "Electronics", "tags": []}]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Tablet")


    def test_post_products_invalid_format(self):
        data = {"wrong_key": []}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("api.controllers.product.delete_products")
    def test_delete_products_success(self, mock_service):
        data = {"ids": [str(self.product1.id)]}
        response = self.client.delete(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_service.assert_called_once_with([str(self.product1.id)])


    def test_delete_products_no_ids(self):
        data = {}
        response = self.client.delete(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
