from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Comment, Favorite, Itinerary, Step


class StepSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Step
        geo_field = "location"
        fields = [
            "id",
            "name",
            "description",
            "picture",
            "step_order",
            "location",
            "itinerary",
            "foodplace",
        ]


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Comment
        fields = ["id", "content", "review", "author", "itinerary"]
        read_only_fields = ["author"]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ["id", "user", "itinerary"]
        read_only_fields = ["user"]


class ItinerarySerializer(GeoFeatureModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        geo_field = "path"
        fields = [
            "id",
            "title",
            "type",
            "zone",
            "distance",
            "duration",
            "difficulty",
            "diet",
            "speciality",
            "facts",
            "path",
            "author",
            "steps",
            "comments",
        ]
        read_only_fields = ["author"]
