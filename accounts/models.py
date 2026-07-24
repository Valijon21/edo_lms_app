"""Foydalanuvchi profili va rollari (2-bosqichda kengaytiriladi)."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    class Role(models.TextChoices):
        IJROCHI = "ijrochi", _("Performer")
        NAZORATCHI = "nazoratchi", _("Controller")
        RAHBAR = "rahbar", _("Leader")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("user"),
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.IJROCHI,
        verbose_name=_("role"),
    )

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"{self.user} ({self.get_role_display()})"
