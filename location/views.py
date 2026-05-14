from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
import json
from feed.models import Crisis
from .models import District


def crisis_map(request):
    crises = Crisis.objects.select_related('geotag', 'category', 'district').exclude(geotag=None)

    crisis_data = []
    for c in crises:
        crisis_data.append({
            'id': c.pk,
            'title': c.title,
            'lat': float(c.geotag.latitude),
            'lng': float(c.geotag.longitude),
            'severity': c.severity,
            'status': c.status,
            'category': c.category.name if c.category else '',
            'color': c.category.color if c.category else '#999999',
            'district': c.district.name if c.district else '',
        })

    context = {
        'crisis_data': json.dumps(crisis_data, cls=DjangoJSONEncoder),
        'crisis_count': len(crisis_data),
        'crises': crises,
        'districts': District.objects.all(),
    }
    return render(request, 'location/crisis_map.html', context)