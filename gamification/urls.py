from django.urls import path
from .views import GamificationProfileView, LeaderboardView

app_name = 'gamification'

urlpatterns = [
    path('profile/', GamificationProfileView.as_view(), name='profile'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
