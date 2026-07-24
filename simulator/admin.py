from django.contrib import admin
from .models import SimulationScenario, SimulationSession


@admin.register(SimulationScenario)
class SimulationScenarioAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "doc_type", "difficulty", "xp_reward", "is_active", "created_at")
    list_filter = ("doc_type", "difficulty", "is_active")
    search_fields = ("title", "description")


@admin.register(SimulationSession)
class SimulationSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "scenario", "current_step_index", "score", "is_completed", "started_at")
    list_filter = ("is_completed",)
    search_fields = ("user__username", "scenario__title")
