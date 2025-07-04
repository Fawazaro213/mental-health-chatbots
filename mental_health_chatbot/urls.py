from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
# mental_health_chatbot/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('c/', include('chatbot.urls')),
    path('u/', include('users.urls')),
    path('mood/', include('mood.urls')),
    path('resources/', include('resources.urls')),
    path('admin-tools/', include('adminpanel.urls')),

    path('privacy-policy/', privacy_policy, name='privacy'),
    path('cookie-policy/', cookie_policy, name='cookies'),
    path('terms-of-service/', terms_of_service, name='terms'),
]
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)                                                                          