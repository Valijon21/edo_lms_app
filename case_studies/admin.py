from django.contrib import admin
from .models import CaseStudy, ScenarioNode, ScenarioEdge, UserCaseProgress

class ScenarioEdgeInline(admin.TabularInline):
    model = ScenarioEdge
    fk_name = 'from_node'
    extra = 1

@admin.register(ScenarioNode)
class ScenarioNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'case_study', 'is_start_node', 'is_end_node', 'is_fail_node')
    list_filter = ('case_study', 'is_start_node', 'is_end_node', 'is_fail_node')
    search_fields = ('title', 'content')
    inlines = [ScenarioEdgeInline]

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp_reward', 'is_active', 'created_at')
    search_fields = ('title', 'description')

@admin.register(ScenarioEdge)
class ScenarioEdgeAdmin(admin.ModelAdmin):
    list_display = ('from_node', 'option_text', 'to_node', 'xp_delta')
    list_filter = ('from_node__case_study',)
    search_fields = ('option_text', 'feedback_text')

@admin.register(UserCaseProgress)
class UserCaseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'case_study', 'current_node', 'score', 'is_completed')
    list_filter = ('case_study', 'is_completed')
    search_fields = ('user__username', 'case_study__title')
