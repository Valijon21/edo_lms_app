from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CaseStudy(models.Model):
    """Umumiy Keys ma'lumoti"""
    title = models.CharField(max_length=200, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"))
    # Keysni to'liq tamomlaganlik uchun bonus
    xp_reward = models.PositiveIntegerField(
        default=50,
        verbose_name=_("XP reward")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at")
    )

    class Meta:
        verbose_name = _("case study")
        verbose_name_plural = _("case studies")

    def __str__(self):
        return self.title


class ScenarioNode(models.Model):
    """Keys ichidagi muayyan qadam yoki holat (Savol / Matn)"""
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name='nodes',
        verbose_name=_("case study")
    )
    title = models.CharField(max_length=150, verbose_name=_("title"))
    # Keysning shu qismidagi holat matni
    content = models.TextField(verbose_name=_("content"))
    is_start_node = models.BooleanField(
        default=False,
        verbose_name=_("is start node")
    )
    is_end_node = models.BooleanField(
        default=False,
        verbose_name=_("is end node")
    )
    # Xato qaror qabul qilganda tugash nuqtasi
    is_fail_node = models.BooleanField(
        default=False,
        verbose_name=_("is fail node")
    )

    class Meta:
        verbose_name = _("scenario node")
        verbose_name_plural = _("scenario nodes")

    def __str__(self):
        return f"{self.case_study.title} - {self.title}"


class ScenarioEdge(models.Model):
    """
    Tugunlar orasidagi bog'lanish va foydalanuvchining
    tanlov variantlari
    """
    from_node = models.ForeignKey(
        ScenarioNode,
        on_delete=models.CASCADE,
        related_name='edges',
        verbose_name=_("from node")
    )
    to_node = models.ForeignKey(
        ScenarioNode,
        on_delete=models.CASCADE,
        related_name='incoming_edges',
        verbose_name=_("to node")
    )
    # Ekranda chiqadigan tanlov tugmasi matni
    option_text = models.CharField(
        max_length=255,
        verbose_name=_("option text")
    )
    # Tanlovdan keyingi tushuntirish matni (Huquqiy asos)
    feedback_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("feedback text")
    )
    # To'g'ri yoki noto'g'ri qaror uchun ball (+/-)
    xp_delta = models.IntegerField(
        default=0,
        verbose_name=_("XP delta")
    )

    class Meta:
        verbose_name = _("scenario edge")
        verbose_name_plural = _("scenario edges")

    def __str__(self):
        return (
            f"From '{self.from_node.title}' to '{self.to_node.title}' "
            f"via '{self.option_text}'"
        )


class UserCaseProgress(models.Model):
    """Foydalanuvchining keys ustidagi faol holati"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='case_progresses',
        verbose_name=_("user")
    )
    case_study = models.ForeignKey(
        CaseStudy,
        on_delete=models.CASCADE,
        related_name='user_progresses',
        verbose_name=_("case study")
    )
    current_node = models.ForeignKey(
        ScenarioNode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("current node")
    )
    score = models.IntegerField(default=0, verbose_name=_("score"))
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_("is completed")
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("started at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at")
    )

    class Meta:
        unique_together = ('user', 'case_study')
        verbose_name = _("user case progress")
        verbose_name_plural = _("user case progresses")

    def __str__(self):
        return (
            f"{self.user.username} - {self.case_study.title} "
            f"(Completed: {self.is_completed})"
        )
