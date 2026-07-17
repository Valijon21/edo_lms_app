"""Kurs, dars va mavzu modellari (UI: Modul=Dars, Lesson=Mavzu)."""
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules"
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(
        default=6, null=True, blank=True,
        help_text="Maksimal urinishlar soni. Bo'sh yoki 0 bo'lsa - cheksiz."
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course} / {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(
        default=6, null=True, blank=True,
        help_text="Maksimal urinishlar soni. Bo'sh yoki 0 bo'lsa - cheksiz."
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
