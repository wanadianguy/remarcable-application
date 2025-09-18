from api.models.product import Product

def get_products_by_description_category_tag_ordered_by_name(description, category, tags):
	products = Product.objects.filter(description__icontains=description)
	if category:
		products = products.filter(category__name=category)
	for tag in tags:
		products = products.filter(tags__name=tag)
	return products.order_by('name')

def get_products_by_id_ordered_by_name(ids):
	return Product.objects.filter(id__in=ids).order_by('name')

def save_product(product, tags):
	saved_product = Product.objects.create(name=product.name, description=product.description, price=product.price, category=product.category)
	saved_product.tags.set(tags)
	return saved_product

def delete_products_by_id(ids):
	Product.objects.filter(id__in=ids).delete()
