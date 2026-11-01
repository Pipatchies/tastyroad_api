from django.contrib.gis.db import models


# FoodPlace Model
class FoodPlace(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    location = models.PointField(srid=4326)

    def __str__(self):
        return self.name
