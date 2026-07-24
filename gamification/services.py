from django.utils import timezone
from .models import UserGamificationProfile, Badge, UserBadge, GamificationActivityLog

def reward_user_xp(user, activity_type, xp_amount):
    """Rewards XP to a user and logs the activity, updates streak and badges."""
    profile, _ = UserGamificationProfile.objects.get_or_create(user=user)
    
    # 1. Update total XP
    profile.total_xp += xp_amount
    profile.save()
    
    # 2. Log activity
    GamificationActivityLog.objects.create(
        user=user,
        activity_type=activity_type,
        xp_earned=xp_amount
    )
    
    # 3. Update daily streak
    update_user_streak(profile)
    
    # 4. Check for new badges
    check_and_award_badges(user, profile)
    return profile

def update_user_streak(profile):
    """Updates user current and longest streak based on last activity date."""
    today = timezone.localdate()
    
    if profile.last_activity_date == today:
        return # already updated today
        
    yesterday = today - timezone.timedelta(days=1)
    if profile.last_activity_date == yesterday:
        profile.current_streak += 1
    else:
        # streak broken or first activity
        profile.current_streak = 1
        
    if profile.current_streak > profile.longest_streak:
        profile.longest_streak = profile.current_streak
        
    profile.last_activity_date = today
    profile.save()

def check_and_award_badges(user, profile):
    """Checks and awards badges to the user based on total XP or streaks."""
    # Find all badges the user has not yet earned
    earned_badge_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    badges_to_check = Badge.objects.exclude(id__in=earned_badge_ids)
    
    for badge in badges_to_check:
        if profile.total_xp >= badge.xp_required:
            # Also check if it's a streak badge
            if badge.badge_type == 'streak_3' and profile.current_streak < 3:
                continue
            if badge.badge_type == 'streak_7' and profile.current_streak < 7:
                continue
                
            # Award badge
            UserBadge.objects.get_or_create(user=user, badge=badge)
