from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResponseTeam, Assignment, StatusUpdate
from feed.models import Crisis


# ---------------------------------------------------------------------------
# Role helpers
# ---------------------------------------------------------------------------

def get_role_name(user):
    """Return the user's role name, or '' if they have no role assigned."""
    return user.role.name if user.role else ''


def can_assign_teams(user):
    """Government Officials and Admins (is_staff) can assign response teams."""
    return user.is_staff or get_role_name(user) == 'Government Official'


def can_post_status(user):
    """Responders, Government Officials, Journalists, and Admins can post status updates."""
    return user.is_staff or get_role_name(user) in (
        'Responder',
        'Government Official',
        'Journalist',
    )


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

@login_required
def assign_team(request, pk):
    if not can_assign_teams(request.user):
        messages.error(
            request,
            "Access denied. Only Government Officials or Admins can assign response teams."
        )
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
            note=note,
        )
        messages.success(request, f"Team '{team.name}' has been assigned to this crisis.")
        return redirect('crisis_detail', pk=pk)

    teams = ResponseTeam.objects.filter(is_active=True)
    return render(request, 'response/assign_team.html', {
        'crisis': crisis,
        'teams': teams,
    })


@login_required
def post_status_update(request, pk):
    if not can_post_status(request.user):
        messages.error(
            request,
            "Access denied. Only Responders, Government Officials, Journalists, or Admins can post status updates."
        )
        return redirect('crisis_detail', pk=pk)

    crisis = get_object_or_404(Crisis, pk=pk)

    if request.method == 'POST':
        message = request.POST.get('message')
        new_status = request.POST.get('new_status')

        StatusUpdate.objects.create(
            crisis=crisis,
            posted_by=request.user,
            message=message,
            new_status=new_status,
        )

        # Keep the main crisis status in sync
        crisis.status = new_status
        crisis.save()

        messages.success(request, "Status updated successfully.")
        return redirect('crisis_detail', pk=pk)

    return render(request, 'response/post_status_update.html', {
        'crisis': crisis,
        'status_choices': Crisis.STATUS_CHOICES,
    })