"""Test savollari, variantlar va urinishlar — dars (Module) va mavzu (Lesson) darajasida."""
from django.conf import settings
from django.db import models

from courses.models import Lesson, Module


class Question(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="questions"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="questions",
        null=True, blank=True
    )
    text = models.TextField()

    def __str__(self):
        return self.text[:60]


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True
    )
    score = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.lesson.title if self.lesson else self.module.title
        return f"{self.user} - {target} ({self.score}%)"
