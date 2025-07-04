from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User  = get_user_model()


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Bot")])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    intent_detected = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.sender.upper()} @ {self.timestamp.strftime('%H:%M')} - {self.content[:30]}"

class FlaggedMessage(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='flag')
    reason = models.CharField(max_length=100, default='crisis_intervention')
    flagged_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"⚠️ {self.message.content[:40]}"


class ChatThread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"

class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"