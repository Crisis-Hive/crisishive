from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Role, Profile

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role_id = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'accounts/register.html', {'roles': Role.objects.all()})

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
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
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.username = request.POST.get('username')
        request.user.save()
        
        profile.bio = request.POST.get('bio')
        profile.phone = request.POST.get('phone')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
        
    return render(request, 'accounts/profile.html', {'profile': profile})
