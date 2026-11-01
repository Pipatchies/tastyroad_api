from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import FoodPlace


class FoodPlaceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FoodPlace
        geo_field = "location"
        fields = ["id", "name", "type", "description", "location"]
