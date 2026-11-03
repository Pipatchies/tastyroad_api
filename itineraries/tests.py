# Create your tests here.
import pytest
from django.contrib.gis.geos import LineString
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from itineraries.models import Favorite, Itinerary
from users.models import User


@pytest.mark.django_db
class TestItineraryAPI:
    def setup_method(self):
        self.client = APIClient()
        self.url = "/api/itineraries/"
        self.user = User.objects.create_user(
            username="ariane_test",
            password="testpassword123",
        )

    def authenticate(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_get_itineraries_without_token_is_blocked(self):
        """Vérifie que l'accès sans JWT renvoie une erreur 401."""
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert (
            response.json()["detail"] == "Authentication credentials were not provided."
        )

    def test_get_itineraries_with_valid_token(self):
        """Vérifie que l'accès avec un JWT valide renvoie une FeatureCollection GeoJSON (200 OK)."""
        self.authenticate()
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.json()["type"] == "FeatureCollection"

    def test_create_itinerary_with_valid_token(self):
        """Vérifie que le POST crée l'itinéraire et assigne automatiquement l'auteur connecté."""
        self.authenticate()
        payload = {
            "title": "Nouveau parcours test",
            "distance": 15.5,
            "path": {
                "type": "LineString",
                "coordinates": [[1.4442, 43.6047], [1.4500, 43.6100]],
            },
        }

        response = self.client.post(self.url, payload, format="json")

        assert response.status_code == 201
        assert response.json()["properties"]["title"] == "Nouveau parcours test"
        assert response.json()["properties"]["author"] == self.user.id
        assert Itinerary.objects.count() == 1

    def test_comment_invalid_review_score_is_rejected(self):
        """Vérifie qu'une note supérieure à 5 est refusée (400 Bad Request)."""
        self.authenticate()
        itinerary = Itinerary.objects.create(
            title="Parcours Breton",
            author=self.user,
            path=LineString((1.0, 43.0), (1.1, 43.1)),
        )

        response = self.client.post(
            "/api/comments/",
            {"content": "Super !", "review": 10, "itinerary": itinerary.id},
            format="json",
        )

        assert response.status_code == 400
        assert "review" in response.json()

    def test_user_only_sees_own_favorites(self):
        """Vérifie qu'un utilisateur ne voit pas les favoris des autres utilisateurs."""
        other_user = User.objects.create_user(username="bob", password="password123")
        itinerary = Itinerary.objects.create(
            title="Parcours Normand",
            author=other_user,
            path=LineString((1.0, 43.0), (1.1, 43.1)),
        )
        Favorite.objects.create(user=other_user, itinerary=itinerary)

        self.authenticate()
        response = self.client.get("/api/favorites/")

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_raw_sql_itineraries_endpoint(self):
        """Vérifie le bon fonctionnement de la vue SQL brute et la validation du paramètre limit."""
        Itinerary.objects.create(
            title="Parcours SQL",
            distance=25.0,
            author=self.user,
            path=LineString((1.0, 43.0), (1.1, 43.1)),
        )

        response_ok = self.client.get("/api/raw/itineraries/?limit=1")
        assert response_ok.status_code == 200
        assert len(response_ok.json()["data"]) == 1

        response_bad = self.client.get("/api/raw/itineraries/?limit=-5")
        assert response_bad.status_code == 400
