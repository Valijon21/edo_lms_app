from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserGamificationProfile, Badge, UserBadge, GamificationActivityLog

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'description', 'badge_type', 'xp_required', 'icon')

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ('badge', 'earned_at')

class GamificationActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationActivityLog
        fields = ('id', 'activity_type', 'xp_earned', 'created_at')

class UserGamificationProfileSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    badges = serializers.SerializerMethodField()
    recent_activities = serializers.SerializerMethodField()
    
    class Meta:
        model = UserGamificationProfile
        fields = ('user', 'total_xp', 'current_streak', 'longest_streak', 'last_activity_date', 'badges', 'recent_activities')
        
    def get_badges(self, obj):
        user_badges = UserBadge.objects.filter(user=obj.user).order_by('-earned_at')
        return UserBadgeSerializer(user_badges, many=True).data
        
    def get_recent_activities(self, obj):
        logs = GamificationActivityLog.objects.filter(user=obj.user).order_by('-created_at')[:10]
        return GamificationActivityLogSerializer(logs, many=True).data

class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = UserGamificationProfile
        fields = ('user', 'total_xp', 'current_streak')
