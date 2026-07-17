"""Courses app URL yo'nalishlari."""
from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course_list"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("lessons/<int:pk>/", views.LessonDetailView.as_view(), name="lesson_detail"),
]
