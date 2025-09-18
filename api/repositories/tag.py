from api.models.tag import Tag

def get_all_tags_ordered_by_name():
	return Tag.objects.all().order_by('name')

def get_tag_by_name(name):
	return Tag.objects.get(name=name)

def save_tags(tags):
	saved = []
	failed = []
	for tag in tags:
		try:
			saved_tag = Tag.objects.create(name=tag.name, description=tag.description)
			saved.append(saved_tag)
		except Exception as error:
			failed.append({"tag": tag, "error": str(error)})

	return saved, failed

def delete_tags_by_name(names):
	Tag.objects.filter(name__in=names).delete()

def increment_tag_number_of_products_by_name(name):
	tag = Tag.objects.get(name=name)
	if tag:
		tag.number_of_products += 1
		tag.save()

def decrement_tag_number_of_products_by_name(name):
	tag = Tag.objects.get(name=name)
	if tag:
		tag.number_of_products -= 1
		tag.save()
