from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Case, When, IntegerField
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Crisis, Category, CrisisMedia, Upvote
from location.models import District, GeoTag

def crisis_feed(request):
    crises = Crisis.objects.select_related('category', 'reported_by', 'district').prefetch_related('media').annotate(
        upvote_count=Count('upvotes')
    )

    # Filters from the sidebar
    district_id = request.GET.get('district')
    category_id = request.GET.get('category')
    severity = request.GET.get('severity')
    status = request.GET.get('status')
    query = request.GET.get('q')
    sort = request.GET.get('sort', 'latest')

    if district_id:
        crises = crises.filter(district_id=district_id)
    if category_id:
        crises = crises.filter(category_id=category_id)
    if severity:
        crises = crises.filter(severity=severity)
    if status:
        crises = crises.filter(status=status)
    if query:
        crises = crises.filter(title__icontains=query) | crises.filter(description__icontains=query)

    # Sorting logic
    if sort == 'upvotes':
        crises = crises.order_by('-upvote_count')
    elif sort == 'critical':
        # Custom ordering for severity
        crises = crises.annotate(
            severity_priority=Case(
                When(severity='critical', then=1),
                When(severity='high', then=2),
                When(severity='medium', then=3),
                When(severity='low', then=4),
                output_field=IntegerField(),
            )
        ).order_by('severity_priority', '-created_at')
    else:
        crises = crises.order_by('-created_at')

    context = {
        'crises': crises,
        'categories': Category.objects.all(),
        'districts': District.objects.all(),
        'severity_choices': Crisis.SEVERITY_CHOICES,
        'status_choices': Crisis.STATUS_CHOICES,
    }
    return render(request, 'feed/crisis_feed.html', context)

def crisis_detail(request, pk):
    crisis = get_object_or_404(
        Crisis.objects.select_related('category', 'reported_by', 'district', 'geotag')
                      .prefetch_related('media', 'upvotes', 'status_updates', 'assignments', 'volunteers'),
        pk=pk
    )
    upvote_count = crisis.upvotes.count()
    user_upvoted = request.user.is_authenticated and crisis.upvotes.filter(user=request.user).exists()

    context = {
        'crisis': crisis,
        'upvote_count': upvote_count,
        'user_upvoted': user_upvoted,
    }
    return render(request, 'feed/crisis_detail.html', context)

