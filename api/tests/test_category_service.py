from django.test import TestCase
from unittest.mock import patch
from api.models.category import Category
from api.services.category import get_all_categories, create_categories, delete_categories

class CategoryServiceTests(TestCase):
    @patch("api.services.category.get_all_categories_ordered_by_name")
    def test_get_all_categories_calls_repository(self, mock_get):
        mock_get.return_value = ["cat1", "cat2"]
        categories = get_all_categories()
        self.assertEqual(categories, ["cat1", "cat2"])
        mock_get.assert_called_once()

    @patch("api.services.category.save_categories")
    def test_create_categories(self, mock_save):
        mock_save.return_value = (["saved"], ["failed"])
        categories = [{"name": "Clothing", "description": "Apparel"}]
        saved, failed = create_categories(categories)
        self.assertEqual(saved, ["saved"])
        self.assertEqual(failed, ["failed"])
        mock_save.assert_called_once()

    @patch("api.services.category.delete_categories_by_name")
    def test_delete_categories_calls_repository(self, mock_delete):
        delete_categories(["Books", "Electronics"])
        mock_delete.assert_called_once_with(["Books", "Electronics"])
