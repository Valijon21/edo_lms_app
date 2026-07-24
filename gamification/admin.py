from django.contrib import admin
from .models import UserGamificationProfile, Badge, UserBadge, GamificationActivityLog

@admin.register(UserGamificationProfile)
class UserGamificationProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_xp', 'current_streak', 'longest_streak', 'last_activity_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    ordering = ('-total_xp',)

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge_type', 'xp_required')
    search_fields = ('name', 'badge_type')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge', 'earned_at')
    search_fields = ('user__username',)

@admin.register(GamificationActivityLog)
class GamificationActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'xp_earned', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'activity_type')
    ordering = ('-created_at',)
