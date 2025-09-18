from api.repositories.tag import delete_tags_by_name, save_tags, get_all_tags_ordered_by_name
from api.models.tag import Tag

def get_all_tags():
	return get_all_tags_ordered_by_name()

def create_tags(tags):
	tags_to_create = []
	for tag in tags:
		tags_to_create.append(Tag(name=tag["name"], description=tag["description"]))
	saved_tags, failed_tags = save_tags(tags_to_create)
	return saved_tags, failed_tags

def delete_tags(names):
	delete_tags_by_name(names)
