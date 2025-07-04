from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from users.models import CustomUser
from mood.models import MoodEntry
from chatbot.models import FlaggedMessage
from django.db.models import Avg
from datetime import timedelta
from django.utils import timezone

@staff_member_required
def dashboard(request):
    # Only users who gave consent
    active_users = CustomUser.objects.filter(allow_data_collection=True)

    # Mood trends (last 14 days)
    recent_moods = (
        MoodEntry.objects.filter(user__allow_data_collection=True, timestamp__gte=timezone.now() - timedelta(days=14))
        .order_by("timestamp")
    )

    # Flagged messages
    flagged = FlaggedMessage.objects.all().order_by("-flagged_at")

    return render(request, "adminpanel/dashboard.html", {
        "users": active_users,
        "moods": recent_moods,
        "flagged_messages": flagged,
    })