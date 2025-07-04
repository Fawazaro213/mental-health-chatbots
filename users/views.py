from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from types import SimpleNamespace
from chatbot.models import Conversation

# Step 1: Verify Matric Number
def register_view(request):
    if request.method == 'POST':
        verification_form = StudentVerificationForm(request.POST)
        if verification_form.is_valid():
            student = verification_form.cleaned_data['matric_number']  # this is the actual UniversityStudent object
            
            # Store full student data in session
            request.session['registration_student'] = {
                'matric_number': student.matric_number,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'middle_name': student.middle_name,
                'faculty': student.faculty,
                'department': student.department,
                'email': student.email,
            }
            return redirect('register_credentials')
    else:
        verification_form = StudentVerificationForm()

    return render(request, 'users/verify_matric.html', {
        'form': verification_form
    })


# Step 2: Set Password & Create Account
def register_credentials_view(request):
    if 'registration_student' not in request.session:
        messages.warning(request, "Please start registration by entering your matric number.")
        return redirect('register')

    raw_data = request.session['registration_student']
    student_data = SimpleNamespace(**raw_data)  # allows dot-access like student_data.first_name

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, student_data=raw_data)  # pass raw dict to form
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Clean up session
            del request.session['registration_student']

            messages.success(request, "🎉 Registration successful! Welcome to the platform.")
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm(student_data=raw_data)

    return render(request, 'users/register_credentials.html', {
        'form': form,
        'student_data': student_data  # pass full namespace object for use in template
    })


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid matric number or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')




@login_required
def student_dashboard(request):
    user = request.user
    profile = user.userprofile
    student_record = profile.student_record  # Optional shortcut

    unread = request.user.notifications.filter(is_read=False).count()
    notifications = request.user.notifications.all()[:5]
    
    # Greeting based on time
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    # Fetch last 5 conversations
    conversations = Conversation.objects.filter(user=user).order_by('-started_at')[:5]

    context = {
        "profile": profile,
        "student_record": student_record,
        "greeting": greeting,
        "conversations": conversations,
        "unread_notifications": unread,
        "recent_notifications": notifications,
    }
    return render(request, "users/dashboard.html", context)


@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        form = CombinedProfileForm(request.POST, request.FILES, instance=profile, user_instance=user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = CombinedProfileForm(instance=profile, user_instance=user)

    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def notification_list(request):
    notifications = request.user.notifications.order_by('-created_at')

    # Optional: mark all as read when visiting the page
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'users/notification_list.html', {
        'notifications': notifications
    })