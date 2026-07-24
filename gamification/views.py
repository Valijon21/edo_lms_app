from rest_framework import generics, permissions
from .models import UserGamificationProfile
from .serializers import UserGamificationProfileSerializer, LeaderboardSerializer

class GamificationProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserGamificationProfileSerializer

    def get_object(self):
        profile, _ = UserGamificationProfile.objects.get_or_create(user=self.request.user)
        return profile

class LeaderboardView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        return UserGamificationProfile.objects.all().order_by('-total_xp', '-current_streak')
