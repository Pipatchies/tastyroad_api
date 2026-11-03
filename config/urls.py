"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from itineraries.raw_views import raw_sql_itineraries_view
from itineraries.views import (
    CommentViewSet,
    FavoriteViewSet,
    ItineraryViewSet,
    StepViewSet,
)
from places.views import FoodPlaceViewSet
from users.views import RegisterView, UserProfileView

router = DefaultRouter()
router.register(r"itineraries", ItineraryViewSet, basename="itinerary")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"steps", StepViewSet, basename="step")
router.register(r"foodplaces", FoodPlaceViewSet, basename="foodplace")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/users/register/", RegisterView.as_view(), name="user_register"),
    path("api/users/me/", UserProfileView.as_view(), name="user_profile"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/raw/itineraries/", raw_sql_itineraries_view, name="raw-itineraries"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
