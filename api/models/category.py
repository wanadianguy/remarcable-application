from django.db import models

class Category(models.Model):
	name = models.CharField(primary_key=True, max_length=300)
	description = models.TextField(blank=True)
	number_of_products = models.PositiveIntegerField(default=0)

	class Meta:
		db_table = 'categories'
		verbose_name = "Category"
		verbose_name_plural = "Categories"
