"""Progress app view'lari."""
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.views.generic import TemplateView

from accounts.mixins import NazoratchiRequiredMixin
from courses.models import Course, Lesson
from quizzes.models import QuizAttempt
from .models import Certificate, Progress

User = get_user_model()


class UserProgressDashboardView(LoginRequiredMixin, TemplateView):
    """Foydalanuvchining o'z shaxsiy progress paneli (Dashboard)."""
    template_name = "progress/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Jami darslar va tugatilgan darslar soni
        total_lessons = Lesson.objects.count()
        completed_lessons = Progress.objects.filter(user=user, completed=True).count()

        # O'zlashtirish foizi
        completion_percentage = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0

        # Har bir kurs bo'yicha progress
        courses = Course.objects.all()
        course_progress_list = []
        for course in courses:
            course_lessons_count = Lesson.objects.filter(module__course=course).count()
            completed_course_lessons = Progress.objects.filter(
                user=user,
                completed=True,
                lesson__module__course=course
            ).count()
            
            percentage = int((completed_course_lessons / course_lessons_count * 100)) if course_lessons_count > 0 else 0
            
            course_progress_list.append({
                "course": course,
                "total_lessons": course_lessons_count,
                "completed_lessons": completed_course_lessons,
                "percentage": percentage,
            })

        # Urinishlar tarixi
        attempts = QuizAttempt.objects.filter(user=user).order_by("-created_at")

        # Sertifikatlar
        certificates = Certificate.objects.filter(user=user)

        context.update({
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "completion_percentage": completion_percentage,
            "course_progress": course_progress_list,
            "attempts": attempts,
            "certificates": certificates,
        })
        return context


class ManagerDashboardView(LoginRequiredMixin, NazoratchiRequiredMixin, TemplateView):
    """Rahbar va Nazoratchilar uchun xodimlar o'zlashtirishi tahlil paneli."""
    template_name = "progress/manager_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Barcha xodimlarni yuklash (superusers hisobga olinmaydi)
        users = User.objects.filter(is_superuser=False).select_related("profile")
        
        # Jami darslar soni
        total_lessons_count = Lesson.objects.count()

        user_reports = []
        for u in users:
            # Ushbu foydalanuvchining o'qilgan darslari soni
            done_lessons = Progress.objects.filter(user=u, completed=True).count()
            percentage = int((done_lessons / total_lessons_count * 100)) if total_lessons_count > 0 else 0
            
            # Test topshirish urinishlari ko'rsatkichlari
            user_attempts = QuizAttempt.objects.filter(user=u)
            attempts_count = user_attempts.count()
            passed_attempts = user_attempts.filter(passed=True).count()
            
            # Sertifikatlar
            cert_count = Certificate.objects.filter(user=u).count()

            user_reports.append({
                "user": u,
                "completed_lessons": done_lessons,
                "percentage": percentage,
                "attempts_count": attempts_count,
                "passed_attempts": passed_attempts,
                "certificate_count": cert_count,
            })

        context.update({
            "user_reports": user_reports,
            "total_lessons": total_lessons_count,
        })
        return context
