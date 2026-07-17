"""Asosiy URL konfiguratsiyasi."""
from django.contrib import admin
from django.urls import include, path

from core.views import HomeView, PlatformInfoView
from courses.admin_views import upload_image

urlpatterns = [
    path("admin/upload-image/", upload_image, name="admin_upload_image"),
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("info/", PlatformInfoView.as_view(), name="platform_info"),
    path("accounts/", include("accounts.urls")),
    path("api/", include("api.urls")),
    path("courses/", include("courses.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("progress/", include("progress.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
