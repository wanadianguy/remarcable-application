from django.db import models
from api.models.tag import Tag
from api.models.category import Category
import uuid

class Product(models.Model):
	id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=500)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
	tags = models.ManyToManyField(Tag, related_name="products", blank=True)

	class Meta:
		db_table = 'products'
		verbose_name = "Product"
		verbose_name_plural = "Products"
