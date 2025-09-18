from django.urls import path
from frontend.product_search import product_search


urlpatterns = [
	path("", product_search)
]
