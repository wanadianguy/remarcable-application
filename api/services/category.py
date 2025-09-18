from api.repositories.category import delete_categories_by_name, save_categories, get_all_categories_ordered_by_name
from api.models.category import Category

def get_all_categories():
	return get_all_categories_ordered_by_name()

def create_categories(categories):
	categories_to_create = []
	for category in categories:
		categories_to_create.append(Category(name=category["name"], description=category["description"]))
	saved_categories, failed_categories = save_categories(categories_to_create)
	return saved_categories, failed_categories

def delete_categories(names):
	delete_categories_by_name(names)
