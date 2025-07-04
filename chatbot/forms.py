from django import forms

class StartChatForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label="Conversation Title")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")