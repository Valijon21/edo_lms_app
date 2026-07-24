from django.contrib import admin
from .models import SimulationScenario, SimulationSession, IncomingDocument


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


@admin.register(IncomingDocument)
class IncomingDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "doc_number", "doc_date", "sender",
        "is_registered", "registered_by", "received_at"
    )
    list_filter = ("is_registered", "doc_date", "state_type")
    search_fields = ("doc_number", "sender", "subject")
    readonly_fields = ("received_at", "created_at", "updated_at")
    fieldsets = (
        ("Document Info", {
            "fields": ("doc_number", "doc_date", "sender", "subject", "pdf_file")
        }),
        ("Registration Details", {
            "fields": (
                "doc_name", "reference_type", "executor", "description",
                "incoming_number", "outgoing_number",
                "incoming_date", "outgoing_date"
            )
        }),
        ("Additional Info", {
            "fields": (
                "execution_instruction", "state_type",
                "action_field", "external_corp"
            )
        }),
        ("Status", {
            "fields": (
                "is_registered", "registered_by", "registered_at",
                "signed_at", "received_at", "created_at", "updated_at"
            )
        }),
    )
