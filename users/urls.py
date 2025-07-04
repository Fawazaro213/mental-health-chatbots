from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register/credentials/', register_credentials_view, name='register_credentials'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('dashboard/', student_dashboard, name='dashboard'),
    path('profile/', edit_profile, name='profile'),

    path('notifications/', notification_list, name='notification_list'),
]