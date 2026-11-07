from django.contrib.gis import admin

from .models import Comment, Favorite, Itinerary, Step

admin.site.register(Itinerary, admin.GISModelAdmin)
admin.site.register(Step, admin.GISModelAdmin)
admin.site.register(Comment)
admin.site.register(Favorite)
