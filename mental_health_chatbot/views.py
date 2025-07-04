from django.shortcuts import render
from users.models import UserProfile

def home(request):
    user = request.user
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = None
    return render(request, 'home.html', {'user': user, 'profile': profile})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def cookie_policy(request):
    return render(request, 'cookie_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')