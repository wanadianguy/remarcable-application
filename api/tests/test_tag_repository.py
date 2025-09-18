from django.test import TestCase
from api.models.tag import Tag
from api.repositories.tag import (
    get_all_tags_ordered_by_name,
    get_tag_by_name,
    save_tags,
    delete_tags_by_name,
    increment_tag_number_of_products_by_name,
    decrement_tag_number_of_products_by_name,
)

class TagRepositoryTests(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Python", description="Language")
        self.tag2 = Tag.objects.create(name="Django", description="Framework")

    def test_get_all_tags_ordered_by_name(self):
        tags = get_all_tags_ordered_by_name()
        self.assertEqual(list(tags), [self.tag2, self.tag1])  # Django before Python

    def test_get_tag_by_name(self):
        tag = get_tag_by_name("Python")
        self.assertEqual(tag.name, "Python")

    def test_save_tags_success_and_fail(self):
        new_tag = Tag(name="Flask", description="Microframework")
        duplicate_tag = Tag(name="Flask", description="Duplicate")

        saved, failed = save_tags([new_tag, duplicate_tag])
        self.assertIn(new_tag, saved)
        self.assertTrue(any("error" in f for f in failed))

    def test_delete_tags_by_name(self):
        delete_tags_by_name(["Django"])
        self.assertFalse(Tag.objects.filter(name="Django").exists())
        self.assertTrue(Tag.objects.filter(name="Python").exists())

    def test_increment_and_decrement_number_of_products(self):
        increment_tag_number_of_products_by_name("Python")
        tag = Tag.objects.get(name="Python")
        self.assertEqual(tag.number_of_products, 1)

        decrement_tag_number_of_products_by_name("Python")
        tag.refresh_from_db()
        self.assertEqual(tag.number_of_products, 0)
