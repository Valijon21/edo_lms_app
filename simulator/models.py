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



class IncomingDocument(models.Model):
    """Kiruvchi hujjatlar ro'yxati - Devonxona uchun"""
    
    # Document identification
    doc_number = models.CharField(
        max_length=50,
        verbose_name=_("document number")
    )
    doc_date = models.DateField(verbose_name=_("document date"))
    sender = models.CharField(
        max_length=255,
        verbose_name=_("sender organization")
    )
    subject = models.TextField(verbose_name=_("subject/content summary"))
    
    # Registration fields
    doc_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("document name")
    )
    reference_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("reference type")
    )
    executor = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("executor")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("description")
    )
    
    # Dates and numbers
    incoming_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("incoming number")
    )
    outgoing_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("outgoing number")
    )
    incoming_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("incoming date")
    )
    outgoing_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("outgoing date")
    )
    
    # Additional fields
    execution_instruction = models.TextField(
        blank=True,
        verbose_name=_("execution instruction")
    )
    state_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('geographic', "Qo'riqchi o'qurganlar"),
            ('state', "O'qarlabiga")
        ],
        verbose_name=_("state type")
    )
    action_field = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("action field")
    )
    external_corp = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("external corporation")
    )
    
    # File attachment
    pdf_file = models.FileField(
        upload_to='incoming_documents/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("PDF file")
    )
    
    # Registration status
    is_registered = models.BooleanField(
        default=False,
        verbose_name=_("is registered")
    )
    registered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("registered at")
    )
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registered_documents',
        verbose_name=_("registered by")
    )
    
    # Timestamps
    signed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("signed at")
    )
    received_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("received at")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at")
    )
    
    class Meta:
        ordering = ['-received_at']
        verbose_name = _("incoming document")
        verbose_name_plural = _("incoming documents")
        indexes = [
            models.Index(fields=['doc_number']),
            models.Index(fields=['doc_date']),
            models.Index(fields=['is_registered']),
        ]
    
    def __str__(self):
        return f"{self.doc_number} - {self.sender}"
