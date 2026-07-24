"""
Professional Django Admin Configuration for Quizzes
- Hierarchical filtering by Course → Module → Lesson
- Question count per lesson/module
- Inline editing with improved UX
- Custom list displays with statistics
"""
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Answer, Question, QuizAttempt


class AnswerInline(admin.TabularInline):
    """Inline editor for answers with professional layout"""
    model = Answer
    extra = 2
    fields = ('text', 'is_correct')
    verbose_name = _("Javob varianti")
    verbose_name_plural = _("Javob variantlari")


class CourseFilter(admin.SimpleListFilter):
    """Custom filter to show Course hierarchy in Question admin"""
    title = _('Kurs')
    parameter_name = 'course'

    def lookups(self, request, model_admin):
        from courses.models import Course
        courses = Course.objects.all().order_by('order')
        return [(c.id, c.title) for c in courses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(module__course_id=self.value())
        return queryset


class ModuleWithCountFilter(admin.SimpleListFilter):
    """Module filter showing question counts"""
    title = _('Dars (Module)')
    parameter_name = 'module'

    def lookups(self, request, model_admin):
        from courses.models import Module
        # Get course filter if applied
        course_id = request.GET.get('course')
        modules = Module.objects.all()
        if course_id:
            modules = modules.filter(course_id=course_id)

        modules = modules.annotate(
            question_count=Count('questions')
        ).order_by('course__order', 'order')

        return [
            (m.id, f"{m.course.title} → {m.title} ({m.question_count} ta savol)")
            for m in modules
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(module_id=self.value())
        return queryset


class LessonWithCountFilter(admin.SimpleListFilter):
    """Lesson filter showing question counts per lesson"""
    title = _('Mavzu (Lesson)')
    parameter_name = 'lesson'

    def lookups(self, request, model_admin):
        from courses.models import Lesson
        # Get module filter if applied
        module_id = request.GET.get('module')
        lessons = Lesson.objects.all()
        if module_id:
            lessons = lessons.filter(module_id=module_id)

        lessons = lessons.annotate(
            question_count=Count('questions')
        ).order_by('module__order', 'order')

        # Group by module for better readability
        result = []
        for lesson in lessons:
            result.append((
                lesson.id,
                f"{lesson.module.title} → {lesson.title} ({lesson.question_count} ta savol)"
            ))
        return result

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(lesson_id=self.value())
        return queryset


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Professional Question Admin with hierarchical filtering"""
    list_display = (
        'get_short_text',
        'get_course',
        'module',
        'lesson',
        'get_answer_count',
        'get_correct_answer'
    )
    list_filter = (
        CourseFilter,
        ModuleWithCountFilter,
        LessonWithCountFilter,
    )
    search_fields = ('text', 'module__title', 'lesson__title')
    inlines = [AnswerInline]
    list_per_page = 50

    fieldsets = (
        (_('Savol ma\'lumotlari'), {
            'fields': ('module', 'lesson', 'text'),
            'description': _('Har bir mavzu uchun kamida 20 ta savol yarating')
        }),
    )

    class Media:
        js = ('js/admin_quiz.js',)
        css = {
            'all': ('css/admin_custom.css',) if False else []  # Add custom CSS if needed
        }

    def get_short_text(self, obj):
        """Display shortened question text"""
        text = obj.text[:80]
        if len(obj.text) > 80:
            text += "..."
        return text
    get_short_text.short_description = _('Savol')

    def get_course(self, obj):
        """Display course name"""
        return obj.module.course.title
    get_course.short_description = _('Kurs')
    get_course.admin_order_field = 'module__course__title'

    def get_answer_count(self, obj):
        """Display number of answer options"""
        count = obj.answers.count()
        color = 'green' if count >= 4 else 'orange' if count >= 2 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} ta</span>',
            color,
            count
        )
    get_answer_count.short_description = _('Javoblar')

    def get_correct_answer(self, obj):
        """Display if correct answer is set"""
        has_correct = obj.answers.filter(is_correct=True).exists()
        if has_correct:
            return format_html('<span style="color: green;">✓ Belgilangan</span>')
        return format_html('<span style="color: red;">✗ Yo\'q</span>')
    get_correct_answer.short_description = _('To\'g\'ri javob')

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'module',
            'module__course',
            'lesson'
        ).prefetch_related('answers')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Professional Quiz Attempt Admin with statistics"""
    list_display = (
        'get_user_info',
        'get_course',
        'module',
        'lesson',
        'get_score_badge',
        'get_status',
        'created_at'
    )
    list_filter = (
        'passed',
        CourseFilter,
        'module',
        'lesson',
        'created_at'
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'module__title',
        'lesson__title'
    )
    readonly_fields = ('user', 'module', 'lesson', 'score', 'passed', 'created_at')
    list_per_page = 100
    date_hierarchy = 'created_at'

    def get_user_info(self, obj):
        """Display user with full name"""
        full_name = obj.user.get_full_name() or obj.user.username
        return format_html(
            '<strong>{}</strong><br/><small style="color: #666;">{}</small>',
            full_name,
            obj.user.username
        )
    get_user_info.short_description = _('Foydalanuvchi')
    get_user_info.admin_order_field = 'user__username'

    def get_course(self, obj):
        """Display course name"""
        return obj.module.course.title
    get_course.short_description = _('Kurs')
    get_course.admin_order_field = 'module__course__title'

    def get_score_badge(self, obj):
        """Display score with color coding"""
        if obj.score >= 80:
            color = 'green'
            icon = '✓'
        elif obj.score >= 60:
            color = 'orange'
            icon = '●'
        else:
            color = 'red'
            icon = '✗'

        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-weight: bold;">{} {}%</span>',
            color,
            icon,
            obj.score
        )
    get_score_badge.short_description = _('Ball')
    get_score_badge.admin_order_field = 'score'

    def get_status(self, obj):
        """Display pass/fail status"""
        if obj.passed:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ O\'tdi</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ O\'tmadi</span>'
        )
    get_status.short_description = _('Holat')
    get_status.admin_order_field = 'passed'

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'user',
            'module',
            'module__course',
            'lesson'
        )

    def has_add_permission(self, request):
        """Disable manual creation of quiz attempts"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete quiz attempts"""
        return request.user.is_superuser
