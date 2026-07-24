from rest_framework import generics, permissions
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserGamificationProfile
from .serializers import UserGamificationProfileSerializer, LeaderboardSerializer

class GamificationProfileView(LoginRequiredMixin, TemplateView):
    """Frontend view for user gamification profile"""
    template_name = "gamification/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = UserGamificationProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        context['badges'] = profile.user.badges.all().select_related('badge')
        context['recent_activities'] = profile.user.activity_logs.all().order_by('-created_at')[:10]
        return context

class LeaderboardView(LoginRequiredMixin, TemplateView):
    """Frontend view for leaderboard"""
    template_name = "gamification/leaderboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = UserGamificationProfile.objects.all().select_related('user').order_by('-total_xp', '-current_streak')[:50]
        return context
