from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import *
from .models import *
# from chatbot.models import Conversation, Message


def register_view(request):
    # Step 1: Verify matric number
    if request.method == 'POST' and 'matric_number' in request.POST:
        verification_form = StudentVerificationForm(request.POST)
        if verification_form.is_valid():
            # Store student data in session and proceed to registration
            student_data = verification_form.cleaned_data['matric_number']
            request.session['registration_student'] = {
                'matric_number': student_data.matric_number,
                'first_name': student_data.first_name,
                'middle_name': student_data.middle_name,
                'last_name': student_data.last_name,
                'email': student_data.email,
                'faculty': student_data.faculty,
                'department': student_data.department,
                'year_admitted': student_data.year_admitted,
            }
            return redirect('register_credentials')
    else:
        verification_form = StudentVerificationForm()
    
    return render(request, 'users/verify_matric.html', {
        'form': verification_form
    })

def register_credentials_view(request):
    # Check if student data exists in session
    if 'registration_student' not in request.session:
        messages.warning(request, "Please start registration by entering your matric number")
        return redirect('register')
    
    student_data = request.session['registration_student']
    
    # Step 2: Create credentials
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, student_data=student_data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Clear session data
            del request.session['registration_student']
            
            messages.success(request, 'Registration successful! Welcome to the platform!')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm(student_data=student_data)
    
    return render(request, 'users/register_credentials.html', {
        'form': form,
        'student_data': student_data
    })

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

@login_required
def dashboard_view(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    # Get recent conversations
    # conversations = Conversation.objects.filter(user=user).order_by('-start_time')[:5]
    
    context = {
        'user': user,
        'profile': profile,
        # 'conversations': conversations,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user.userprofile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })