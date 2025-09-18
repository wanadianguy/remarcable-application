from django.db import models

class Tag(models.Model):
	name = models.CharField(primary_key=True, max_length=300)
	description = models.TextField(blank=True)
	number_of_products = models.PositiveIntegerField(default=0)

	class Meta:
		db_table = 'tags'
		verbose_name = "Tag"
		verbose_name_plural = "Tags"
