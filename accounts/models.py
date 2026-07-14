"""Foydalanuvchi profili va rollari (2-bosqichda kengaytiriladi)."""
from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        IJROCHI = "ijrochi", "Ijrochi"
        NAZORATCHI = "nazoratchi", "Nazoratchi"
        RAHBAR = "rahbar", "Rahbar"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.IJROCHI
    )

    def __str__(self):
        return f"{self.user} ({self.get_role_display()})"
