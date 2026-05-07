from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from feed.models import Crisis
from .models import Volunteer, Donation


@login_required
def volunteer_signup(request, crisis_pk):
    crisis = get_object_or_404(Crisis, pk=crisis_pk)

    if request.method == 'POST':
        skill = request.POST.get('skill')
        Volunteer.objects.create(user=request.user, crisis=crisis, skill=skill)
        messages.success(request, 'You have signed up as a volunteer.')
        return redirect('crisis_detail', pk=crisis_pk)

    return render(request, 'community/volunteer_signup.html', {
        'crisis': crisis,
        'skill_choices': Volunteer.SKILL_CHOICES,
    })


@login_required
def donate(request, crisis_pk):
    crisis = get_object_or_404(Crisis, pk=crisis_pk)

    if request.method == 'POST':
        amount = request.POST.get('amount') or None
        resource = request.POST.get('resource', '')
        message_text = request.POST.get('message', '')
        Donation.objects.create(
            donor=request.user,
            crisis=crisis,
            amount=amount,
            resource=resource,
            message=message_text,
        )
        messages.success(request, 'Thank you for your donation!')
        return redirect('crisis_detail', pk=crisis_pk)

    return render(request, 'community/donate.html', {'crisis': crisis})
