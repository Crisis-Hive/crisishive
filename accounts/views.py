from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Profile, Role


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role_id = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        role = Role.objects.filter(id=role_id).first()
        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        Profile.objects.create(user=user)
        login(request, user)
        return redirect('crisis_feed')

    roles = Role.objects.all()
    return render(request, 'accounts/register.html', {'roles': roles})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('crisis_feed')
        messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_obj.bio = request.POST.get('bio', '')
        profile_obj.phone = request.POST.get('phone', '')
        if 'avatar' in request.FILES:
            profile_obj.avatar = request.FILES['avatar']
        profile_obj.save()

        request.user.username = request.POST.get('username', request.user.username)
        request.user.save()
        messages.success(request, 'Profile updated.')
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile_obj})