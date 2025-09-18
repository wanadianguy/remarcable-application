from django.test import TestCase
from unittest.mock import patch
from api.services.product import get_filtered_products, create_products, delete_products

class ProductServiceTests(TestCase):
    @patch("api.services.product.get_products_by_description_category_tag_ordered_by_name")
    def test_get_filtered_products_calls_repository(self, mock_get):
        mock_get.return_value = ["prod1", "prod2"]
        products = get_filtered_products("desc", "cat", ["tag"])
        self.assertEqual(products, ["prod1", "prod2"])
        mock_get.assert_called_once_with("desc", "cat", ["tag"])

    @patch("api.services.product.delete_products_by_id")
    @patch("api.services.product.get_products_by_id_ordered_by_name")
    @patch("api.services.product.decrement_category_number_of_products_by_name")
    @patch("api.services.product.decrement_tag_number_of_products_by_name")
    def test_delete_products(self, mock_dec_tag, mock_dec_cat, mock_get, mock_delete):
        mock_get.return_value = []
        delete_products([1, 2, 3])
        mock_get.assert_called_once_with([1, 2, 3])
        mock_delete.assert_called_once_with([1, 2, 3])
