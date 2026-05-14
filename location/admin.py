from django.contrib import admin
from .models import District, GeoTag


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'division', 'population']
    search_fields = ['name', 'division']


@admin.register(GeoTag)
class GeoTagAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude', 'address']
