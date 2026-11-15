from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "age", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Profil TastyRoad", {"fields": ("age", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profil TastyRoad", {"fields": ("age", "avatar")}),
    )
