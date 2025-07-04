from django import forms
from .models import MentalHealthResource

class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = MentalHealthResource
        fields = ['title', 'file', 'category']