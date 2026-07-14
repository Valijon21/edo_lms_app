"""Accounts app testlari."""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.mixins import user_has_role
from accounts.models import Profile


@pytest.mark.django_db
def test_profile_auto_created():
    user = User.objects.create_user(username="ali", password="parol12345")
    assert Profile.objects.filter(user=user).exists()
    assert user.profile.role == Profile.Role.IJROCHI


@pytest.mark.django_db
def test_register_view(client):
    url = reverse("accounts:register")
    response = client.post(
        url,
        {
            "username": "vali",
            "email": "vali@example.com",
            "password1": "KuchliParol123",
            "password2": "KuchliParol123",
        },
    )
    assert response.status_code == 302
    assert User.objects.filter(username="vali").exists()


@pytest.mark.django_db
def test_login_view(client):
    User.objects.create_user(username="hasan", password="parol12345")
    url = reverse("accounts:login")
    response = client.post(url, {"username": "hasan", "password": "parol12345"})
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_requires_login(client):
    url = reverse("accounts:profile")
    response = client.get(url)
    assert response.status_code == 302
    assert "/accounts/login/" in response.url


@pytest.mark.django_db
def test_user_has_role():
    user = User.objects.create_user(username="boss", password="parol12345")
    user.profile.role = Profile.Role.RAHBAR
    user.profile.save()
    assert user_has_role(user, (Profile.Role.RAHBAR,))
    assert not user_has_role(user, (Profile.Role.NAZORATCHI,))
