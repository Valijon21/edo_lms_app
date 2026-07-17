import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import json

User = get_user_model()


@pytest.fixture
def normal_user(db):
    return User.objects.create_user(username="normaluser", password="password123")


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="adminuser", password="password123", is_staff=True)


@pytest.mark.django_db
def test_upload_image_anonymous_redirect(client):
    url = reverse("admin_upload_image")
    response = client.post(url, {})
    # Anonim foydalanuvchilar login sahifasiga yo'naltirilishi kerak
    assert response.status_code == 302
    assert "login" in response.url


@pytest.mark.django_db
def test_upload_image_normal_user_redirect(client, normal_user):
    client.login(username="normaluser", password="password123")
    url = reverse("admin_upload_image")
    response = client.post(url, {})
    # Oddiy foydalanuvchi (staff bo'lmagan) ham login/admin-login sahifasiga yo'naltiriladi
    assert response.status_code == 302


@pytest.mark.django_db
def test_upload_image_staff_success(client, staff_user):
    client.login(username="adminuser", password="password123")
    url = reverse("admin_upload_image")
    
    # Kichik 1x1 GIF rasmi
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
        b'\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b'
    )
    uploaded_file = SimpleUploadedFile("test.gif", small_gif, content_type="image/gif")
    
    response = client.post(url, {"file": uploaded_file}, format="multipart")
    
    assert response.status_code == 200
    data = json.loads(response.content.decode("utf-8"))
    assert "location" in data
    assert "/media/uploads/" in data["location"]


@pytest.mark.django_db
def test_upload_image_staff_invalid_extension(client, staff_user):
    client.login(username="adminuser", password="password123")
    url = reverse("admin_upload_image")
    
    # Rasm bo'lmagan matnli fayl
    invalid_file = SimpleUploadedFile("script.py", b"print('hello')", content_type="text/plain")
    
    response = client.post(url, {"file": invalid_file}, format="multipart")
    
    assert response.status_code == 400
    data = json.loads(response.content.decode("utf-8"))
    assert "error" in data
    assert "Faqat rasm fayllari" in data["error"]
