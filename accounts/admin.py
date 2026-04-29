from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name','description']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email','username','role','created_at','is_staff']
    ordering = ['email']
    fieldsets = UserAdmin.fieldsets + (
    ('Extra Info' , {'fields': ('role', 'created_at')}),
    )
    readonly_fields = ['created_at']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','is_verified']