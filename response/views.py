from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from feed.models import Crisis
from .models import ResponseTeam, Assignment, StatusUpdate


@login_required
def assign_team(request, crisis_pk):
    crisis = get_object_or_404(Crisis, pk=crisis_pk)

    if request.method == 'POST':
        team_id = request.POST.get('team')
        note = request.POST.get('note', '')
        team = get_object_or_404(ResponseTeam, pk=team_id)
        Assignment.objects.create(
            team=team,
            crisis=crisis,
            assigned_by=request.user,
            note=note,
        )
        messages.success(request, f'{team.name} assigned to crisis.')
        return redirect('crisis_detail', pk=crisis_pk)

    teams = ResponseTeam.objects.filter(is_active=True)
    return render(request, 'response/assign_team.html', {'crisis': crisis, 'teams': teams})


@login_required
def post_status_update(request, crisis_pk):
    crisis = get_object_or_404(Crisis, pk=crisis_pk)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        new_status = request.POST.get('new_status')

        StatusUpdate.objects.create(
            crisis=crisis,
            posted_by=request.user,
            message=message_text,
            new_status=new_status,
        )
        # Update the crisis status
        crisis.status = new_status
        crisis.save()

        messages.success(request, 'Status updated.')
        return redirect('crisis_detail', pk=crisis_pk)

    return render(request, 'response/post_status_update.html', {
        'crisis': crisis,
        'status_choices': StatusUpdate.STATUS_CHOICES,
    })
