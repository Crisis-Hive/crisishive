from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Role, Profile

# Allauth core authentication backend utilities
from allauth.account.utils import perform_login
from allauth.account.adapter import get_adapter


def _unique_username(email):
    """Derive a clean unique username string from the email address safely."""
    if not email or '@' not in email:
        return "user"
    
    # FIX: Select index 0 FIRST to grab the raw string before slicing characters
    parts = email.split('@')
    base = parts[0][:130] if parts else "user"
    
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1
    return username


def _get_roles():
    """Fetch roles safely - returns empty queryset if table doesn't exist yet."""
    try:
        return Role.objects.all()
    except Exception:
        return Role.objects.none()


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        # Fallback to email prefix if the user leaves username empty
        username_input = request.POST.get('username', '').strip()
        username = username_input if username_input else _unique_username(email)
        password = request.POST.get('password')
        role_id = request.POST.get('role')

        if not email or not password:
            messages.error(request, "Email and password are required fields.")
            return render(request, 'accounts/register.html', {'roles': _get_roles()})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'accounts/register.html', {'roles': _get_roles()})

        # Securely pass BOTH parameters to satisfy database column constraints
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if role_id:
            try:
                user.role_id = int(role_id)
                user.save()
            except (ValueError, TypeError):
                pass

        # Ensure profile creation record tracking matches up flawlessly
        Profile.objects.get_or_create(user=user)

        # Authenticate session inside active Allauth context tracking pools
        perform_login(
            request, 
            user, 
            email_verification='none', 
            redirect_url='crisis_feed', 
            signup=True
        )
        
        messages.success(request, f"Welcome, {username}!")
        return redirect('crisis_feed')

    return render(request, 'accounts/register.html', {'roles': _get_roles()})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        adapter = get_adapter(request)
        try:
            user = adapter.authenticate(request, email=email, password=password)
            if user:
                perform_login(
                    request, 
                    user, 
                    email_verification='none', 
                    redirect_url='crisis_feed'
                )
                return redirect('crisis_feed')
            else:
                messages.error(request, "Invalid email or password.")
        except Exception:
            messages.error(request, "Authentication failed. Check your input credentials.")

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
