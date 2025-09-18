from django.test import TestCase
from unittest.mock import patch
from api.services.tag import get_all_tags, create_tags, delete_tags

class TagServiceTests(TestCase):
    @patch("api.services.tag.get_all_tags_ordered_by_name")
    def test_get_all_tags_calls_repository(self, mock_get):
        mock_get.return_value = ["tag1", "tag2"]
        tags = get_all_tags()
        self.assertEqual(tags, ["tag1", "tag2"])
        mock_get.assert_called_once()

    @patch("api.services.tag.save_tags")
    def test_create_tags(self, mock_save):
        mock_save.return_value = (["saved"], ["failed"])
        tags = [{"name": "Flask", "description": "Microframework"}]
        saved, failed = create_tags(tags)
        self.assertEqual(saved, ["saved"])
        self.assertEqual(failed, ["failed"])
        mock_save.assert_called_once()

    @patch("api.services.tag.delete_tags_by_name")
    def test_delete_tags_calls_repository(self, mock_delete):
        delete_tags(["Python", "Django"])
        mock_delete.assert_called_once_with(["Python", "Django"])
