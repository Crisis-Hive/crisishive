from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Volunteer, Donation
from feed.models import Crisis


# ---------------------------------------------------------------------------
# Role helpers
# ---------------------------------------------------------------------------

def get_role_name(user):
    return user.role.name if user.role else ''


def can_volunteer(user):
    """Only users with the Volunteer role (or staff) may sign up as volunteers."""
    return user.is_staff or get_role_name(user) == 'Volunteer'


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

@login_required
def volunteer_signup(request, pk):
    crisis = get_object_or_404(Crisis, pk=pk)

    if not can_volunteer(request.user):
        messages.error(
            request,
            "Only users with the Volunteer role can sign up to help. "
            "Update your role in your profile if you'd like to volunteer."
        )
        return redirect('crisis_detail', pk=pk)

    # Already signed up?
    if Volunteer.objects.filter(user=request.user, crisis=crisis).exists():
        messages.info(request, "You have already signed up as a volunteer for this crisis.")
        return redirect('crisis_detail', pk=pk)

    if request.method == 'POST':
        skill = request.POST.get('skill')
        Volunteer.objects.create(
            user=request.user,
            crisis=crisis,
            skill=skill,
        )
        messages.success(request, "Thank you for volunteering! Your request is pending approval.")
        return redirect('crisis_detail', pk=pk)

    return render(request, 'community/volunteer_signup.html', {
        'crisis': crisis,
        'skill_choices': Volunteer.SKILL_CHOICES,
    })


@login_required
def donate(request, pk):
    """Any authenticated user can donate — no role restriction."""
    crisis = get_object_or_404(Crisis, pk=pk)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        resource = request.POST.get('resource')
        message = request.POST.get('message')

        Donation.objects.create(
            donor=request.user,
            crisis=crisis,
            amount=amount if amount else None,
            resource=resource,
            message=message,
        )
        messages.success(request, "Thank you for your donation!")
        return redirect('crisis_detail', pk=pk)

    return render(request, 'community/donate.html', {'crisis': crisis})