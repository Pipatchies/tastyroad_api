from rest_framework import viewsets

from .models import FoodPlace
from .serializers import FoodPlaceSerializer


class FoodPlaceViewSet(viewsets.ModelViewSet):
    queryset = FoodPlace.objects.all()
    serializer_class = FoodPlaceSerializer
