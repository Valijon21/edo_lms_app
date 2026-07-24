from django.urls import path
from . import views

app_name = "simulator"

urlpatterns = [
    path("", views.simulator_list, name="list"),
    path("<int:pk>/", views.simulator_detail, name="detail"),
    path("<int:pk>/action/", views.simulator_action_api, name="action_api"),
    path("<int:pk>/reset/", views.simulator_reset, name="reset"),
]
