"""Progress app URL yo'nalishlari."""
from django.urls import path
from . import views

app_name = "progress"

urlpatterns = [
    path("dashboard/", views.UserProgressDashboardView.as_view(), name="user_dashboard"),
    path("manager/", views.ManagerDashboardView.as_view(), name="manager_dashboard"),
]
