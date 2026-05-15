from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResponseTeam, Assignment, StatusUpdate
from feed.models import Crisis


def is_authorized_to_manage(user):
    return user.is_staff or (user.role and user.role.name in ['Admin', 'Government Official'])


def is_authorized_to_update(user):
    return is_authorized_to_manage(user) or (user.role and user.role.name == 'Responder')


@login_required
def assign_team(request, pk):
    if not is_authorized_to_manage(request.user):
        messages.error(request, "Access denied. Only Government Officials or Admins can assign teams.")
        return redirect('crisis_detail', pk=pk)

    crisis = get_object_or_404(Crisis, pk=pk)
    if request.method == 'POST':
        team_id = request.POST.get('team')
        note = request.POST.get('note', '')
        team = get_object_or_404(ResponseTeam, pk=team_id)

        Assignment.objects.create(
            team=team,
            crisis=crisis,
            assigned_by=request.user,
            note=note
        )
        messages.success(request, f"Team {team.name} assigned to this crisis.")
        return redirect('crisis_detail', pk=pk)

    teams = ResponseTeam.objects.filter(is_active=True)
    return render(request, 'response/assign_team.html', {'crisis': crisis, 'teams': teams})


@login_required
def post_status_update(request, pk):
    if not is_authorized_to_update(request.user):
        messages.error(request, "Access denied. Only Responders, Government Officials, or Admins can update status.")
        return redirect('crisis_detail', pk=pk)

    crisis = get_object_or_404(Crisis, pk=pk)
    if request.method == 'POST':
        message = request.POST.get('message')
        new_status = request.POST.get('new_status')

        StatusUpdate.objects.create(
            crisis=crisis,
            posted_by=request.user,
            message=message,
            new_status=new_status
        )

        # Update the main crisis status
        crisis.status = new_status
        crisis.save()

        messages.success(request, "Status updated successfully.")
        return redirect('crisis_detail', pk=pk)

    return render(request, 'response/post_status_update.html', {
        'crisis': crisis,
        'status_choices': Crisis.STATUS_CHOICES
    })
