from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from .models import Crisis, Category, CrisisMedia, Upvote
from location.models import District


def crisis_feed(request):
    crises = Crisis.objects.select_related('category', 'reported_by', 'district').annotate(
        upvote_count=Count('upvotes')
    )

    # Filters
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

    if sort == 'upvotes':
        crises = crises.order_by('-upvote_count')
    elif sort == 'critical':
        severity_order = ['critical', 'high', 'medium', 'low']
        # Django doesn't natively support custom ordering — use Python sort as fallback
        crises = sorted(crises, key=lambda c: severity_order.index(c.severity))
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
                      .prefetch_related('media', 'upvotes'),
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
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        severity = request.POST.get('severity')
        district_id = request.POST.get('district')

        crisis = Crisis.objects.create(
            title=title,
            description=description,
            category_id=category_id,
            severity=severity,
            district_id=district_id,
            reported_by=request.user,
        )

        # Handle media uploads
        for f in request.FILES.getlist('media'):
            media_type = 'image' if f.content_type.startswith('image') else 'video'
            CrisisMedia.objects.create(
                crisis=crisis,
                file=f,
                media_type=media_type,
                uploaded_by=request.user,
            )

        return redirect('crisis_detail', pk=crisis.pk)

    context = {
        'categories': Category.objects.all(),
        'districts': District.objects.all(),
        'severity_choices': Crisis.SEVERITY_CHOICES,
    }
    return render(request, 'feed/report_crisis.html', context)


@login_required
def toggle_upvote(request, pk):
    crisis = get_object_or_404(Crisis, pk=pk)
    upvote, created = Upvote.objects.get_or_create(crisis=crisis, user=request.user)
    if not created:
        upvote.delete()
    upvote_count = crisis.upvotes.count()
    return JsonResponse({'upvoted': created, 'count': upvote_count})