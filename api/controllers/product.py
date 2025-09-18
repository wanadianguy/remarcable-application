from rest_framework.views import APIView
from api.serializers.product import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from api.services.product import create_products, delete_products, get_filtered_products

# Controller for handling requests that involve multiple products
# Serialized data represents JSON formatted data whereas deserialized data represents Python objects
class ProductsController(APIView):
	def get(self, request):
		# Gets all filters (description, category, tags)
		description = request.GET.get('description', '')
		category = request.GET.get('category', None)
		tags = request.GET.getlist('tag', [])

		# Gets all products that match the filters
		products = get_filtered_products(description, category, tags)
		serialized_products = ProductSerializer(products, many=True)
		return Response(serialized_products.data, status=status.HTTP_200_OK)

	def post(self, request):
		serialized_products = request.data.get('products')

		# Checks the format of the JSON data by making sure products are wrapped in an attribute called "products"
		if not serialized_products:
			return Response({"error": "No product provided"}, status=status.HTTP_400_BAD_REQUEST)

		products = ProductSerializer(data=serialized_products, many=True)
		products.is_valid(raise_exception=False)
		valid_products = []
		invalid_products = []

		# Separates valid and invalid products (valid products are the ones respecting the model's format)
		for i, product in enumerate(serialized_products):
			if i in products.errors:
				invalid_products.append({"product": product, "error": products.errors[i]})
			else:
				valid_products.append(product)

		saved_products = []
		failed_products = []
		if valid_products:
			saved_products, failed_products = create_products(valid_products)

		failed_products = failed_products + invalid_products

		serialized_saved_products = ProductSerializer(saved_products, many=True)

		if len(failed_products) == 0:
			return Response(serialized_saved_products.data ,status=status.HTTP_201_CREATED)

		if len(saved_products) == 0:
			return Response(failed_products ,status=status.HTTP_400_BAD_REQUEST)

		return Response(
			{
				"saved": serialized_saved_products.data,
				"failed": failed_products
			},
			status=status.HTTP_207_MULTI_STATUS
		)

	def delete(self, request):
		ids = request.data.get("ids")

		# Checks the format of the JSON data by making sure products' ids are wrapped in an attribute called "ids"
		if not ids:
			return Response({"error": "No product id provided"}, status=status.HTTP_400_BAD_REQUEST)

		delete_products(ids)
		return Response(status=status.HTTP_200_OK)
