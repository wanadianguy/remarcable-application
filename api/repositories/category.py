from api.models.category import Category

def get_all_categories_ordered_by_name():
	return Category.objects.all().order_by('name')

def get_category_by_name(name):
	return Category.objects.get(name=name)

def save_categories(categories):
	saved = []
	failed = []
	for category in categories:
		try:
			saved_category = Category.objects.create(name=category.name, description=category.description)
			saved.append(saved_category)
		except Exception as error:
			failed.append({"category": category, "error": str(error)})

	return saved, failed

def delete_categories_by_name(names):
	Category.objects.filter(name__in=names).delete()

def increment_category_number_of_products_by_name(name):
	category = Category.objects.get(name=name)
	if category:
		category.number_of_products += 1
		category.save()

def decrement_category_number_of_products_by_name(name):
	category = Category.objects.get(name=name)
	if category:
		category.number_of_products -= 1
		category.save()
