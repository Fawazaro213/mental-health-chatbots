from django.contrib import admin
from .models import Conversation, Message, FlaggedMessage

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("user", "started_at", "is_active")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "timestamp", "intent_detected", "conversation")

@admin.register(FlaggedMessage)
class FlaggedMessageAdmin(admin.ModelAdmin):
    list_display = ("message", "reason", "flagged_at", "reviewed")
    list_filter = ("reviewed",)
    actions = ["mark_as_reviewed"]

    @admin.action(description="Mark selected messages as reviewed")
    def mark_as_reviewed(self, request, queryset):
        queryset.update(reviewed=True)

