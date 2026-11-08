import io

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

User = get_user_model()


def get_dummy_avatar(filename="avatar.jpg"):
    """Generate a tiny in-memory image for upload testing."""
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="blue").save(buffer, format="JPEG")
    return SimpleUploadedFile(filename, buffer.getvalue(), content_type="image/jpeg")


@pytest.mark.django_db
class TestUserModel:
    """Test suite for the Custom User model."""

    def test_create_user_with_all_fields(self):
        """Ensure a user can be created with both standard and custom fields."""
        avatar_file = get_dummy_avatar()
        user = User.objects.create_user(
            username="gourmet_traveler",
            email="gourmet@tastyroad.com",
            password="secure_password_123",
            first_name="Jean",
            last_name="Dupont",
            age=32,
            avatar=avatar_file,
        )

        # Standard fields
        assert user.username == "gourmet_traveler"
        assert user.email == "gourmet@tastyroad.com"
        assert user.first_name == "Jean"
        assert user.last_name == "Dupont"
        assert user.check_password("secure_password_123") is True
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

        # Custom fields
        assert user.age == 32
        assert user.avatar.name.startswith("avatars/avatar")

    def test_create_user_with_optional_fields_empty(self):
        """Ensure age and avatar can be blank/null."""
        user = User.objects.create_user(
            username="minimal_user",
            password="secure_password_123",
        )
        assert user.age is None
        assert not user.avatar

    def test_create_superuser(self):
        """Ensure a superuser is created with proper staff and superuser permissions."""
        admin = User.objects.create_superuser(
            username="admin_user",
            email="admin@tastyroad.com",
            password="admin_password_123",
            age=40,
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.age == 40

    def test_user_str_representation(self):
        """Ensure __str__ returns the username."""
        user = User.objects.create_user(username="charlie", password="password123")
        assert str(user) == "charlie"

    def test_delete_account_rgpd_right_to_be_forgotten(self):
        """Vérifie que DELETE /api/users/me/ supprime le compte et ses traces GPS en cascade (RGPD)."""
        from django.contrib.gis.geos import LineString
        from rest_framework.test import APIClient
        from rest_framework_simplejwt.tokens import RefreshToken

        from itineraries.models import Itinerary

        user = User.objects.create_user(username="rgpd_user", password="password123")
        Itinerary.objects.create(
            title="Trace GPS personnelle",
            author=user,
            path=LineString((1.0, 43.0), (1.1, 43.1)),
        )
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = client.delete("/api/users/me/")
        assert response.status_code == 204
        assert User.objects.filter(id=user.id).exists() is False
        assert Itinerary.objects.filter(author_id=user.id).exists() is False
