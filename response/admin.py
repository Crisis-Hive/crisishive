from django.contrib import admin
from .models import ResponseTeam, Assignment, StatusUpdate


@admin.register(ResponseTeam)
class ResponseTeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'team_type', 'leader', 'district', 'is_active']
    list_filter = ['team_type', 'is_active']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['team', 'crisis', 'assigned_by', 'assigned_at']
    list_filter = ['team']


@admin.register(StatusUpdate)
class StatusUpdateAdmin(admin.ModelAdmin):
    list_display = ['crisis', 'posted_by', 'new_status', 'created_at']
    list_filter = ['new_status']
    readonly_fields = ['created_at']
