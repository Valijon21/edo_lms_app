from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class DocumentType(models.TextChoices):
    KIRUVCHI = "KIRUVCHI", _("Incoming mail")
    CHIQUVCHI = "CHIQUVCHI", _("Outgoing mail")
    ICHKI_BUYRUQ = "ICHKI_BUYRUQ", _("Internal order")


class DifficultyLevel(models.TextChoices):
    EASY = "EASY", _("Beginner (Easy)")
    MEDIUM = "MEDIUM", _("Intermediate")
    HARD = "HARD", _("Advanced (Complex)")


class SimulationScenario(models.Model):
    """Edo.ijro.uz virtual simulyatsiyasi uchun ssenariylar modeli."""
    title = models.CharField(max_length=255, verbose_name=_("scenario title"))
    doc_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.KIRUVCHI,
        verbose_name=_("document type")
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.EASY,
        verbose_name=_("difficulty")
    )
    description = models.TextField(verbose_name=_("description"))
    initial_doc_data = models.JSONField(
        default=dict,
        help_text=_("Initial layout of the document (number, date, outgoing organization, summary, file)")
    )
    expected_steps = models.JSONField(
        default=list,
        help_text=_("Sequence of steps that must be completed correctly")
    )
    xp_reward = models.PositiveIntegerField(default=100, verbose_name=_("XP reward"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("simulation scenario")
        verbose_name_plural = _("simulation scenarios")
        ordering = ["id"]

    def __str__(self):
        return f"[{self.get_doc_type_display()}] {self.title}"


class SimulationSession(models.Model):
    """Foydalanuvchining simulyatordagi amaliy mashq sessiyasi."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="simulation_sessions",
        verbose_name=_("user")
    )
    scenario = models.ForeignKey(
        SimulationScenario,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("scenario")
    )
    current_step_index = models.IntegerField(default=0, verbose_name=_("current step"))
    performed_actions = models.JSONField(
        default=list,
        help_text=_("History of actions performed by the user")
    )
    score = models.IntegerField(default=0, verbose_name=_("XP score"))
    is_completed = models.BooleanField(default=False, verbose_name=_("is completed"))
    started_at = models.DateTimeField(auto_now_add=True, verbose_name=_("started at"))
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("completed at"))

    class Meta:
        verbose_name = _("simulation session")
        verbose_name_plural = _("simulation sessions")
        unique_together = ("user", "scenario")

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title} ({'Tugatilgan' if self.is_completed else 'Jarayonda'})"
