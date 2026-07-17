"""Quizzes app URL yo'nalishlari."""
from django.urls import path
from . import views

app_name = "quizzes"

urlpatterns = [
    path("<int:module_id>/take/", views.TakeQuizView.as_view(), name="quiz_take"),
    path("<int:module_id>/submit/", views.SubmitQuizView.as_view(), name="quiz_submit"),
    path("lesson/<int:lesson_id>/take/", views.TakeLessonQuizView.as_view(), name="lesson_quiz_take"),
    path("lesson/<int:lesson_id>/submit/", views.SubmitLessonQuizView.as_view(), name="lesson_quiz_submit"),
    path("results/<int:attempt_id>/", views.AttemptResultView.as_view(), name="attempt_result"),
]
