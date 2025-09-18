from django.test import TestCase
from api.models.category import Category
from api.repositories.category import (
    get_all_categories_ordered_by_name,
    get_category_by_name,
    save_categories,
    delete_categories_by_name,
    increment_category_number_of_products_by_name,
    decrement_category_number_of_products_by_name,
)

class CategoryRepositoryTests(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Electronics", description="Devices")
        self.category2 = Category.objects.create(name="Books", description="Reading materials")

    def test_get_all_categories_ordered_by_name(self):
        categories = get_all_categories_ordered_by_name()
        self.assertEqual(list(categories), [self.category2, self.category1])  # Books before Electronics

    def test_get_category_by_name(self):
        category = get_category_by_name("Electronics")
        self.assertEqual(category.name, "Electronics")

    def test_save_categories_success_and_fail(self):
        new_category = Category(name="Clothing", description="Apparel")
        duplicate_category = Category(name="Clothing", description="Duplicate")

        saved, failed = save_categories([new_category, duplicate_category])
        self.assertIn(new_category, saved)
        self.assertIn({'category': duplicate_category, 'error': 'UNIQUE constraint failed: categories.name'}, failed)

    def test_delete_categories_by_name(self):
        delete_categories_by_name(["Books"])
        self.assertFalse(Category.objects.filter(name="Books").exists())
        self.assertTrue(Category.objects.filter(name="Electronics").exists())

    def test_increment_and_decrement_number_of_products(self):
        increment_category_number_of_products_by_name("Electronics")
        category = Category.objects.get(name="Electronics")
        self.assertEqual(category.number_of_products, 1)

        decrement_category_number_of_products_by_name("Electronics")
        category.refresh_from_db()
        self.assertEqual(category.number_of_products, 0)
