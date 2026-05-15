from django.shortcuts import render
from feed.models import Crisis
from .models import District
import json

def crisis_map(request):
    # Get all crises that have a geotag
    crises_with_location = Crisis.objects.filter(geotag__isnull=False).select_related('geotag', 'category', 'district')
    
    # Prepare data for Leaflet.js map
    map_data = []
    for c in crises_with_location:
        map_data.append({
            'id': c.id,
            'title': c.title,
            'lat': float(c.geotag.latitude),
            'lng': float(c.geotag.longitude),
            'severity': c.severity,
            'status': c.status,
            'category': c.category.name if c.category else "Other",
            'color': c.category.color if c.category else "#666666",
            'district': c.district.name if c.district else ""
        })

    context = {
        'crisis_data_json': json.dumps(map_data),
        'total_count': crises_with_location.count(),
        'districts': District.objects.all(),
    }
    return render(request, 'location/crisis_map.html', context)