@login_required
def report_crisis(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category')
        severity = request.POST.get('severity')
        district_id = request.POST.get('district')

        if not all([title, description, category_id, severity, district_id]):
            messages.error(request, 'All required fields must be filled.')
            return render(request, 'feed/report_crisis.html', {
                'categories': Category.objects.all(),
                'districts': District.objects.all(),
                'severity_choices': Crisis.SEVERITY_CHOICES,
            })

        crisis = Crisis.objects.create(
            title=title,
            description=description,
            category_id=category_id,
            severity=severity,
            district_id=district_id,
            reported_by=request.user,
        )

        # Optional GeoTagging
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        addr = request.POST.get('location_name')
        if lat and lng:
            geotag = GeoTag.objects.create(latitude=lat, longitude=lng, address=addr or "")
            crisis.geotag = geotag
            crisis.save()

        # Media Uploads
        for f in request.FILES.getlist('media'):
            m_type = 'image' if f.content_type.startswith('image') else 'video'
            CrisisMedia.objects.create(crisis=crisis, file=f, media_type=m_type, uploaded_by=request.user)

        messages.success(request, "Crisis reported successfully!")
        return redirect('crisis_detail', pk=crisis.pk)

    return render(request, 'feed/report_crisis.html', {
        'categories': Category.objects.all(),
        'districts': District.objects.all(),
        'severity_choices': Crisis.SEVERITY_CHOICES,
    })

@login_required
def edit_crisis(request, pk):
    crisis = get_object_or_404(Crisis, pk=pk)

    # Only reporter or staff can edit
    if crisis.reported_by != request.user and not request.user.is_staff:
        messages.error(request, "You can only edit crises you reported.")
        return redirect('crisis_detail', pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category_id = request.POST.get('category')
        severity = request.POST.get('severity')
        district_id = request.POST.get('district')

        if not all([title, description, category_id, severity, district_id]):
            messages.error(request, 'All required fields must be filled.')
        else:
            crisis.title = title
            crisis.description = description
            crisis.category_id = category_id
            crisis.severity = severity
            crisis.district_id = district_id
            crisis.save()

            # New media uploads
            for f in request.FILES.getlist('media'):
                m_type = 'image' if f.content_type.startswith('image') else 'video'
                CrisisMedia.objects.create(crisis=crisis, file=f, media_type=m_type, uploaded_by=request.user)

            messages.success(request, "Crisis updated successfully.")
            return redirect('crisis_detail', pk=pk)

    return render(request, 'feed/edit_crisis.html', {
        'crisis': crisis,
        'categories': Category.objects.all(),
        'districts': District.objects.all(),
        'severity_choices': Crisis.SEVERITY_CHOICES,
    })


@login_required
def delete_crisis(request, pk):
    crisis = get_object_or_404(Crisis, pk=pk)

    if crisis.reported_by != request.user and not request.user.is_staff:
        messages.error(request, "You can only delete crises you reported.")
        return redirect('crisis_detail', pk=pk)

    if request.method == 'POST':
        crisis.delete()
        messages.success(request, "Crisis report deleted.")
        return redirect('crisis_feed')

    return render(request, 'feed/delete_crisis.html', {'crisis': crisis})


@login_required
def delete_media(request, media_pk):
    media = get_object_or_404(CrisisMedia, pk=media_pk)
    crisis_pk = media.crisis.pk

    if media.crisis.reported_by != request.user and not request.user.is_staff:
        messages.error(request, "You can only delete media from your own reports.")
        return redirect('crisis_detail', pk=crisis_pk)

    if request.method == 'POST':
        # Delete file from disk
        if media.file:
            import os
            if os.path.isfile(media.file.path):
                os.remove(media.file.path)
        media.delete()
        messages.success(request, "Media removed.")
        return redirect('edit_crisis', pk=crisis_pk)

    return redirect('edit_crisis', pk=crisis_pk)


@login_required
def my_reports(request):
    crises = Crisis.objects.filter(reported_by=request.user).annotate(
        upvote_count=Count('upvotes'),
        media_count=Count('media'),
    ).order_by('-created_at')
    return render(request, 'feed/my_reports.html', {'crises': crises})


@login_required
def toggle_upvote(request, pk):
    crisis = get_object_or_404(Crisis, pk=pk)
    upvote, created = Upvote.objects.get_or_create(crisis=crisis, user=request.user)
    if not created:
        upvote.delete()
    return JsonResponse({'upvoted': created, 'count': crisis.upvotes.count()})


@login_required
def dashboard_view(request):
    # 1. Severity Distribution
    severity_data = Crisis.objects.values('severity').annotate(count=Count('severity')).order_by('severity')
    severity_labels = [item['severity'].capitalize() for item in severity_data]
    severity_counts = [item['count'] for item in severity_data]

    # 2. Crises by District
    district_data = Crisis.objects.values('district__name').annotate(count=Count('district__name')).order_by('-count')
    district_labels = [item['district__name'] for item in district_data]
    district_counts = [item['count'] for item in district_data]

    # 3. Reporting Trends (last 7 days)
    today = timezone.now().date()
    date_counts = []
    date_labels = []
    for i in range(7):
        date = today - timedelta(days=6 - i)
        count = Crisis.objects.filter(created_at__date=date).count()
        date_labels.append(date.strftime('%b %d'))
        date_counts.append(count)

    # 4. Heatmap Data (GeoTags)
    heatmap_data = []
    geotagged_crises = Crisis.objects.filter(geotag__isnull=False).select_related('geotag')
    for crisis in geotagged_crises:
        heatmap_data.append({
            'lat': float(crisis.geotag.latitude),
            'lng': float(crisis.geotag.longitude),
            'count': 1 # Each point represents one crisis
        })

    context = {
        'severity_labels': severity_labels,
        'severity_counts': severity_counts,
        'district_labels': district_labels,
        'district_counts': district_counts,
        'date_labels': date_labels,
        'date_counts': date_counts,
        'heatmap_data': heatmap_data,
    }
    return render(request, 'feed/dashboard.html', context)
