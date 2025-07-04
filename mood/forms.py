from django import forms
from .models import MoodEntry

class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['score', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }