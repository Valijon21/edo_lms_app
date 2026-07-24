from django.db.models.signals import post_save
from django.dispatch import receiver
from progress.models import Progress
from quizzes.models import QuizAttempt
from gamification.services import reward_user_xp
from gamification.models import GamificationActivityLog

@receiver(post_save, sender=Progress)
def handle_lesson_completed(sender, instance, created, **kwargs):
    if instance.completed:
        user = instance.user
        activity_type = f"lesson_complete_{instance.lesson.id}"
        # Check if already rewarded
        if not GamificationActivityLog.objects.filter(user=user, activity_type=activity_type).exists():
            # Reward 10 XP for completing a lesson
            reward_user_xp(user, activity_type, xp_amount=10)

@receiver(post_save, sender=QuizAttempt)
def handle_quiz_attempt_passed(sender, instance, created, **kwargs):
    if created and instance.passed:
        user = instance.user
        if instance.lesson:
            activity_type = f"lesson_quiz_pass_{instance.lesson.id}"
            xp_amount = 20
        else:
            activity_type = f"module_quiz_pass_{instance.module.id}"
            xp_amount = 50
            
        # Check if already rewarded
        if not GamificationActivityLog.objects.filter(user=user, activity_type=activity_type).exists():
            reward_user_xp(user, activity_type, xp_amount=xp_amount)
