"""Test savollari, variantlar va urinishlar — dars (Module) va mavzu (Lesson) darajasida."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Lesson, Module


class Question(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name=_("module"),
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="questions",
        null=True,
        blank=True,
        verbose_name=_("lesson"),
    )
    text = models.TextField(verbose_name=_("text"))

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return self.text[:60]


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("question"),
    )
    text = models.CharField(max_length=255, verbose_name=_("text"))
    is_correct = models.BooleanField(default=False, verbose_name=_("is correct"))

    class Meta:
        verbose_name = _("answer")
        verbose_name_plural = _("answers")

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        verbose_name=_("user"),
    )
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, verbose_name=_("module")
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("lesson"),
    )
    score = models.PositiveIntegerField(default=0, verbose_name=_("score"))
    passed = models.BooleanField(default=False, verbose_name=_("passed"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("quiz attempt")
        verbose_name_plural = _("quiz attempts")

    def __str__(self):
        target = self.lesson.title if self.lesson else self.module.title
        return f"{self.user} - {target} ({self.score}%)"
