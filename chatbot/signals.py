
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FlaggedMessage
from users.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=FlaggedMessage)
def notify_admin_on_flag(sender, instance, created, **kwargs):
    if created:
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                message=f"A message was flagged: \"{instance.message.content[:50]}\"",
                link=f"/admin/chat/with-user/{instance.message.sender.id}/"
            )
