from django.conf import settings
from django.contrib.gis.db import models


# Itinerary Model
class Itinerary(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True)
    zone = models.CharField(max_length=100, blank=True)
    distance = models.FloatField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    diet = models.CharField(max_length=100, blank=True)
    speciality = models.CharField(max_length=255, blank=True)
    facts = models.TextField(blank=True)
    path = models.LineStringField(srid=4326)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_itineraries",
    )
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Favorite",
        related_name="favorited_itineraries",
        blank=True,
    )

    def __str__(self):
        return self.title


# Favorite Model
class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    itinerary = models.ForeignKey("Itinerary", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "itinerary")

    def __str__(self):
        return f"{self.user} - {self.itinerary}"


# FoodPlace Model
class FoodPlace(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    location = models.PointField(srid=4326)

    def __str__(self):
        return self.name


# Step Model
class Step(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to="steps_pictures/", null=True, blank=True)
    step_order = models.PositiveIntegerField()
    location = models.PointField(srid=4326)
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="steps"
    )
    foodplace = models.ForeignKey(
        "FoodPlace",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="steps",
    )

    class Meta:
        ordering = ["step_order"]

    def __str__(self):
        return f"{self.name} (Step {self.step_order})"


# Comment Model
class Comment(models.Model):
    content = models.TextField()
    review = models.IntegerField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    itinerary = models.ForeignKey(
        Itinerary, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"Comment by {self.author} on {self.itinerary}"
