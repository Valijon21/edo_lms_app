"""Progress app signals: auto-issuing certificates upon course completion."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Progress, Certificate
from courses.models import Course, Lesson


@receiver(post_save, sender=Progress)
def check_course_completion(sender, instance, created, **kwargs):
    """Marks course as complete and generates a Certificate when all lessons are finished."""
    if instance.completed:
        user = instance.user
        course = instance.lesson.module.course
        
        # Get all lessons for this course
        course_lessons = Lesson.objects.filter(module__course=course)
        
        # Get completed lessons for this user in this course
        completed_count = Progress.objects.filter(
            user=user,
            completed=True,
            lesson__in=course_lessons
        ).count()
        
        # Issue certificate if all lessons are completed and not already issued
        if course_lessons.count() > 0 and completed_count == course_lessons.count():
            Certificate.objects.get_or_create(user=user, course=course)
