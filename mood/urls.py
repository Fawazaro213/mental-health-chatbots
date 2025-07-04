from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.mood_check, name='mood_check'),
    path('history/', views.mood_history, name='mood_history'),
]