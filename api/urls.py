"""API endpoint'lari (4-bosqichda test topshirish qo'shiladi)."""
from django.urls import path

from .views import health_check

app_name = "api"

urlpatterns = [
    path("health/", health_check, name="health"),
]
