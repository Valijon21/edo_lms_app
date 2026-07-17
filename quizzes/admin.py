from django.contrib import admin

from .models import Answer, Question, QuizAttempt


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "module", "lesson")
    list_filter = ("module", "lesson")
    inlines = [AnswerInline]

    class Media:
        js = (
            "js/admin_quiz.js",
        )


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "module", "lesson", "score", "passed", "created_at")
    list_filter = ("passed", "module", "lesson")
