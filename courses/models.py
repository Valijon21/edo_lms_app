"""Kurs, dars va mavzu modellari (UI: Modul=Dars, Lesson=Mavzu)."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("order"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name=_("course"),
    )
    title = models.CharField(max_length=255, verbose_name=_("title"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("order"))
    max_attempts = models.PositiveIntegerField(
        default=6,
        null=True,
        blank=True,
        help_text=_("Maximum number of attempts. Blank or 0 means unlimited."),
        verbose_name=_("maximum attempts"),
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("module")
        verbose_name_plural = _("modules")

    def __str__(self):
        return f"{self.course} / {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("module"),
    )
    title = models.CharField(max_length=255, verbose_name=_("title"))
    content = models.TextField(blank=True, verbose_name=_("content"))
    video_url = models.URLField(blank=True, verbose_name=_("video URL"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("order"))
    max_attempts = models.PositiveIntegerField(
        default=6,
        null=True,
        blank=True,
        help_text=_("Maximum number of attempts. Blank or 0 means unlimited."),
        verbose_name=_("maximum attempts"),
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")

    def __str__(self):
        return self.title
