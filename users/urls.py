from django.urls import path
from .views import (
    register_view,
    register_credentials_view,
    login_view,
    logout_view,
    dashboard_view,
    profile_update_view
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('register/credentials/', register_credentials_view, name='register_credentials'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', profile_update_view, name='profile'),
]