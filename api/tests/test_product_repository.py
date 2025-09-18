from django.test import TestCase
from api.models.product import Product
from api.models.category import Category
from api.repositories.product import (
    get_products_by_description_category_tag_ordered_by_name,
    get_products_by_id_ordered_by_name,
    save_product,
    delete_products_by_id,
)

class ProductRepositoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Devices")
        self.product1 = Product.objects.create(
            name="Laptop", description="Portable computer", price=1000, category=self.category
        )
        self.product2 = Product.objects.create(
            name="Phone", description="Smartphone", price=500, category=self.category
        )

    def test_get_products_by_description_category_tag(self):
        products = get_products_by_description_category_tag_ordered_by_name("Portable", "Electronics", [])
        self.assertIn(self.product1, products)
        self.assertNotIn(self.product2, products)

    def test_get_products_by_id_ordered_by_name(self):
        products = get_products_by_id_ordered_by_name([self.product1.id, self.product2.id])
        self.assertEqual(list(products), [self.product1, self.product2])

    def test_save_product(self):
        product = Product(name="Tablet", description="Touch device", price=300, category=self.category)
        saved_product = save_product(product, [])
        self.assertEqual(saved_product.name, "Tablet")
        self.assertEqual(Product.objects.count(), 3)

    def test_delete_products_by_id(self):
        delete_products_by_id([self.product1.id])
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())
        self.assertTrue(Product.objects.filter(id=self.product2.id).exists())
