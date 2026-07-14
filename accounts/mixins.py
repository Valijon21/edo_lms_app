"""Rolga asoslangan ruxsat mixin va yordamchilari."""
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Profile


def user_has_role(user, roles):
    """Foydalanuvchi profili roli `roles` ichida ekanini tekshiradi."""
    if not user.is_authenticated:
        return False
    profile = getattr(user, "profile", None)
    if profile is None:
        return False
    return profile.role in roles


class RoleRequiredMixin(UserPassesTestMixin):
    """Berilgan rollardan biriga ega foydalanuvchiga ruxsat beradi."""

    allowed_roles = ()

    def test_func(self):
        return user_has_role(self.request.user, self.allowed_roles)


class RahbarRequiredMixin(RoleRequiredMixin):
    allowed_roles = (Profile.Role.RAHBAR,)


class NazoratchiRequiredMixin(RoleRequiredMixin):
    allowed_roles = (Profile.Role.RAHBAR, Profile.Role.NAZORATCHI)
