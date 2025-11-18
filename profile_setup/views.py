from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.models import User, Group
from .models import Profile
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def public_page(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='student').exists():
            return redirect('student_home')
        elif request.user.groups.filter(name='staff').exists():
            return redirect('staff_home')
        elif request.user.is_superuser or request.user.groups.filter(name='admin').exists():
            return redirect('admin_home')
            
    return render(request, 'public.html')

@never_cache   
def student_login(request):
    request.user = get_user(request)

    if request.user.is_authenticated:
        profile = getattr(request.user, 'profile', None)
        if profile and profile.user_type == 'student':
            return redirect('student_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found for this user.")
                return redirect('student_login')

            if profile.user_type != 'student':
                messages.error(request, "You are not authorized for student login.")
                return redirect('student_login')

            if profile.session_key:
                messages.warning(request, "Logout on the other device to login here.")
                return redirect('student_login')

            login(request, user)
            profile.session_key = request.session.session_key
            profile.save()
            return redirect('student_home')

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'student_login.html')

@never_cache
def staff_login(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='staff').exists():
            return redirect('staff_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found for this user.")
                return redirect('staff_login')

            if profile.user_type != 'staff':
                messages.error(request, "You are not authorized for staff login.")
                return redirect('staff_login')

            if profile.session_key:
                messages.warning(request, "Logout on the other device to login here.")
                return redirect('staff_login')

            login(request, user)

            profile.session_key = request.session.session_key
            profile.save()

            return redirect('staff_home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'staff_login.html')    

@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='admin').exists():
            return redirect('admin_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_home')

            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found for this user.")
                return redirect('admin_login')

            if profile.user_type != 'admin':
                messages.error(request, "You are not authorized for admin login.")
                return redirect('admin_login')

            if profile.session_key:
                messages.warning(request, "Logout on the other device to login here.")
                return redirect('admin_login')

            login (request, user)

            profile.session_key = request.session.session_key
            profile.save()

            return redirect('admin_home')

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin_login.html')    

@never_cache
def logout_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            profile.session_key = None
            profile.save()
    auth_logout(request)
    return redirect('public')  