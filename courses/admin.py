from django.contrib import admin

from .models import Course, Lesson, Module


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "max_attempts")
    inlines = [LessonInline]

    class Media:
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.2/tinymce.min.js",
            "js/admin_tinymce.js",
        )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "max_attempts")

    class Media:
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.2/tinymce.min.js",
            "js/admin_tinymce.js",
        )

