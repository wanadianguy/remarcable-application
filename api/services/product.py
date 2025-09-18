from api.repositories.product import delete_products_by_id, get_products_by_id_ordered_by_name, get_products_by_description_category_tag_ordered_by_name, save_product
from api.repositories.category import decrement_category_number_of_products_by_name, get_category_by_name, increment_category_number_of_products_by_name, save_categories
from api.repositories.tag import get_tag_by_name, increment_tag_number_of_products_by_name, decrement_tag_number_of_products_by_name
from api.models.product import Product
from api.models.category import Category
from api.models.tag import Tag

def get_filtered_products(description, category, tags):
	try:
		return get_products_by_description_category_tag_ordered_by_name(description, category, tags)
	except Product.DoesNotExist:
		return []

def create_products(products):
	saved_products = []
	failed_products = []
	for product in products:
		# Adds product to "Other" category if none is provided (and create it if it doesn't exist). Also increments the number of products in the category
		try:
			category = get_category_by_name(product["category"])
		except Category.DoesNotExist:
			try:
				other_category = get_category_by_name("Other")
			except Category.DoesNotExist:
				other_category = Category(name="Other")
				create_categories([other_category])
			category = other_category
		increment_category_number_of_products_by_name(category.name)

		tags = []
		tag_names = product["tags"]
		if tag_names:
			for name in tag_names:
				# Increments the number of products in the category
				try:
					tag = get_tag_by_name(name)
					increment_tag_number_of_products_by_name(name)
					tags.append(tag)
				except Tag.DoesNotExist:
					continue

		try:
			saved_product = save_product(Product(name=product["name"], description=product["description"], price=product["price"], category=category), tags)
			saved_products.append(saved_product)
		except Exception as error:
			failed_products.append({"product": product, "error": str(error)})
	return saved_products, failed_products

def delete_products(ids):
	try:
		products = get_products_by_id_ordered_by_name(ids)
		for product in products:
			# Decrements the number of products in the category and tags
			decrement_category_number_of_products_by_name(product.category.name)
			for tag in product.tags.all():
				decrement_tag_number_of_products_by_name(tag.name)
	except Product.DoesNotExist:
		pass
	delete_products_by_id(ids)
