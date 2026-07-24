"""O'zlashtirish kuzatuvi va sertifikat (5-bosqichda kengaytiriladi)."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Lesson


class Progress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progress",
        verbose_name=_("user"),
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name=_("lesson")
    )
    completed = models.BooleanField(default=False, verbose_name=_("completed"))
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("completed at")
    )

    class Meta:
        unique_together = ("user", "lesson")
        verbose_name = _("progress")
        verbose_name_plural = _("progresses")

    def __str__(self):
        return f"{self.user} - {self.lesson}"


class Certificate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificates",
        verbose_name=_("user"),
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, verbose_name=_("course")
    )
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name=_("issued at"))

    class Meta:
        verbose_name = _("certificate")
        verbose_name_plural = _("certificates")

    def __str__(self):
        return f"Sertifikat: {self.user} - {self.course}"
