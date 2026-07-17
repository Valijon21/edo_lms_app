"""Courses app view'lari."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Course, Module, Lesson


from django.utils import timezone
from progress.models import Progress


class CourseListView(LoginRequiredMixin, ListView):
    """Barcha kurslar ro'yxati."""
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"


class CourseDetailView(LoginRequiredMixin, DetailView):
    """Kurs haqida batafsil ma'lumot va uning darslari."""
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"


class LessonDetailView(LoginRequiredMixin, DetailView):
    """Mavzu sahifasi (matn, video va sidebar navigatsiya)."""
    model = Lesson
    template_name = "courses/lesson_detail.html"
    context_object_name = "lesson"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Agar mavzuning testi bo'lmasa, uni ochishi bilanoq yakunlangan deb hisoblaymiz.
        # Agar testi bo'lsa, faqat testdan o'tganda (passed=True) o'zlashtirilgan deb hisoblanadi.
        if not self.object.questions.exists():
            Progress.objects.get_or_create(
                user=request.user,
                lesson=self.object,
                defaults={"completed": True, "completed_at": timezone.now()}
            )
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Yon paneldagi navigatsiya uchun dars mavzulari ro'yxati
        context["module_lessons"] = self.object.module.lessons.all()
        
        # Keyingi mavzuni aniqlash
        next_lesson = Lesson.objects.filter(
            module=self.object.module,
            order__gt=self.object.order
        ).first()
        
        if not next_lesson:
            # Agar ushbu darsda mavzu qolmagan bo'lsa, keyingi darsning birinchi mavzusini izlaymiz
            next_module = Module.objects.filter(
                course=self.object.module.course,
                order__gt=self.object.module.order
            ).first()
            if next_module:
                next_lesson = next_module.lessons.first()
                
        context["next_lesson"] = next_lesson
        context["has_lesson_quiz"] = self.object.questions.exists()
        return context

