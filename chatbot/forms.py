from django import forms

class StartChatForm(forms.Form):
    title = forms.CharField(
        max_length=100, 
        required=False, 
        label="Conversation Title",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional title for your conversation'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'What would you like to talk about today?'}),
        label="Your Message",
        min_length=5,
        max_length=2000,
        help_text="Share what's on your mind (5-2000 characters)"
    )

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if message and len(message.strip()) < 5:
            raise forms.ValidationError("Please provide a message with at least 5 characters.")
        return message.strip()