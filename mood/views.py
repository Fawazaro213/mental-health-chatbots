from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MoodEntryForm
from .models import MoodEntry

@login_required
def mood_check(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()

            request.user.userprofile.update_mood_stats()
            return redirect('mood_history')
    else:
        form = MoodEntryForm()

    return render(request, 'mood/mood_check.html', {'form': form})


from django.db.models import Avg
from django.utils.timezone import now, timedelta

@login_required
def mood_history(request):
    moods = MoodEntry.objects.filter(user=request.user).order_by('timestamp')

    average_mood = moods.aggregate(avg_score=Avg('score'))['avg_score'] or 0
    highest_mood = moods.order_by('-score', '-timestamp').first()
    lowest_mood = moods.order_by('score', 'timestamp').first()
    recent_moods = moods.order_by('-timestamp')[:10]  # Last 10 moods
    all_moods = list(moods)

    context = {
        'moods': moods,
        'average_mood': average_mood,
        'highest_mood': highest_mood,
        'lowest_mood': lowest_mood,
        'recent_moods': recent_moods,
        'all_moods': all_moods,
    }
    return render(request, 'mood/mood_history.html', context)

