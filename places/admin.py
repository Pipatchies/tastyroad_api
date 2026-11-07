from django.contrib.gis import admin

from .models import FoodPlace

admin.site.register(FoodPlace, admin.GISModelAdmin)
