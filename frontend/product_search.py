from django.shortcuts import render
import requests

def product_search(request):
	# Get all categories present  the database
    categories_response = requests.get(f"{request.scheme}://{request.get_host()}/categories")
    categories = categories_response.json() if categories_response.status_code == 200 else []

	# Get all tags present  the database
    tags_response = requests.get(f"{request.scheme}://{request.get_host()}/tags")
    tags = tags_response.json() if tags_response.status_code == 200 else []

	# Get parameters from current URL
    params = {
        "description": request.GET.get("description", ""),
        "category": request.GET.get("category"),
    }
    tags_selected = request.GET.getlist("tag")
    params["tag"] = tags_selected

    # Get products based on the parameters
    products_response = requests.get(f"{request.scheme}://{request.get_host()}/products", params=params)
    products = products_response.json() if products_response.status_code == 200 else []

	# Renders the frontend template with all relevant data
    return render(
        request,
        "product_search.html",
        {
            "categories": categories,
            "tags": tags,
            "products": products
        },
    )
