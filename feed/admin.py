from django.contrib import admin
from .models import Category, Crisis, CrisisMedia, Upvote


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color']


class CrisisMediaInline(admin.TabularInline):
    model = CrisisMedia
    extra = 1


@admin.register(Crisis)
class CrisisAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'reported_by', 'district', 'severity', 'status', 'created_at']
    list_filter = ['severity', 'status', 'category', 'district']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CrisisMediaInline]


@admin.register(CrisisMedia)
class CrisisMediaAdmin(admin.ModelAdmin):
    list_display = ['crisis', 'media_type', 'uploaded_by', 'uploaded_at']


@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ['crisis', 'user', 'created_at']
