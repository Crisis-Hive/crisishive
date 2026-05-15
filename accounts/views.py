from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Role, Profile


def _unique_username(email):
    """Derive a unique username from the email address."""
    base = email.split('@')[0][:140]
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1
    return username


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip() or _unique_username(email)
        password = request.POST.get('password')
        role_id = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'accounts/register.html', {'roles': Role.objects.all()})

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
        )

        if role_id:
            user.role_id = role_id
            user.save()

        # Create profile
        Profile.objects.create(user=user)

        login(request, user)
        messages.success(request, f"Welcome, {username}!")
        return redirect('crisis_feed')

    return render(request, 'accounts/register.html', {'roles': Role.objects.all()})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('crisis_feed')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != request.user.username:
            if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                messages.error(request, "That username is already taken.")
                return render(request, 'accounts/profile.html', {'profile': profile_obj})
            request.user.username = new_username
        request.user.save()

        profile_obj.bio = request.POST.get('bio', '')
        profile_obj.phone = request.POST.get('phone', '')
        if 'avatar' in request.FILES:
            profile_obj.avatar = request.FILES['avatar']
        profile_obj.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile_obj})