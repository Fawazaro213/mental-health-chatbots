from django.urls import path
from . import views

urlpatterns = [
    path('', views.resources_page, name='resources'),
    path('emergency/', views.emergency_contacts, name='emergency_contacts'),
]