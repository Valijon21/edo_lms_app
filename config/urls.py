"""Asosiy URL konfiguratsiyasi."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from core.views import HomeView, PlatformInfoView
from courses.admin_views import upload_image

admin.site.site_header = _("Edo LMS Admin Panel")
admin.site.site_title = _("Edo LMS Admin")
admin.site.index_title = _("Welcome to Edo LMS Administration")

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
    path("gamification/", include("gamification.urls")),
    path("case-studies/", include("case_studies.urls")),
    path("simulator/", include("simulator.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
