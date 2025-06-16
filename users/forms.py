# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *

class StudentVerificationForm(forms.Form):
    matric_number = forms.CharField(
        max_length=20,
        label="Matriculation Number",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 210591032',
            'class': 'form-control',
            'autofocus': 'autofocus'
        }),
        help_text="Enter your official university matriculation number"
    )
    
    def clean_matric_number(self):
        matric_number = self.cleaned_data.get('matric_number').upper().strip()
        try:
            return UniversityStudent.objects.get(matric_number=matric_number)
        except UniversityStudent.DoesNotExist:
            raise ValidationError(
                "This matric number was not found in our records. "
                "Please check the number or contact your university administration."
            )

class StudentRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username',
            'class': 'form-control'
        }),
        label='Username',
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            'class': 'form-control'
        }),
        label='Password',
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-control'
        }),
        label='Confirm Password',
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, student_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_data = student_data
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.student_data:
            user.email = self.student_data['email']
            user.first_name = self.student_data['first_name']
            user.last_name = self.student_data['last_name']
            user.is_student = True
            user.university = "Lagos State University"
            
            if commit:
                user.save()
                # Create or update user profile
                profile = user.userprofile
                profile.middle_name = self.student_data.get('middle_name', '')
                profile.faculty = self.student_data['faculty']
                profile.department = self.student_data['department']
                profile.year_admitted = self.student_data['year_admitted']
                profile.matric_number = self.student_data['matric_number']
                profile.save()
        return user



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                username = User.objects.get(email=username).username
            except User.DoesNotExist:
                pass
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']