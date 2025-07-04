from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_chat, name='start_chat'),
    path('chat/<int:convo_id>/', views.chat_session, name='chat_session'),
    path('chat/<int:convo_id>/ajax/', views.ajax_chat_reply, name='ajax_chat_reply'),
    path("chat/rename/", views.rename_chat, name="rename_chat"),
    path("chat/delete/", views.delete_chat, name="delete_chat"),
    path("history/", views.chat_history, name="chat_history"),
]
