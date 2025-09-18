from rest_framework.views import APIView
from api.serializers.category import CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from api.services.category import get_all_categories, create_categories, delete_categories

# Controller for handling requests that involve multiple categories
# Serialized data represents JSON formatted data whereas deserialized data represents Python objects
class CategoriesController(APIView):
	def get(self, request):
		categories = get_all_categories()
		serialized_categories = CategorySerializer(categories, many=True)
		return Response(serialized_categories.data, status=status.HTTP_200_OK)

	def post(self, request):
		serialized_categories = request.data.get("categories")

		# Checks the format of the JSON data by making sure categories are wrapped in an attribute called "categories"
		if not serialized_categories:
			return Response({"error": "No category provided"}, status=status.HTTP_400_BAD_REQUEST)

		categories = CategorySerializer(data=serialized_categories, many=True)
		categories.is_valid(raise_exception=False)
		valid_categories = []
		invalid_categories = []

		# Separates valid and invalid categories (valid categories are the ones respecting the model's format)
		for i, category in enumerate(serialized_categories):
			if i in categories.errors:
				invalid_categories.append({"category": category, "error": categories.errors[i]})
			else:
				valid_categories.append(category)

		saved_categories = []
		failed_categories = []
		if valid_categories:
			saved_categories, failed_categories = create_categories(valid_categories)

		failed_categories = failed_categories + invalid_categories

		serialized_saved_categories = CategorySerializer(saved_categories, many=True)

		if len(failed_categories) == 0:
			return Response(serialized_saved_categories.data ,status=status.HTTP_201_CREATED)

		if len(saved_categories) == 0:
			return Response(failed_categories ,status=status.HTTP_400_BAD_REQUEST)

		return Response(
			{
				"saved": serialized_saved_categories.data,
				"failed": failed_categories
			},
			status=status.HTTP_207_MULTI_STATUS
		)

	def delete(self, request):
		names = request.data.get("names")

		# Checks the format of the JSON data by making sure categories' names are wrapped in an attribute called "names"
		if not names:
			return Response({"error": "No category name provided"}, status=status.HTTP_400_BAD_REQUEST)

		delete_categories(names);
		return Response(status=status.HTTP_200_OK)
