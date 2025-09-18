from django.contrib import admin
from api.models.category import Category
from api.models.tag import Tag
from api.models.product import Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "number_of_products")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "number_of_products")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "category")
    list_filter = ("category", "tags")
    search_fields = ("id", "name")
    filter_horizontal = ("tags",)
