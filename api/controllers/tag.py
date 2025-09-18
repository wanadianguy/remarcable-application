from rest_framework.views import APIView
from api.serializers.tag import TagSerializer
from rest_framework.response import Response
from rest_framework import status
from api.services.tag import get_all_tags, create_tags, delete_tags

# Controller for handling requests that involve multiple tags
# Serialized data represents JSON formatted data whereas deserialized data represents Python objects
class TagsController(APIView):
	def get(self, request):
		tags = get_all_tags()
		serialized_tags = TagSerializer(tags, many=True)
		return Response(serialized_tags.data, status=status.HTTP_200_OK)

	def post(self, request):
		serialized_tags = request.data.get("tags")

		# Checks the format of the JSON data by making sure tags are wrapped in an attribute called "tags"
		if not serialized_tags:
			return Response({"error": "No tag provided"}, status=status.HTTP_400_BAD_REQUEST)

		tags = TagSerializer(data=serialized_tags, many=True)
		tags.is_valid(raise_exception=False)
		valid_tags = []
		invalid_tags = []

		# Separates valid and invalid tags (valid tags are the ones respecting the model's format)
		for i, tag in enumerate(serialized_tags):
			if i in tags.errors:
				invalid_tags.append({"tag": tag, "error": tags.errors[i]})
			else:
				valid_tags.append(tag)

		saved_tags = []
		failed_tags = []
		if valid_tags:
			saved_tags, failed_tags = create_tags(valid_tags)

		failed_tags = failed_tags + invalid_tags

		serialized_saved_tags = TagSerializer(saved_tags, many=True)

		if len(failed_tags) == 0:
			return Response(serialized_saved_tags.data ,status=status.HTTP_201_CREATED)

		if len(saved_tags) == 0:
			return Response(failed_tags ,status=status.HTTP_400_BAD_REQUEST)

		return Response(
			{
				"saved": serialized_saved_tags.data,
				"failed": failed_tags
			},
			status=status.HTTP_207_MULTI_STATUS
		)

	def delete(self, request):
		names = request.data.get("names")

		# Checks the format of the JSON data by making sure tags' names are wrapped in an attribute called "names"
		if not names:
			return Response({"error": "No tag name provided"}, status=status.HTTP_400_BAD_REQUEST)

		delete_tags(names);
		return Response(status=status.HTTP_200_OK)
