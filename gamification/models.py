from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserGamificationProfile(models.Model):
    """Foydalanuvchining umumiy gamifikatsiya ko'rsatkichlari"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gamification_profile', verbose_name=_("user"))
    total_xp = models.PositiveIntegerField(default=0, db_index=True, verbose_name=_("total XP"))
    current_streak = models.PositiveIntegerField(default=0, verbose_name=_("current streak"))
    longest_streak = models.PositiveIntegerField(default=0, verbose_name=_("longest streak"))
    last_activity_date = models.DateField(null=True, blank=True, verbose_name=_("last activity date"))

    class Meta:
        verbose_name = _("user gamification profile")
        verbose_name_plural = _("user gamification profiles")

    def __str__(self):
        return f"{self.user.username} - XP: {self.total_xp}"

class Badge(models.Model):
    """Tizimdagi yutuqlar va nishonlar"""
    name = models.CharField(max_length=100, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    badge_type = models.CharField(max_length=50, unique=True, verbose_name=_("badge type")) # e.g., 'fast_learner', 'seven_day_streak'
    xp_required = models.PositiveIntegerField(default=0, verbose_name=_("XP required"))
    icon = models.ImageField(upload_to='badges/', blank=True, null=True, verbose_name=_("icon"))

    class Meta:
        verbose_name = _("badge")
        verbose_name_plural = _("badges")

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    """Foydalanuvchiga berilgan nishonlar"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges', verbose_name=_("user"))
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, verbose_name=_("badge"))
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name=_("earned at"))

    class Meta:
        unique_together = ('user', 'badge')
        verbose_name = _("user badge")
        verbose_name_plural = _("user badges")

class GamificationActivityLog(models.Model):
    """XP berilgan har bir harakat tarixi"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs', verbose_name=_("user"))
    activity_type = models.CharField(max_length=50, verbose_name=_("activity type")) # e.g., 'lesson_completed', 'quiz_passed'
    xp_earned = models.PositiveIntegerField(verbose_name=_("XP earned"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("gamification activity log")
        verbose_name_plural = _("gamification activity logs")

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} (+{self.xp_earned} XP)"
