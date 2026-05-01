from django.contrib import admin
from .models import Volunteer, Donation


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'crisis', 'skill', 'status', 'signed_up_at']
    list_filter = ['status', 'skill']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'crisis', 'amount', 'resource', 'created_at']
    readonly_fields = ['created_at']



