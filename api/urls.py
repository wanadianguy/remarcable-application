from django.urls import path
from api.controllers.category import CategoriesController
from api.controllers.tag import TagsController
from api.controllers.product import ProductsController


urlpatterns = [
    path("categories", CategoriesController.as_view(), name="categories"),
    path("tags", TagsController.as_view(), name="tags"),
    path("products", ProductsController.as_view(), name="products")
]
